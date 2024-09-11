import sys
import ssl
import json
import pymysql
import traceback
from sanic import Sanic
from sanic import Request, text
from sanic import response
from config import *
from common.salt import saltdec, saltenc
from sanic.log import logger

app = Sanic(name = "sanic_IoT_Demo", log_config=LOGGING_CONFIG)

# DBHOST = 'localhost'
# DBUSER = 'debian-sys-maint'
# DBPASS = 'snxfaTSIXPtlHOXe'
# DBNAME = 'dbtest'

dbname = 'cloud_server'

def identify(op_id):
    db = pymysql.connect(host='localhost', user='root', password='123456', database="cloud_server")
    cur=db.cursor()

    sql='SELECT * FROM edge_server where edge_id=%s'
    value=(op_id)
    cur.execute(sql,value)
    results=cur.fetchall()

    for row in results:
        db.close()
        return row

def sql_add(db_name,data):
    try:
        db = pymysql.connect(host='localhost', user='root', password='123456', database=db_name)
        print('数据库连接成功!')

        cur=db.cursor()

        sql = 'insert into device value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        value=data
        cur.execute(sql, value)
        db.commit()
        print("数据插入成功")
        db.close()
        return 1

    except pymysql.Error as e:
        print('数据插入失败' + str(e))
        db.rollback()
        db.close()
        return 0

def sql_del(db_name,op_id):
    try:
        db = pymysql.connect(host='localhost', user='root', password='123456', database=db_name)
        print('数据库连接成功!')

        cur=db.cursor()
        sql="delete from device where device_id=%s"
        value=(op_id)
        cur.execute(sql,value)
        db.commit()
        print("数据删除成功")
        db.close()
        return 1

    except pymysql.Error as e:
        print('数据删除失败' + str(e))
        db.rollback()
        db.close()
        return 0

def sql_get(db_name,op_id) -> str:
    try:
        db = pymysql.connect(host='localhost', user='root', password='123456', database=db_name)
        #print('数据库连接成功!')

        cur=db.cursor()

        sql='SELECT * FROM device where device_id=%s'
        value=(op_id)
        cur.execute(sql,value)
        results=cur.fetchall()
        #print(cur.fetchall())

        for row in results:
            query_result='device_id:'+row[0]+', '+'name:'+row[1]+', '+'edge_id:'+row[2]+', '\
            +'status:'+row[3]+', '+'connection:'+str(row[4])+', '+'device_host:'+row[5]+','\
            +'device_description:'+row[6]+', '+'create_time:'+row[7]+', '+'last_update:'+row[8]\
            +', '+'hardware_model:'+row[9]+', '+'hardware_sn:'+row[10]+', '\
            +'software_infra_version:'+row[11]+', '+'software_infra_last_update:'+row[12]\
            +', '+'software_bus_version:'+row[13]+', '+'software_bus_last_update:'+row[14]\
            +', '+'nic1_type:'+row[15]+', '+'nic1_mac:'+row[16]+', '+'nic1_ipv4:'+row[17]\
            +', '+'nic2_type:'+row[18]+', '+'nic2_mac:'+row[19]+', '+'nic2_ipv4:'+row[20]\
            +', '+'nic3_type:'+row[21]+', '+'nic3_imei:'+row[22]+', '+'nic3_ipv4:'+row[23]
        db.close()
        return query_result

    except pymysql.Error as e:
        print('数据查询失败' + str(e))
        db.close()
        return 0

def sql_cha(db_name,device_id,ziduan,new_info):
    try:
        db = pymysql.connect(host='localhost', user='root', password='123456', database=db_name)
        print('数据库连接成功!')

        cur=db.cursor()
        sql="update device set " + ziduan + "=%s where device_id=%s" #创建sql语句这一步中，ziduan必须用字符串拼接
        value=(new_info, device_id)
        cur.execute(sql, value)
        db.commit()
        print("数据更新成功")
        db.close()
        return 1

    except pymysql.Error as e:
        print('数据更新失败' + str(e))
        db.rollback()
        db.close()
        return 0

