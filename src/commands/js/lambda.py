from importlib.metadata import requires
from src.core.command import Command

class JSLambda(Command):

    @requires('path')
    def execute(self, **kwargs):
        path: str = kwargs.get('path')
        

    def construct(self, parent):
        parser = super().construct(parent)
        parser.add_argument('path', help='The path where the lambda function should be created. The last component of the path will be used for the function name')
        parser.set_defaults(fn=self.execute)
        return parser