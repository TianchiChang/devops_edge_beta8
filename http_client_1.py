import sys
import ssl
import snowflake.client
import urllib.request
import json

fileHandler = open(sys.argv[3], "r")
listOfLines = fileHandler.readlines()
outputHandler = open(sys.argv[4], "w")
link = listOfLines[0].split(" ")[1].replace("\n","")
rurl = "http://"+sys.argv[1]+":"+sys.argv[2]+link
fileHandler.close()

def get_snowflake_uuid():
    guid = snowflake.client.get_guid()
    return guid

target = link.split("/")[2]
if target=="add":
    content = listOfLines[2]
    dic_data = json.loads(content)
    for dic in dic_data:
        keys = []
        key = list(dic.keys())
        value = list(dic.values())
        for i in range(len(key)):
            if key[i]=='id':
                id_v = get_snowflake_uuid()
                print(id_v)
                keys.append(id_v)
            elif key[i]=='hardware':
                keys.append(value[i]['model'])
                keys.append(value[i]['sn'])
            elif key[i]=='software':
                keys.append(value[i]['infrastructure']['version'])
                keys.append(value[i]['infrastructure']['last_update'])
                keys.append(value[i]['business']['version'])
                keys.append(value[i]['business']['last_update'])
            elif key[i]=='nic':
                for j in range(2):
                    try:
    	                keys.append(value[i][j]['type'])
                    except:
    	                keys.append('')
                    try:
    	                keys.append(value[i][j]['mac'])
                    except:
    	                keys.append('')
                    try:
    	                keys.append(value[i][j]['ipv4'])
                    except:
    	                keys.append('')
                try:
    	            keys.append(value[i][j]['type'])
                except:
    	            keys.append('')
                try:
    	            keys.append(value[i][j]['imei'])
                except:
    	            keys.append('')
                try:
                    keys.append(value[i][j]['ipv4'])
                except:
                    keys.append('')
            else:
                keys.append(value[i])
    params = {"method": "ADD","data": [{"id": keys[0], "info": keys}]}
    params = json.dumps(params)
    params = bytes(params, 'utf8')
    print(params) 
    request = urllib.request.Request(rurl, data=params, method='POST')
    response = urllib.request.urlopen(request).read() #, context=ssl_context
    
    output = {}
    status = json.loads(response.decode('utf-8'))["status"]
    if status==200:
        output.setdefault("status", "success")
        output.setdefault("data", "")
    elif status==400:
        output.setdefault("status", "fail")
        output.setdefault("data", "")
    outputHandler.write(json.dumps(output))
	        
elif target=="del":
    content = listOfLines[2]
    dic_data = json.loads(content)
    params = {"method": "DEL","data": [{"id": dic_data[0]}]}
    params = json.dumps(params)
    params = bytes(params, 'utf8')
    request = urllib.request.Request(rurl, data=params, method='POST')
    response = urllib.request.urlopen(request).read()
    
    output = {}
    status = json.loads(response.decode('utf-8'))["status"]
    if status==200:
        output.setdefault("status", "success")
        output.setdefault("data", "")
    elif status==400:
        output.setdefault("status", "fail")
        output.setdefault("data", "")
    outputHandler.write(json.dumps(output))
    
elif target=="get":
    content = listOfLines[2]
    dic_data = json.loads(content)
    params = {"method": "GET","data": [{"id": dic_data[0]}]}
    params = json.dumps(params)
    params = bytes(params, 'utf8')
    request = urllib.request.Request(rurl, data=params, method='POST')
    response = urllib.request.urlopen(request).read()
    #response = requests.post(url=rurl, json=)
    
    output = {}
    status = json.loads(response.decode('utf-8'))["status"]
    if status==200:
        output.setdefault("status", "success")
        data = json.loads(response.decode('utf-8'))["info"]
        output.setdefault("data", data)
    elif status==400:
        output.setdefault("status", "fail")
        output.setdefault("data", "")
    outputHandler.write(json.dumps(output))
    