def sql_get_all(db_name):
    try:
        db = pymysql.connect(host='localhost', user='root', password='123456', database=db_name)
        print('数据库连接成功!')

        cur=db.cursor()

        sql='SELECT * FROM device'
        cur.execute(sql)
        results=cur.fetchall()
        #print(cur.fetchall())

        for row in results:
            query_result='device_id:'+row[0]+', '+'name:'+row[1]+', '+'edge_id:'+row[2]+', '\
            +'status:'+row[3]+', '+'connection:'+str(row[4])+', '+'device_host:'+row[5]+','\
            +'device_description:'+row[6]+', '+'create_time:'+row[7]+', '+'last_update:'+row[8]\
            +', '+'hardware_model:'+row[9]+', '+'hardware_sn:'+row[10]+', '\
            +'software_infra_version:'+row[11]+', '+'software_infra_last_update:'+row[12]\
            +', '+'software_bus_version:'+row[13]+', '+'software_bus_last_update:'+row[14]\
            +', '+'nic1_type:'+row[15]+', '+'nic1_mac:'+row[16]+', '+'nic1_ipv4:'+row[17]\
            +', '+'nic2_type:'+row[18]+', '+'nic2_mac:'+row[19]+', '+'nic2_ipv4:'+row[20]\
            +', '+'nic3_type:'+row[21]+', '+'nic3_imei:'+row[22]+', '+'nic3_ipv4:'+row[23]
            print(query_result)
        print('数据查询成功!')
        db.close()
        return 1
    except pymysql.Error as e:
        print('数据查询失败' + str(e))
        db.close()
        return 0

######
def sql_get_group(op_id):
    try:
        db = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DBNAME)
        print('数据库连接成功!')

        cur = db.cursor()

        sql = 'SELECT * FROM device where id=%s'
        value = (op_id)
        cur.execute(sql, value)
        results = cur.fetchall()
        
        for row in results:
            query_result='id:'+row[0]+', '+'name:'+row[1]+', '+'device_description:'+row[2]\
            +', '+'create_time:'+row[3]+', '+'last_update:'+row[4]+', '+'hardware_model:'+row[5]+', '\
            +'hardware_sn:'+row[6]+', '+'software_infra_version:'+row[7]+', '+'software_infra_last_update:'\
            +row[8]+', '+'software_bus_version:'+row[9]+', '+'software_bus_last_update:'+row[10]+', '\
            +'nic1_type:'+row[11]+', '+'nic1_mac:'+row[12]+', '+'nic1_ipv4:'+row[13]+', '\
            +'nic2_type:'+row[14]+', '+'nic2_mac:'+row[15]+', '+'nic2_ipv4:'+row[16]+', '\
            +'state:'+row[17]+', '+'divide_into_groups:'+row[18]
            print("设备的分组查询成功")
            db.close()
            return row[18]

    except pymysql.Error as e:
        print('数据查询失败' + str(e))
        db.close()
        return 0

def sql_get_all_group(db_name):
    try:
        db = pymysql.connect(host='localhost', user='root', password='123456', database=db_name)
        print('数据库连接成功!')

        cur=db.cursor()

        sql='SELECT * FROM group_info'
        cur.execute(sql)
        results=cur.fetchall()
        #print(cur.fetchall())

        for row in results:
            query_result='group_id:'+str(row[0])+', '+'group_name:'+row[1]
            print(query_result)
        print('数据查询成功!')
        db.close()
        return 1
    except pymysql.Error as e:
        print('数据查询失败' + str(e))
        db.close()
        return 0

def sql_add_group(db_name,group_id,group_name):
    try:
        db = pymysql.connect(host='localhost', user='root', password='123456', database=db_name)
        print('数据库连接成功!')

        cur=db.cursor()

        sql = "insert into group_info values (%s,%s);"
        value = (group_id,group_name)
        cur.execute(sql,value)
        db.commit()
        print("数据插入成功")
        db.close()
        return 1

    except pymysql.Error as e:
        print('数据插入失败' + str(e))
        db.rollback()
        db.close()
        return 0
    
def sql_del_group(db_name,op_group_id):
    try:
        db = pymysql.connect(host='localhost', user='root', password='123456', database=db_name)
        print('数据库连接成功!')

        cur=db.cursor()

        sql = "delete from group_info where group_id="+str(op_group_id)
        cur.execute(sql)
        db.commit()
        print("数据删除成功")
        db.close()
        return 1

    except pymysql.Error as e:
        print('数据删除失败' + str(e))
        db.rollback()
        db.close()
        return 0

def sql_get_group_name(db_name,op_group_id):
    try:
        db = pymysql.connect(host='localhost', user='root', password='123456', database=db_name)
        print('数据库连接成功!')

        cur=db.cursor()

        sql = "select group_name from group_info where group_id="+str(op_group_id)
        cur.execute(sql)
        results = cur.fetchall()
        ans=results[0][0]
        return ans
        print("数据查询成功")
        db.close()


    except pymysql.Error as e:
        print('数据删除失败' + str(e))
        db.rollback()
        db.close()
        return 0

