from Crypto.Cipher import AES
import base64
import random
from hashlib import md5
from Crypto.Util.Padding import pad, unpad

def md(s,salt): # md5加密，盐加在了末尾
    mdd=md5()
    mdd.update(s+salt)
    return mdd.digest()

def dec(key,iv,data): # aes解密
    decc= AES.new(key,AES.MODE_CBC,iv)
    result=unpad(decc.decrypt(data),block_size=16).decode()
    return result

def enc(key,iv,data): # aes加密
    decc = AES.new(key, AES.MODE_CBC, iv)
    result=decc.encrypt(pad(data.encode(),block_size=16))
    return result

def saltenc(xdata, password):  # 加盐解密
    salt = md(str(random.random()).encode(), b'')[4:12]  # 随机生成盐，8位
    st = md(password.encode(), salt)  # 第一次md5
    keys = md(st + password.encode(), salt)  # 第一次md5的结果加上原始key再进行一次md5
    key = st + keys  # 两次加密结果衔接作为32位的加密key
    iv = md(keys + password.encode(), salt)  # 将得到的key再和原始key相加进行一次md5，作为偏移量iv
    encda = enc(key, iv, xdata)  # 使用加密key和iv进行加密
    result = base64.b64encode(b'Salted__' + salt + encda).decode()  # 返回结果带上salted和盐，进行base加密
    return result

def saltdec(xdata,password):# 加盐加密
    s=base64.b64decode(xdata) # base64解密
    data=s[16:] # 数据从第17位开始
    salt=s[8:16] # 盐
    st=md(password.encode(),salt) # 第一次md5
    keys=md(st+password.encode(),salt) # 第一次md5的结果加上原始key再进行一次md5
    key=st+keys # 32位的加密key由两次加密结果衔接得到
    iv=md(keys+password.encode(),salt) # 将得到的key再和原始key相加进行一次md5，得到偏移量iv
    result=dec(key,iv,data) # 使用加密key和iv进行解密
    return result

def test():
    unenc_data = 'the key is 42' # 原始数据
    password = 'the password' # 密钥
    enc_data = saltenc(unenc_data, password) #加密
    print(enc_data)
    dec_data = saltdec(enc_data, password) #解密
    print(dec_data)

if __name__=="__main__":
    test()