elif target=="cha":
    content = listOfLines[2]
    dic_data = json.loads(content)
    params = {"method": "CHA","data": [{"id": dic_data[0]['id'], "data": [dic_data[0]['ziduan'], dic_data[0]['new_info']]}]}
    params = json.dumps(params)
    params = bytes(params, 'utf8')
    request = urllib.request.Request(rurl, data=params, method='POST')
    response = urllib.request.urlopen(request).read()
    #response = requests.post(url=rurl, json=)
    
    output = {}
    status = json.loads(response.decode('utf-8'))["status"]
    if status==200:
        output.setdefault("status", "success")
        output.setdefault("data", "")
    elif status==400:
        output.setdefault("status", "fail")
        output.setdefault("data", "")
    outputHandler.write(json.dumps(output))
    
elif target=="get_all":
    #response = requests.get(url=rurl)
    request = urllib.request.Request(rurl, method='GET')
    response = urllib.request.urlopen(request).read()
    output = {}
    status = json.loads(response.decode('utf-8'))["status"]
    if status==200:
        output.setdefault("status", "success")
        data = json.loads(response.decode('utf-8'))["info"]
        output.setdefault("data", data)
    outputHandler.write(json.dumps(output))

elif target=="get_group":
    content = listOfLines[2]
    dic_data = json.loads(content)
    params = {"method": "GET_GROUP","data": [{"id": dic_data[0]}]}
    params = json.dumps(params)
    params = bytes(params, 'utf8')
    request = urllib.request.Request(rurl, data=params, method='POST')
    response = urllib.request.urlopen(request).read()
    #response = requests.post(url=rurl, json=)
    
    output = {}
    status = json.loads(response.decode('utf-8'))["status"]
    if status==200:
        output.setdefault("status", "success")
        data = json.loads(response.decode('utf-8'))["info"]
        output.setdefault("data", data)
    elif status==400:
        output.setdefault("status", "fail")
        output.setdefault("data", "")
    outputHandler.write(json.dumps(output))

elif target=="get_all_group":
    #response = requests.get(url=rurl)
    request = urllib.request.Request(rurl, method='GET')
    response = urllib.request.urlopen(request).read()
    output = {}
    status = json.loads(response.decode('utf-8'))["status"]
    if status==200:
        output.setdefault("status", "success")
        data = json.loads(response.decode('utf-8'))["info"]
        output.setdefault("data", data)
    outputHandler.write(json.dumps(output))

elif target=="add_group":
    content = listOfLines[2]
    dic_data = json.loads(content)
    params = {"method": "ADD_GROUP","data": [{"group_id": dic_data["group_id"], "group_name": dic_data["group_name"]}]}
    params = json.dumps(params)
    params = bytes(params, 'utf8')
    request = urllib.request.Request(rurl, data=params, method='POST')
    response = urllib.request.urlopen(request).read()
    #response = requests.post(url=rurl, json=)
    
    output = {}
    status = json.loads(response.decode('utf-8'))["status"]
    if status==200:
        output.setdefault("status", "success")
        output.setdefault("data", "")
    elif status==400:
        output.setdefault("status", "fail")
        output.setdefault("data", "")
    outputHandler.write(json.dumps(output))

elif target=="del_group":
    content = listOfLines[2]
    dic_data = json.loads(content)
    params = {"method": "DEL_GROUP","data": [{"group_id": dic_data[0]}]}
    params = json.dumps(params)
    params = bytes(params, 'utf8')
    request = urllib.request.Request(rurl, data=params, method='POST')
    response = urllib.request.urlopen(request).read()
    #response = requests.post(url=rurl, json=)
    
    output = {}
    status = json.loads(response.decode('utf-8'))["status"]
    if status==200:
        output.setdefault("status", "success")
        output.setdefault("data", "")
    elif status==400:
        output.setdefault("status", "fail")
        output.setdefault("data", "")
    outputHandler.write(json.dumps(output))
    
