from config import *
from sanic.log import logger
from common.salt import saltdec, saltenc
from common.logger import LOGGING_CONFIG
from common.token import generate_token
from common.service_info import GetFullSystemData
from common.utils import is_file_or_dir
from sql_edge import *
from urllib import parse
from sanic.response import text
import requests
import websockets
import paramiko # sftp
import asyncio # async
import sanic
import os, json

edge_app = sanic.Sanic(name="edge_service", log_config=LOGGING_CONFIG)
edge_app.config.WEBSOCKET_PING_TIMEOUT = 30

@edge_app.on_request
async def token_auth(request):
    # 规定传送报文中必须为dict，包含"device_id"
    device_id = request.body.decode("utf-8")["device_id"]
    url_query = parse.urlparse(request.url).query
    param_dict = parse.parse_qs(url_query)
    if param_dict["path"] !="device_login":
        token = saltdec(param_dict["auth"], pwd)
        with open('token.txt','w') as token_file:
            # dict 
            # {device_id1: token1<str>, device_id2: token2<str>...}
            token_dict = json.loads(token_file.read())
            if token_dict.get(device_id):
                return text("Unauthorized", status=401)
            elif token_dict[device_id] != token:
                return text("Unauthorized", status=401)


# 手动上传操作日志模块
@edge_app.post('/report')
async def report(request):
    try:
        device_id = request.body.decode("utf-8")["device_id"]
        if sql_device_service_exist(device_id):
            device_host, device_port = sql_device_service_get(device_id)
            device_req = await requests.post("http://{}:{}/{}".format(device_host, device_port, "report"))
            if device_req.body.decode("utf-8") == "success":
                try:
                    logger.debug('building sftp connection')
                    transport = paramiko.Transport(sftp_port, sftp_port)
                    transport.connect(None, username=sftp_usrname, password=sftp_remote_log_pth)
                    logger.debug('sftp connection built successfully')
                except Exception:
                    logger.debug('build sftp connection error')
                # 尝试传输日志文件
                try:
                    sftp = paramiko.SFTPClient.from_transport(transport)
                    # 遍历设备操作日志目录，将所有的logfile上传
                    for f in os.listdir(sftp_log_pth):
                        if is_file_or_dir(f):
                            sftp.put(sftp_log_pth+f, sftp_remote_log_pth+f)
                        else:
                            for ff in os.listdir(sftp_log_pth+f):
                                if is_file_or_dir(ff):
                                    sftp.put(sftp_log_pth+f+"/"+ff, sftp_remote_log_pth+f+"/"+ff)
                                else:
                                    for fff in os.listdir(sftp_log_pth+f+"/"+ff):
                                        if is_file_or_dir(fff):
                                            sftp.put(sftp_log_pth+f+"/"+ff+"/"+fff, sftp_remote_log_pth+f+"/"+ff+"/"+fff)
                    transport.close()
                except Exception:
                    logger.debug('sftp transport process error')
        else:
            logger.info('device do not connect, device_id: {}'.format(device_id))
    except Exception:
        logger.error('sftp error')
    finally:
        logger.debug('logs sftp finish')

async def device_control_update(device_id, action):
    # 完成 <登陆设备管理> 与 <中心云设备同步>
    try:
        if action == "login":
            sql_device_service_connect(device_id, True)
        elif action == "logout":
            sql_device_service_connect(device_id, False)
    except:
        logger.error("sql error, location: device_control_update")
    finally:
        request = requests.post("http://{}:{}/{}".format(cloud_host, cloud_port, "device_async"), data=json(device_id, action))
        logger.debug("device_async finished")

async def device_status_update(device_id, status):
    # 设备status更新
    sql_device_status_update(device_id, status)

@edge_app.websocket('/device_login')
async def device_login(request, ws):
    try:
        auth_resp = await ws.recv()

        if auth_resp["method"]!="auth":
            return text("Unauthorized", status=401)

        try: 
            device_id = auth_resp["params"][0]
            device_pwd = auth_resp["params"][1]
        except:
            logger.info('auth data format error')
            return text("Unauthorized", status=401)

        if sql_device_service_exist(device_id): 
            if saltdec(device_pwd, pwd) == device_id: 
                asyncio.run(device_control_update(device_id=device_id, action="logout"))
                globals()["ws_{}".format(device_id)]=ws
                
                new_token = generate_token()# use specified edge snow-flake to generate
                with open('token.txt','w') as token_file:
                    # dict 
                    # {device_id1: token: <str>, device_id2:...}
                    token_dict = json.loads(token_file.read())
                    token_dict[device_id]=new_token
                    token_file.write(token_dict)


                ws.send(saltenc(new_token))
                while True:
                    resp = await ws.recv()
                    if resp["method"] == "heartbeat":
                        print("device_id: {}".format(device_id))
                        print("device_status: {}".format(resp["params"][0]))
            else:
                logger.error('login password error, device_id: '+device_id)
                return text("Unauthorized", status=401)
        else:
            logger.error('device do not register')
    except:
        logger.error('device login error')
    finally:
        logger.info('device log out, device_id: {}'.format(device_id))
        asyncio.run(device_control_update(device_id=device_id, action="logout"))
        sql_device_service_delete(device_id)
        with open('token.txt','w') as token_file:
            # dict 
            # {device_id1: token: <str>, device_id2:...}
            token_dict = json.loads(token_file.read())
            del token_dict[device_id]
            token_file.write(token_dict)

async def heartbeat(edge_app):
    while True:
        await asyncio.sleep(10)
        if globals()["ws_cloud"]!=None:
            print(globals()["ws_cloud"])
            logger.debug("heartbeat status report")
            ws = globals()["ws_cloud"]
            content = {"method":"heartbeat", "params":[GetFullSystemData()]}
            content = json.dumps(content)
            await ws.send(content)

async def connect_cloud(edge_app):
    logger.debug('start connect cloud')
    try:
        # async with websockets.connect("ws://{}:{}/edge_login".format(cloud_host, str(cloud_port))) as ws:
        async with websockets.connect("ws://" + cloud_host +":"+ str(cloud_port) + "/edge_login") as ws:            
            content = {"method":"auth","params":[edge_id, saltenc(edge_id, pwd)]}
            content = json.dumps(content)
            await ws.send(content)
            auth = await ws.recv()
            if auth:
                logger.info('websocket auth successfully')
                globals()["ws_cloud"]=ws
                # await heartbeat(ws)
                while True:
                    resp = await ws.recv()
                    resp = json.loads(resp)
                    if resp["method"] == "register":
                        device_id = resp["params"][0]
                        device_host = resp["params"][1]
                        device_port = resp["params"][2]
                        sql_device_service_insert(device_id, device_host, device_port)
    except Exception:
        logger.error('websocket with cloud process error')
    finally:
        globals()["ws_cloud"]=None

def app_run(host, port, access_log=False, debug=False, workers=1):
    edge_app.run(host=host, port=port, access_log=access_log, debug=debug, workers=workers)

@edge_app.before_server_start
async def main_start(*_):
    logger.debug("background process start")
    edge_app.add_task(heartbeat(edge_app))
    edge_app.add_task(connect_cloud(edge_app))

def start():
    app_run(edge_host, edge_port, access_log=False, debug=True, workers=1)

    
if __name__ == "__main__":
    start()