def sql_cha_group_name(db_name,op_group_id,group_new_name):
    try:
        db = pymysql.connect(host='localhost', user='root', password='123456', database=db_name)
        print('数据库连接成功!')

        cur=db.cursor()
        sql = "update group_info set group_name=%s where group_id="+str(op_group_id)
        value=(group_new_name)
        cur.execute(sql,value)
        db.commit()
        print("数据修改成功")
        db.close()
        return 1


    except pymysql.Error as e:
        print('数据修改失败' + str(e))
        db.rollback()
        db.close()
        return 0

######
def sql_get_all_group_info():
    try:
        db = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DBNAME)
        print('数据库连接成功!')
    
        cur=db.cursor()
    
        sql='SELECT * FROM device'
        cur.execute(sql)
        results=cur.fetchall()
    
        for row in results:
            query_result='id:'+row[0]+', '+'name:'+row[1]+', '+'divide_into_groups:'+row[18]
            print(query_result)
        print("数据查询成功")
        db.close()
        return query_result
    
    except pymysql.Error as e:
        print('数据查询失败' + str(e))
        db.close()
        return 0

def sql_add_relation(db_name,device_id,group_id):
    try:
        db = pymysql.connect(host='localhost', user='root', password='123456', database=db_name)
        print('数据库连接成功!')

        cur=db.cursor()
        sql = "insert into group_mapping values (null,%s,%s);"
        value=(device_id,group_id)
        cur.execute(sql,value)
        db.commit()
        print("数据插入成功")
        db.close()
        return 1

    except pymysql.Error as e:
        print('数据插入失败' + str(e))
        db.rollback()
        db.close()
        return 0

def sql_del_relation(db_name,device_id,group_id):
    try:
        db = pymysql.connect(host='localhost', user='root', password='123456', database=db_name)
        print('数据库连接成功!')

        cur=db.cursor()
        #sql语句传参必须按下面的方式写
        sql = "delete from group_mapping where device_id=%s and group_id="+str(group_id);
        value=(device_id)
        cur.execute(sql,value)
        db.commit()
        print("数据删除成功")
        db.close()
        return 1

    except pymysql.Error as e:
        print('数据删除失败' + str(e))
        db.rollback()
        db.close()
        return 0

@app.post("/device/add")
async def sadd(request):
#    data = request.json["data"][0]["id"]
#    repe = sql_get(data)
    suc = sql_add('cloud_server', request.json["data"][0]["info"])
    if suc==0:
        return response.json({"status": 400, "message": "insert fail"})
    else:
        if globals()["ws_edge"]!=None:
            ws = globals()["ws_edge"]
            content = {"method":"register", "params":[request.json["data"][0]["info"][0], request.json["data"][0]["info"][5], request.json["data"][0]["info"][6]]}
            content = json.dumps(content)
            await ws.send(content)
        return response.json({"status": 200, "message": "create device successfully"})

@app.post("/device/del")
async def sdel(request):
    data = request.json["data"][0]["id"]
    suc = sql_del('cloud_server', data)
    if suc==0:
        return response.json({"status": 400, "message": "delete fail"})
    else:
        if globals()["ws_edge"]!=None:
            ws = globals()["ws_edge"]
            content = {"method":"delete", "params":[request.json["data"][0]["id"]]}
            content = json.dumps(content)
            await ws.send(content)
        return response.json({"status": 200, "message": "deleted device successfully"})

@app.post("/device/get")
async def sget(request):
    data = request.json["data"][0]["id"]
    suc = sql_get('cloud_server', data)
    if suc==0:
        return response.json({"status": 400, "message": "device does not exist"})
    else:
        return response.json({"status": 200, "message": "get info successfully", "info": suc})

@app.post("/device/cha")
async def scha(request):
    data1 = request.json["data"][0]["id"]
    data2 = request.json["data"][0]["data"][0]
    data3 = request.json["data"][0]["data"][1]
    suc = sql_cha('cloud_server', data1, data2, data3)
    if suc==0:
        return response.json({"status": 400, "message": "change fail"})
    else:
        return response.json({"status": 200, "message": "changed device successfully"})

@app.get("/device/get_all")
async def sget_all(request):
    suc = sql_get_all('cloud_server')
    if suc==0:
        return response.json({"status": 400, "message": "get fail"})
    else:
        return response.json({"status": 200, "message": "get device info successfully", "info": suc})

@app.post("/device/get_group")
async def sget_group(request):
    data = request.json["data"][0]["id"]
    suc = sql_get_group('cloud_server', data)
    if suc==0:
        return response.json({"status": 400, "message": "device does not exist"})
    else:
        return response.json({"status": 200, "message": "get name successfully", "info": suc})

@app.get("/device/get_all_group")
async def sget_all_group(request):
    suc = sql_get_all_group('cloud_server')
    if suc==0:
        return response.json({"status": 400, "message": "get fail"})
    else:
        return response.json({"status": 200, "message": "get group info successfully", "info": suc})

