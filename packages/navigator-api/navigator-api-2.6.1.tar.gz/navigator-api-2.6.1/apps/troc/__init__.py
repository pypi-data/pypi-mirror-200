import logging
from navigator.handlers.types import AppConfig
from navigator.views import load_models

class troc(AppConfig):
    __version__ = '0.0.1'
    app_description = """
    API for TROC
    """
    template = '/templates'
    domain = 'troc.*'
    enable_pgpool: bool = True

    async def app_startup(self, app, connection):
        await super(troc, self).app_startup(app, connection)
        try:
            mdl = __import__('apps.troc.models', fromlist=['*'])
            models = getattr(mdl, 'MODELS')
            # get the table list:
            tables = getattr(mdl, 'TABLES')
            if tables:
                print('::: STARTING LOADING MODELS ::: ')
                models = await load_models(app, models, tables)
        except ImportError as err:
            print(err)
        except Exception as err:
            print(err)
            logging.error(f'TROC APP: Error connecting to Database: {err!s}')

    async def on_shutdown(self, app):
        await super(troc, self).on_shutdown(app)
        print('ON SHUTDOWN TROC')
