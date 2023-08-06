from aiohttp import web
from datetime import datetime
from asyncdb.models import Model
from typing import (
    Dict
)
from navconfig.logging import logging
from asyncdb.providers.pg import pg
from navigator.conf import default_dsn


async def last_login(request: web.Request, user: Model, userdata: Dict, **kwargs):
    print('::: Calling last Login ::: ')
    logging.debug(f'User was logged in: {user.username}')
    # making a connection, then, saving the last login to user.
    try:
        db = pg(dsn=default_dsn)
        async with await db.connection() as conn:
            user.Meta.set_connection(conn)
            user.last_login = datetime.now()
            await user.save()
    except Exception as e:
        logging.exception(e, stack_info=True)
    finally:
        db = None



async def saving_troc_user(request: web.Request, user: Model, userdata: Dict, **kwargs):
    print(' ::: Calling TROC User ::: ')
