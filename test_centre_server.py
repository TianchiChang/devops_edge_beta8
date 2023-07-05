import sys
import ssl
import json
from sanic import Sanic
from sanic import Request, text
from sanic import response
from config import *
from common.salt import saltdec, saltenc

app = Sanic(__name__)

@app.websocket("/edge_login")
async def edge_login(request,ws):
    auth_data = await ws.recv()
    print(auth_data)
    target = json.loads(auth_data)["params"][1]
    dec_target = saltdec(target, pwd)
    origin = json.loads(auth_data)["params"][0]
    if dec_target==origin:
        await ws.send("success")
        while True:
            receive_data = await ws.recv()
            print(receive_data)
            # await ws.send(receive_data)
        
    
if __name__ == "__main__":
    app.run(host=cloud_host, port=int(cloud_port))