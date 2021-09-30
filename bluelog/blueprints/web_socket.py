# coding:utf-8
import json
from bluelog.utils.extensions import sockets
from flask import current_app
ws_pool = []


@sockets.route('/echo')
def echo_sockets(ws):
    r_data = ws.receive()
    r_data = json.loads(r_data)
    if not r_data['type'] == 'open':
        return
    name = r_data['data']['name']
    for e in ws_pool:
        try:
            e.send(json.dumps({'type':'enter','data':{'name':name}}))
        except:
            ws_pool.remove(e)
    ws_pool.append(ws)

    while not ws.closed:
        r_data = ws.receive()
        if r_data is None:
            break

        # ws.send("客户端已收到："+str(message))
        # 如何推送给他人
        r_data = json.loads(r_data)
        if r_data['type'] == 'say':
            data = r_data['data']
            for e in ws_pool:
                if e == ws:
                    continue
                e.send(json.dumps({'type':'say','data':{'name':name,'content':data['content']}}))
    ws_pool.remove(ws)
    for e in ws_pool:
        e.send(json.dumps({'type':'leave','data':{'name':name}}))



