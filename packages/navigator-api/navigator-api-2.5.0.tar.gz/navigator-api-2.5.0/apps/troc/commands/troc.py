from navigator.commands import BaseCommand, CommandError

class TrocCommand(BaseCommand):
    help = 'Enviroment Commands for Navigator'

    def hello(self, options, **kwargs):
        """
        Print a simple Hello world
        """
        self.write('Hello World', level='NOTICE')
