"""
Program Init.

worp Program.
"""
from aiohttp import hdrs
from aiohttp.web import middleware
from aiohttp.web_urldispatcher import SystemRoute

from resources.program import ProgramConfig


@middleware
async def app_session(request, handler):
    user_id = None
    if isinstance(request.match_info.route, SystemRoute):  # eg. 404
        return await handler(request)
    # avoid authorization backend on excluded methods:
    if request.method == hdrs.METH_OPTIONS:
        return await handler(request)
    return await handler(request)


class worp(ProgramConfig):
    # class worp(AppConfig):
    __version__ = "0.0.1"
    app_description = """
    API for worp
    """
    _middleware: list = [app_session]
