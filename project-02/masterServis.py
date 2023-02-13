
import asyncio
import aiohttp
import random
from aiohttp import web
import logging

routes = web.RouteTableDef()

N = random.randint(5, 10) # number of workers
print("Number of workers", N)

workers = {"id" + str(id) : [] for id in range(1, N+1)}
print("Workers:", workers)

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

recivedRequests = 0
M = 1000
sendTask = 0
completedTasks = 0
currWorker = 1
@routes.get("/")
async def get_function(req):
    try:
        global recivedRequests
        global currWorker
        global sendTask
        global completedTasks
        max_number = 10000
        tasks = []
        res = []
        data = await req.json()
        recivedRequests += 1
        logging.info(f"Received new request: {recivedRequests} / {max_number}")
        dataCodes = data.get("codes")
        dataDict = {i:code for i,code in enumerate(dataCodes)}
        
        async with aiohttp.ClientSession() as session:
            for index,elem in dataDict.items():
                tasks.append(asyncio.create_task(session.get(f"http://localhost:{7000 + currWorker}/", json = {"client": index, "codes": elem})))
                workers["id" + str(currWorker)].append(tasks)
                sendTask += 1 
                if(currWorker == N):
                    currWorker = 1
                else:
                    currWorker += 1
                logging.info(f"Sending: {sendTask} / {recivedRequests}")
                
                    
            res = await asyncio.gather(*tasks)
            res = [await x.json() for x in res]        
            if(res):
                completedTasks += 1
                logging.info(f"Completed tasks: {completedTasks}")
            # print(workers)        
        return web.json_response({"status":"ok", "res": res}, status=200)
    except Exception as e:
        return web.json_response({"failed": str(e)}, status=500)

app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port=6000)
