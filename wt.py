import aiohttp
import asyncio
from aiohttp import web

routes = web.RouteTableDef()

@routes.post("/passdata")
async def get_links(request):
    try:
        data = await request.json()
        res = []
        for i in data:
            checkFirstLetterW = data[i].get("username").startswith("w")
            checkFirstLetterD = data[i].get("username").startswith("d")
            if(checkFirstLetterW):
                res.append(data[i])
            if(checkFirstLetterD):
                res.append(data[i])
                
        async with aiohttp.ClientSession() as session:
            async with session.post("http://localhost:7003/gatherdata", json = res) as res:
                result = await res.json()
        return web.json_response({"status":"ok","passedFirstLetters": result.get("recivedData"),"recivedDataFromM0":data}, status=200)
    except Exception as e:
        return web.json_response({"status":"error", "response":e}, status=500)

app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port=7002)