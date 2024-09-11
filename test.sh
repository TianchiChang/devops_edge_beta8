curl -X POST 'http://127.0.0.1:81/device/add' -d '{"method": "ADD", "data": [{"id": "00005", "info": ["00005", "npl7c", "4773513196776456193", "alive", 0, "127.0.0.1", "86", "controller", "2017-11-15 11:12:59", "2022-01-07 03:37:04", "x86 PC", "t2tp2fh6", "5.6", "2021-06-20 18:30:50", "8.9", "2021-11-15 11:12:59", "eth", "69:3d:71:d9:e1:58", "22.183.83.93", "wifi", "97:53:f6:ba:50:48", "234.227.223.46", "wifi", "97:53:f6:ba:50:48", "234.227.223.46"]}]}'
sleep 2
curl -X POST 'http://127.0.0.1:81/device/add' -d '{"method": "ADD", "data": [{"id": "00006", "info": ["00006", "npl7c", "4773513196776456193", "alive", 0, "127.0.0.1", "85", "controller", "2017-11-15 11:12:59", "2022-01-07 03:37:04", "x86 PC", "t2tp2fh6", "5.6", "2021-06-20 18:30:50", "8.9", "2021-11-15 11:12:59", "eth", "69:3d:71:d9:e1:58", "22.183.83.93", "wifi", "97:53:f6:ba:50:48", "234.227.223.46", "wifi", "97:53:f6:ba:50:48", "234.227.223.46"]}]}'
sleep 2
curl -X POST 'http://127.0.0.1:81/device/add' -d '{"method": "ADD", "data": [{"id": "dedajfaiuhfahifiua", "info": ["00007", "npl7c", "4773513196776456193", "alive", 0, "127.0.0.1", "87", "controller", "2017-11-15 11:12:59", "2022-01-07 03:37:04", "x86 PC", "t2tp2fh6", "5.6", "2021-06-20 18:30:50", "8.9", "2021-11-15 11:12:59", "eth", "69:3d:71:d9:e1:58", "22.183.83.93", "wifi", "97:53:f6:ba:50:48", "234.227.223.46", "wifi", "97:53:f6:ba:50:48", "234.227.223.46"]}]}'
sleep 2
curl -X POST 'http://127.0.0.1:81/device/del' -d '{"method": "DEL", "data": [{"id": "00005"}]}'
sleep 2
curl -X POST 'http://127.0.0.1:81/device/get' -d '{"method": "GET", "data": [{"id": "00006"}]}'
sleep 2
curl -X POST 'http://127.0.0.1:81/device/cha' -d '{"method": "CHA", "data": [{"id": "00005", "data": ["status", "off-line"]}]}'
sleep 2
curl -X POST 'http://127.0.0.1:81/device/get' -d '{"method": "GET", "data": [{"id": "00006"}]}'
sleep 2
curl -X GET 'http://127.0.0.1:81/device/get_all'
sleep 2
curl -X POST 'http://127.0.0.1:81/device/add_group' -d '{"method": "ADD_GROUP","data": [{"group_id": "4", "group_name": "Xin Xiao Qu"}]}'
sleep 2
curl -X POST 'http://127.0.0.1:81/device/del_group' -d '{"method": "DEL_GROUP","data": [{"group_id": "4"}]}'
sleep 2
curl -X POST 'http://127.0.0.1:81/device/get_group_name' -d '{"method": "GET_GROUP_NAME","data": [{"group_id": "1"}]}'
sleep 2
curl -X POST 'http://127.0.0.1:81/device/cha_group_name' -d '{"method": "CHA_GROUP_NAME","data": [{"group_id": "1", "group_name": "Qing-Shui-He-Xiao-Qu"}]}'
sleep 2
curl -X GET 'http://127.0.0.1:81/device/get_all_group'
sleep 2
curl -X POST 'http://127.0.0.1:81/device/add_relation' -d '{"method": "ADD_RELATION","data": [{"device_id": "00006", "group_id": "1"}]}'
sleep 2
curl -X POST 'http://127.0.0.1:81/device/del_relation' -d '{"method": "DEL_RELATION","data": [{"device_id": "00006", "group_id": "1"}]}'
