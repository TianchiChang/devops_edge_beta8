curl -X POST 'http://127.0.0.1:81/device/del' -d '{"method": "DEL", "data": [{"id": "00006"}]}'
curl -X POST 'http://127.0.0.1:81/device/del' -d '{"method": "DEL", "data": [{"id": "00007"}]}'
curl -X POST 'http://127.0.0.1:81/device/cha_group_name' -d '{"method": "CHA_GROUP_NAME","data": [{"group_id": "1", "group_name": "Qing Shui He Xiao Qu"}]}'
