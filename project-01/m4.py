from aiohttp import web
import aiofiles
import os

routes = web.RouteTableDef()

async def create_file(element, index, name):
    try:    
            if(index < 9):
                async with aiofiles.open(f'gatherData/0{index+1}-{name}.txt', 'w') as f:
                    await f.write(str(element))
            else:
                async with aiofiles.open(f'gatherData/{index+1}-{name}.txt', 'w') as f:
                    await f.write(str(element))
    except Exception as e:
        return e

@routes.post("/gatherdata")
async def get_links(request):
    try:
        data = await request.json()

        if(len(data) > 10):
            for index, el in enumerate(data):
                name = el.get("username")
                print(index, el)
                await create_file(el, index, name)
        
        return web.json_response({"status":"ok", "recivedData":data}, status=200)
    except Exception as e:
        return web.json_response({"status":"error", "response":e}, status=500)

app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port=7003)