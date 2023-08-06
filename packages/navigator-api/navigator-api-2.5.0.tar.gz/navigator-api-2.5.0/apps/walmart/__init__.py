"""
Program Init.

Walmart Program.
"""
from resources.program import ProgramConfig

class walmart(ProgramConfig):
    __version__ = '0.0.1'
    app_description = """
    API for Walmart
    """
    template = '/templates'

    async def on_startup(self, app):
        await super(walmart, self).on_startup(app)
        print('ON STARTUP Walmart')

    async def on_shutdown(self, app):
        await super(walmart, self).on_shutdown(app)
        print('ON SHUTDOWN Walmart')
