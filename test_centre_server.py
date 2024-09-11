import sys
import ssl
import json
from sanic import Sanic
from sanic import Request, text
from sanic import response
from config import *
from common.salt import saltdec, saltenc

app = Sanic(__name__)

@app.post("/device/device_async")
async def sdevice_async(request):
    device_id = request.json["device_id"]
    action = request.json["action"]
    suc = 0
    if action=="login":
        suc = sql_cha('cloud_server', device_id, "connect", 1)
    elif action=="logout":
        suc = sql_cha('cloud_server', device_id, "connect", 1)
    if suc==1:
        print("changed device successfully") #logger
        return 1
    print("change fail") #logger
    return 0

@app.websocket("/edge_login")
async def edge_login(request,ws):
    try:
        auth_data = await ws.recv()
        globals()["ws_edge"] = ws
        print(auth_data)
        target = json.loads(auth_data)["params"][1]
        dec_target = saltdec(target, pwd)
        origin = json.loads(auth_data)["params"][0]
        if dec_target==origin:
            # await ws.send("success")
            while True:
                receive_data = await ws.recv()
                print(receive_data) #logger
    except Exception:
        logger.error('websocket with edge process error')
    finally:
        globals()["ws_edge"]=None
        
    
if __name__ == "__main__":
    app.run(host=cloud_host, port=int(cloud_port))
