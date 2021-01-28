from aiohttp import web
import json

routes = web.RouteTableDef()

@routes.get('/')
async def hello(request):
    return web.Response(text=f"we are mixin' it!")


@routes.get('/output')
async def hello(request):
    # cnt = await request.app['ctx']["cache"].getCnt()
    data = request.app['ctx']["cache"].data
    return web.Response(text=json.dumps(data))
    #return web.Response(text=f"mixin' it {cnt}")
