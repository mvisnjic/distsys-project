
import asyncio
import aiohttp
import random
from aiohttp import web
import logging

routes = web.RouteTableDef()

M = 1000
maxNum = 10000
N = random.randint(5, 10) # number of workers
print("Number of workers", N)

workers = {"id" + str(id) : [] for id in range(1, N+1)}
print("Workers:", workers)

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

@routes.get("/")
async def get_function(req):
    try:
        tasks = []
        res = []

        logging.info(received_requests / maxNum)
        received_requests += 1
        data = [await x.json() for x in data]
        data = data[0]
        res = data.get("data")
        print(res)
        return web.json_response({"status":"ok"}, status=200)
    except Exception as e:
        return web.json_response({"failed":str(e)}, status=500)

app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port=7000)