@app.post("/device/add_group")
async def sadd_group(request):
    data1 = request.json["data"][0]["group_id"]
    data2 = request.json["data"][0]["group_name"]
    suc = sql_add_group('cloud_server', data1, data2)
    if suc==0:
        return response.json({"status": 400, "message": "add fail"})
    else:
        return response.json({"status": 200, "message": "create group successfully"})

@app.post("/device/del_group")
async def sdel_group(request):
    #data = request.json["data"][0]["drop_group"]
    data = request.json["data"][0]["group_id"]
    suc = sql_del_group('cloud_server', data)
    if suc==0:
        return response.json({"status": 400, "message": "delete fail"})
    else:
        return response.json({"status": 200, "message": "deleted group successfully"})

@app.post("/device/get_group_name")
async def sget_group_name(request):
    data = request.json["data"][0]["group_id"]
    suc = sql_get_group_name('cloud_server', data)
    if suc==0:
        return response.json({"status": 400, "message": "device does not exist"})
    else:
        return response.json({"status": 200, "message": "get name successfully", "info": suc})

@app.post("/device/cha_group_name")
async def scha_group_name(request):
    data1 = request.json["data"][0]["group_id"]
    data2 = request.json["data"][0]["group_name"]
    suc = sql_cha_group_name('cloud_server', data1, data2)
    if suc==0:
        return response.json({"status": 400, "message": "change fail"})
    else:
        return response.json({"status": 200, "message": "changed group name successfully"})

@app.get("/device/get_all_group_info")
async def sget_all_group_info(request):
    suc = sql_get_all_group_info('cloud_server')
    if suc==0:
        return response.json({"status": 400, "message": "get fail"})
    else:
        return response.json({"status": 200, "message": "get device info successfully", "info": suc})

@app.post("/device/add_relation")
async def sadd_relation(request):
    data1 = request.json["data"][0]["device_id"]
    data2 = request.json["data"][0]["group_id"]
    suc = sql_add_relation('cloud_server', data1, data2)
    if suc==0:
        return response.json({"status": 400, "message": "add fail"})
    else:
        return response.json({"status": 200, "message": "create relation successfully"})

@app.post("/device/del_relation")
async def sdel_relation(request):
    data1 = request.json["data"][0]["device_id"]
    data2 = request.json["data"][0]["group_id"]
    suc = sql_del_relation('cloud_server', data1, data2)
    if suc==0:
        return response.json({"status": 400, "message": "delete fail"})
    else:
        return response.json({"status": 200, "message": "deleted relation successfully"})

@app.post("/device/get_group_info")
async def sget_group_info(request):
    data = request.json["data"][0]["group_id"]
    suc = sql_get_group_info('cloud_server', data)
    if suc==0:
        return response.json({"status": 400, "message": "device does not exist"})
    else:
        return response.json({"status": 200, "message": "get info successfully", "info": suc})


@app.post("/device_async")
async def sdevice_async(request):
    device_id = request.json["device_id"]
    action = request.json["action"]
    suc = 0
    if action=="login":
        suc = sql_cha('cloud_server', device_id, "connection", 1)
    elif action=="logout":
        suc = sql_cha('cloud_server', device_id, "connection", 1)
    if suc==1:
        logger.info("changed device successfully")
        print("changed device successfully") #logger
        return response.json({"status": 200, "message": "changed device successfully"})
    logger.error("change fail")
    print("change fail") #logger
    return response.json({"status": 400, "message": "change fail"})

@app.websocket("/edge_login")
async def edge_login(request,ws):
    try:
        auth_data = await ws.recv()
        globals()["ws_edge"] = ws
        target = json.loads(auth_data)["params"][1]
        dec_target = saltdec(target, pwd)
        origin = json.loads(auth_data)["params"][0]
        exists = identify(origin)
        if dec_target==origin and exists!=0:
            print("connection success")
            await ws.send("success")
            while True:
                receive_data = await ws.recv()
                logger.info(receive_data)
                print(receive_data) #logger
    except Exception:
        logger.error('websocket with edge process error')
    finally:
        globals()["ws_edge"]=None

if __name__ == '__main__':
#    ssl.SSLContext(protocol=ssl.PROTOCOL_TLSv1_2)
#    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
#    context.load_cert_chain(certfile="/cert/server.crt",keyfile="/cert/server.key")
#    context.load_verify_locations("/cert/client.crt")
#    context.verify_mode=ssl.CERT_REQUIRED
#    context.check_hostname = False
    app.run(host=cloud_host, port=int(cloud_port)) #, ssl=ssl_context
