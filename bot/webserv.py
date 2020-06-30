from aiohttp import web
import asyncio
import requests
import os
from subprocess import Popen


async def handle(request):
    ## here how to get query parameters
    param1 = request.rel_url.query['osuid']
    param2 = request.rel_url.query['disid']
    print(param1)
    print(param2)
    result = "osuid: {}, disid: {}".format(param1, param2)
    Popen(['python3 runauth.py -o' + param1 + " -d " + param2], shell=True) 
    return web.Response(text=str(result))
    exit()

app = web.Application()

app.add_routes([web.get('/', handle),
                web.get('/{name}', handle)])

if __name__ == '__main__':
    web.run_app(app, port=5001)
