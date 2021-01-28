from aiohttp import web
import asyncio
from http_clients import *
from cache import *
import logging
from routes import routes
from env import *


def init_app():
    app = web.Application()
    app.add_routes(routes)
    return app

def init_context():
    result = {}
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('[:PANTIES:]')
    logger.info('the service forwards http data from two urls')

    result['cache'] = Cache(logger,ttl=REQUEST_TIME+60)
    result['logger'] = logger

    return result


async def main():
    ctx = init_context()
    app = init_app()

    app['ctx'] = ctx

    # asyncio.create_task()
    asyncio.create_task(http_clients(ctx), name='http_clients')

    runner = aiohttp.web.AppRunner(app)
    await runner.setup()
    site = aiohttp.web.TCPSite(runner)    
    await site.start()    

    # wait forever
    await asyncio.Event().wait()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    print('\nBye!')
    