elif target=="get_group_name":
    content = listOfLines[2]
    dic_data = json.loads(content)
    params = {"method": "GET_GROUP_NAME","data": [{"group_id": dic_data[0]}]}
    params = json.dumps(params)
    params = bytes(params, 'utf8')
    request = urllib.request.Request(rurl, data=params, method='POST')
    response = urllib.request.urlopen(request).read()
    #response = requests.post(url=rurl, json=)
    
    output = {}
    status = json.loads(response.decode('utf-8'))["status"]
    if status==200:
        output.setdefault("status", "success")
        data = json.loads(response.decode('utf-8'))["info"]
        output.setdefault("data", data)
    elif status==400:
        output.setdefault("status", "fail")
        output.setdefault("data", "")
    outputHandler.write(json.dumps(output))

elif target=="cha_group_name":
    content = listOfLines[2]
    dic_data = json.loads(content)
    params = {"method": "CHA_GROUP_NAME","data": [{"group_id": dic_data["group_id"], "group_name": dic_data["group_name"]}]}
    params = json.dumps(params)
    params = bytes(params, 'utf8')
    request = urllib.request.Request(rurl, data=params, method='POST')
    response = urllib.request.urlopen(request).read()
    
    output = {}
    status = json.loads(response.decode('utf-8'))["status"]
    if status==200:
        output.setdefault("status", "success")
        output.setdefault("data", "")
    elif status==400:
        output.setdefault("status", "fail")
        output.setdefault("data", "")
    outputHandler.write(json.dumps(output))

elif target=="get_all_group_info":
    #response = requests.get(url=rurl)
    request = urllib.request.Request(rurl, method='GET')
    response = urllib.request.urlopen(request).read()
    output = {}
    status = json.loads(response.decode('utf-8'))["status"]
    if status==200:
        output.setdefault("status", "success")
        data = json.loads(response.decode('utf-8'))["info"]
        output.setdefault("data", data)
    outputHandler.write(json.dumps(output))

elif target=="add_relation":
    content = listOfLines[2]
    dic_data = json.loads(content)
    params = {"method": "ADD_RELATION","data": [{"device_id": dic_data["device_id"], "group_id": dic_data["group_id"]}]}
    params = json.dumps(params)
    params = bytes(params, 'utf8')
    request = urllib.request.Request(rurl, data=params, method='POST')
    response = urllib.request.urlopen(request).read()
    
    output = {}
    status = json.loads(response.decode('utf-8'))["status"]
    if status==200:
        output.setdefault("status", "success")
        output.setdefault("data", "")
    elif status==400:
        output.setdefault("status", "fail")
        output.setdefault("data", "")
    outputHandler.write(json.dumps(output))
    
elif target=="del_relation":
    content = listOfLines[2]
    dic_data = json.loads(content)
    params = {"method": "DEL_RELATION","data": [{"device_id": dic_data["device_id"], "group_id": dic_data["group_id"]}]}
    params = json.dumps(params)
    params = bytes(params, 'utf8')
    request = urllib.request.Request(rurl, data=params, method='POST')
    response = urllib.request.urlopen(request).read()
    
    output = {}
    status = json.loads(response.decode('utf-8'))["status"]
    if status==200:
        output.setdefault("status", "success")
        output.setdefault("data", "")
    elif status==400:
        output.setdefault("status", "fail")
        output.setdefault("data", "")
    outputHandler.write(json.dumps(output))

elif target=="get_group_info":
    content = listOfLines[2]
    dic_data = json.loads(content)
    params = {"method": "GET_GROUP_INFO","data": [{"group_id": dic_data[0]}]}
    params = json.dumps(params)
    params = bytes(params, 'utf8')
    request = urllib.request.Request(rurl, data=params, method='POST')
    response = urllib.request.urlopen(request).read()
    #response = requests.post(url=rurl, json=)
    
    output = {}
    status = json.loads(response.decode('utf-8'))["status"]
    if status==200:
        output.setdefault("status", "success")
        data = json.loads(response.decode('utf-8'))["info"]
        output.setdefault("data", data)
    elif status==400:
        output.setdefault("status", "fail")
        output.setdefault("data", "")
    outputHandler.write(json.dumps(output))

