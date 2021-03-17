from aiohttp import web
import json

routes = web.RouteTableDef()

@routes.get('/')
async def hello(request):
    return web.Response(text=f"we are mixin' it!")


@routes.get('/output')
async def hello(request):
    params = request.rel_url.query
    gwid = params.get('id')

    if gwid is None:
        # cnt = await request.app['ctx']["cache"].getCnt()
        data = request.app['ctx']['cache'].data
        return web.Response(text=json.dumps(data))

    data = request.app['ctx']['cache'].item(gwid)
    # return web.Response(text=json.dumps())    
    return web.json_response(data)



