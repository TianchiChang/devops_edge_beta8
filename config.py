import time

edge_id = "4773513196776456193"
db_name = "X"+"4773513196776456193"
edge_host = "localhost"
edge_port = 82
cloud_host = "localhost"
cloud_port = 81
log_path = "./Logs/"
remote_log_path = "./Logs/edge_" + edge_id +"/"

sftp_usrname = "Extrac0n"
sftp_pwd = "HanKangRui886"
sftp_log_pth = "D:/Grade 3 Sec/devops_edge/Logs/"
sftp_remote_log_pth = "D:/Grade 3 Sec/devops_centre/Logs/" + edge_id + "/"
sftp_host = '127.0.0.1'
sftp_port = 22



globals()["ws_edge"] = None

pwd = "the edge password"

today = time.strftime('%Y-%m-%d',time.localtime(time.time()))