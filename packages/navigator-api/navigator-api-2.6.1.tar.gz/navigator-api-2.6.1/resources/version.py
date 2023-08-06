"""version.

Extract the version of all required packages and showed in a response.
"""
import importlib

from asyncdb.utils import cPrint

from navigator.responses import JSONResponse
from navigator.types import HTTPRequest

package_list = ('asyncdb', 'notify', 'datamodel', 'navconfig', 'navigator', 'navigator_auth', 'navigator_session')


async def get_versions(request: HTTPRequest):
    """
    ---
    summary: Return version of all required packages
    tags:
    - version
    produces:
    - application/json
    responses:
        "200":
            description: list of packages and versions.
    """
    versions = {}
    cPrint('RUNNING VERSION')
    for package in package_list:
        mdl = importlib.import_module(f'{package}.version', package='version')
        obj = getattr(mdl, '__version__')
        versions[package] = obj
    return JSONResponse(versions, status=200)
