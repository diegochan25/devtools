from Command import Command
from util.decorators import abortable, requires

class NestController(Command):
    def __init__(self):
        super().__init__()
    
    @abortable
    @requires('path')
    def execute(self, **kwargs):
        path: str = kwargs.get('path') 
        flat: bool = kwargs.get('flat', False)
        pass

    def construct(self):
        # argparse logic here
        pass


