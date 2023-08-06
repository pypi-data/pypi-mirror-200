from navigator.commands import BaseCommand

class HelloCommand(BaseCommand):
    help = 'Enviroment Commands for Navigator'

    def configure(self):
        pass

    def say_hello(self, options, *args, **kwargs):
        """
        Print a simple Hello world
        """
        self.write('Hello World', level='DEBUG')
