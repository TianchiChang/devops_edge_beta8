import paramiko, os
from config import *
from common.utils import is_file_or_dir

if __name__=="__main__":
    client = paramiko.Transport(sftp_host, sftp_port)
    client.connect( username=sftp_usrname,password=sftp_pwd)
    sftp = paramiko.SFTPClient.from_transport(client)
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
    client.close()