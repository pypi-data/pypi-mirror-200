"""ProgramConfig.

Program-based Application.
"""
import sys
import logging
from collections.abc import Callable
from aiohttp.web import middleware
from aiohttp.web_urldispatcher import SystemRoute
from aiohttp import web, hdrs
from asyncdb.exceptions import ProviderError, DriverError, NoDataFound
from navigator_session import get_session
from navigator.handlers.types import AppConfig
from navigator.responses import JSONResponse
from navigator.conf import (
    AUTH_SESSION_OBJECT
)
if sys.version_info < (3, 10):
    from typing_extensions import ParamSpec
else:
    from typing import ParamSpec
P = ParamSpec("P")




@middleware
async def program_session(request, handler):
    if isinstance(request.match_info.route, SystemRoute):  # eg. 404
        return await handler(request)
    # avoid authorization backend on excluded methods:
    if request.method == hdrs.METH_OPTIONS:
        return await handler(request)
    app = request.app
    program = app['program']
    program_slug = program.get_program()
    session = await get_session(request)
    try:
        user = session[AUTH_SESSION_OBJECT]
    except Exception as ex:
        raise web.HTTPUnauthorized(
            reason=f'NAV: Missing User Information: {ex}',
        ) from ex
    try:
        programs = user['programs']
    except (TypeError, KeyError, ValueError) as ex:
        print(ex)
        raise web.HTTPBadRequest(
            reason=f'Bad Session Information: {ex!s}'
        )
    if program_slug in programs:
        # TODO: sent a warning to empty PROGRAM AUTHORIZATION
        return await handler(request)
    else:
        try:
            if 'superuser' in user['groups']:
                pass
            elif not program_slug in user['programs']:
                raise web.HTTPUnauthorized(
                    reason=f'NAV: You are not authorized to see this Program: {program_slug}',
                )
        except Exception as err:
           logging.warning(f'Program Middleware: {err}')
        return await handler(request)


class ProgramConfig(AppConfig):
    _middleware: list = [program_session]
    template: str = '/templates'
    program_slug: str = ''
    enable_pgpool: bool = True

    def __init__(self, *args: P.args, **kwargs: P.kwargs):
        super(ProgramConfig, self).__init__(*args, **kwargs)
        self.app.router.add_get(
            '/authorize', self.app_authorization, name = f'{self.program_slug}_authorization'
        )

    async def app_authorization(self, request: web.Request) -> web.Response:
        session = await get_session(request)
        program_slug = self.program_slug
        # calculate the hierarchy:
        app = request.app
        try:
            user = session[AUTH_SESSION_OBJECT]
            user_id = user['user_id']
        except Exception as ex:
            raise web.HTTPUnauthorized(
                reason='NAV: Missing User Information: {ex}',
            ) from ex
        # try to know if the user has permission over this Program:
        try:
            if 'superuser' in user['groups']:
                pass
            elif not program_slug in user['programs']:
                raise web.HTTPUnauthorized(
                    reason=f'NAV: You are not authorized to see this Program: {program_slug}',
                )
        except KeyError:
            pass
        try:
            programs = user['programs']
        except (TypeError, KeyError) as err:
            raise web.HTTPBadRequest(
                reason=f'Missing Program information on User Session: {err!s}'
            )
        if program_slug in programs: # only if user has permission over this program:
            # using info:
            session['current_program'] = program_slug
            session[program_slug] = {
                "hierarchy": self.get_hierarchy
            }
            try:
                async with await app['database'].acquire() as conn:
                    sql = f"SELECT get_filtering_fixed FROM {program_slug}.get_filtering_fixed({user_id}, '{program_slug}')"
                    print('SQL IS: ', sql)
                    result, error = await conn.queryrow(sql)
                    if not result:
                        del session[program_slug]['hierarchy_filtering']
                    if error:
                        raise web.HTTPBadRequest(
                            reason=f'Bad Auth Request: {error!s}'
                        )
                    if result and not error:
                        session[program_slug]['hierarchy_filtering'] = result['get_filtering_fixed']
            except Exception as e:
                raise web.HTTPBadRequest(
                    reason=f'Bad Auth Request: {e!s}'
                )
            return JSONResponse({
                    "status": "User Authorized",
                    "id": user_id,
                    "program": self.program_slug,
                    "hierarchy_filtering": session[program_slug]['hierarchy_filtering']
                    # "session": info
                },
                status=200
            )
        else:
            raise web.HTTPUnauthorized(
                reason=f'NAV: You are not authorized to see this Program: {program_slug}',
            )

    @property
    def get_hierarchy(self):
        return self.hierarchy

    def get_program(self):
        return self.program_slug

    def get_program_id(self):
        return self.program_id

    async def app_startup(self, app: web.Request, connection: Callable):
        pool = app['database']
        try:
            async with await pool.acquire() as conn:
                sql = f"SELECT program_slug, program_id, orgid, array_agg(field) as hierarchy FROM {self._name}.vw_hierarchy GROUP BY program_slug, program_id, orgid"
                try:
                    result = await conn.fetch_one(sql)
                    self.program_id = result['program_id']
                    self.program_slug = result['program_slug']
                    self.hierarchy = result['hierarchy']
                    # TODO: also add on a LIST of program hierarchies.
                except NoDataFound:
                    pass
        except (ProviderError, DriverError) as ex:
            logging.exception(f'Error on Program: {ex}', stack_info=True)
        logging.debug(f'PROJECT STARTED {self._name}')

    async def on_startup(self, app):
        await super(ProgramConfig, self).on_startup(app)
        app['program'] = self


    async def on_shutdown(self, app):
        await super(ProgramConfig, self).on_shutdown(app)
        logging.debug(f'ON SHUTDOWN {self._name}')
