import asyncio
import aiohttp
import time
from env import *
# from random import randint # temp


# URL1='https://dx-api-ru1.thingpark.com/core/latest/api/baseStations?healthState=ACTIVE&connectionState=CNX&statistics=true&commercialDetails=true'
# URL2 = 'http://172.17.0.1:8083/api/monitoring/gateways/actility_styled'

HDRS1 = {'Accept': 'application/json', 'Authorization' : AUTH1 }
HDRS2 = {'Accept': 'application/json', 'Authorization' : AUTH2 }

async def http_clients(ctx):
    ctx['logger'].info(f'http clients have been started. Requests every {REQUEST_TIME} seconds ...')
    await asyncio.gather(
        http_client(ctx=ctx,master=False,url=URL1,headers=HDRS1),
        http_client(ctx=ctx,master=True, url=URL2,headers=HDRS2)
    )

async def http_client(ctx,master,**kwargs):
    log = ctx['logger']
    while True:
        start = time.time()
        log.debug('[http-client] opening session GET:{}'.format(kwargs['url']))

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(**kwargs) as resp:
                    if resp.status in range(200,300):
                        d = await resp.json()
                        # print(d)
                        log.debug('[http-client] finished GET: {} (code:{})! took: {} seconds'.format(kwargs['url'],resp.status,time.time()-start))
                        try:
                            ctx["cache"].save_data(d,master)
                        except Exception as e:
                            log.error(e)
                    else:
                        log.error('[http-client] error GET: {} (code:{})! took: {} seconds'.format(kwargs['url'],resp.status,time.time()-start))
        except Exception as e:
            log.error('[http-client] unable to get url {} error: {} '.format(kwargs['url'],e))
        
        log.debug('-------------------------------------')
        # return res
        await asyncio.sleep(REQUEST_TIME)