import aiohttp
import asyncio
from aiohttp import web

routes = web.RouteTableDef()

@routes.get("/go")
async def get_links(request):
    try:
        resDict = {}    
        async with aiohttp.ClientSession() as session:
            task = asyncio.create_task(session.get("http://localhost:7000/getlinks"))
            data = await asyncio.gather(task)
            data = [await x.json() for x in data]
            data = data[0]
            res = data.get("data")
            
            for row in res:
                resDict[res.index(row)] = row
            
            async with session.post("http://localhost:7002/passdata", json = resDict) as res:
                result = await res.json()
        return web.json_response(result, status=200)
    except Exception as e:
        return web.json_response({"status":"error", "response":e}, status=500)

app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port=7001)