import aiosqlite
import asyncio
from aiohttp import web

import pandas as pd

routes = web.RouteTableDef()

df = pd.read_json("file-040.json", lines=True, nrows=10000)

async def fill_db():
    try:
        async with aiosqlite.connect("data.db") as db:
            for _, row in df.iterrows():
                    username = row["repo_name"].split("/")[0]
                    repo = row["repo_name"]
                    path = row["path"]
                    size = row["size"]
                    line_max = row["line_max"]
                    copies = row["copies"]
                        
                    await db.execute("CREATE TABLE IF NOT EXISTS data(username,repo,path,size,line_max,copies)")
                    await db.execute("INSERT INTO data (username,repo,path,size,line_max,copies) VALUES (?,?,?,?,?,?)", (username,repo,path,size,line_max,copies))    
            await db.commit()
        return "Successfully filled the database!"
    except Exception as e:
        return "ERROR: ", str(e)

async def check_db(): 
    async with aiosqlite.connect("data.db") as db:
        async with db.execute("SELECT COUNT(*) FROM sqlite_schema;") as cur:
            async for row in cur:
                if(row[0] == 0):
                    print("Database is empty, filling...")
                    re = await fill_db()
                    return re
            await db.commit()
        return "Database is already filled!"

check_db = asyncio.run(check_db())
print(check_db)

@routes.get("/getlinks")
async def get_links(request):
    try:    
        res = []
        resDict = {}
        async with aiosqlite.connect("data.db") as db:
            async with db.execute("SELECT * FROM data LIMIT 100;") as cur:
                async for row in cur:
                    if(row[0] == 0):
                        return "Database is empty!"
                    
                    colNames = tuple(map(lambda x: x[0], cur.description))
                    namesAndRows = colNames + row
                    resDict.update({namesAndRows[0]:namesAndRows[6]})
                    resDict.update({namesAndRows[1]:namesAndRows[7]})
                    resDict.update({namesAndRows[2]:namesAndRows[8]})
                    resDict.update({namesAndRows[3]:namesAndRows[9]})
                    resDict.update({namesAndRows[4]:namesAndRows[10]})
                    resDict.update({namesAndRows[5]:namesAndRows[11]})
                    res.append(resDict.copy())
                await db.commit()
        return web.json_response({"status":"ok", "data":res}, status=200)
    except Exception as e:
        return web.json_response({"status":"error", "response":e}, status=500)

app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port=7000)