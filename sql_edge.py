import pymysql

def list_parse(
    device_id='null',
    device_name = 'null',
    edge_id = 'null',
    status = 'null',
    connection = 1,
    device_host = '10.0.0.1',
    device_port='80',
    device_description = 'null',
    create_time = 'null',
    last_update = 'null',
    hardware_model = 'null',
    hardware_sn = 'null',
    software_infra_version = 'null',
    software_infra_last_update = 'null',
    software_bus_version = 'null',
    software_bus_last_update = 'null',
    nic1_type = 'null',
    nic1_mac = 'null',
    nic1_ipv4 = 'null',
    nic2_type = 'null',
    nic2_mac = 'null',
    nic2_ipv4 = 'null',
    nic3_type = 'null',
    nic3_imei = 'null',
    nic3_ipv4 = 'null'
) ->list:
    return_list=[device_id, device_name, edge_id, status, connection, device_host, device_port,
     device_description, create_time, last_update, hardware_model, hardware_sn,
     software_infra_version, software_infra_last_update, software_bus_version,
     software_bus_last_update, nic1_type, nic1_mac, nic1_ipv4, nic2_type,
     nic2_mac, nic2_ipv4, nic3_type, nic3_imei, nic3_ipv4]
    return return_list

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

def sql_change(db_name,device_id,ziduan,new_info):
    try:
        db = pymysql.connect(host='localhost', user='root', password='123456', database=db_name)
        print('数据库连接成功!')

        cur=db.cursor()
        sql="update device set " + ziduan + "=%s where device_id=%s" #创建sql语句这一步中，ziduan必须用字符串拼接
        value=(new_info,device_id)
        cur.execute(sql,value)
        db.commit()
        print("数据更新成功")
        db.close()
        return 1

    except pymysql.Error as e:
        print('数据更新失败' + str(e))
        db.rollback()
        db.close()
        return 0

def identify(op_id):
    db = pymysql.connect(host='localhost', user='root', password='123456', database="x4773513196776456193")
    cur=db.cursor()

    sql='SELECT * FROM device where device_id=%s'
    value=(op_id)
    cur.execute(sql,value)
    results=cur.fetchall()

    for row in results:
        db.close()
        if row:
            return 1
        else:
            return 0

def sql_device_service_exist(device_id):
    suc = identify(device_id)
    return suc
def sql_device_service_delete(device_id):
    suc = sql_del('x4773513196776456193',device_id)
    return suc
def sql_device_service_insert(device_id, device_host, device_port):
    suc = sql_add('x4773513196776456193',list_parse(device_id=device_id,device_host=device_host,device_port=device_port))
    return suc
def sql_device_service_connect(device_id, new_value):
    suc = sql_change('x4773513196776456193',device_id,"connection",new_value)
    return suc
def sql_device_status_update():
    return True
def sql_device_service_get(device_id):
    return "localhost","9000"
