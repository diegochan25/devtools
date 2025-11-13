from src.core.command import Command


class NestController(Command):
    _name = 'controller'
    _help = 'Create a new NestJS controller file'

    def execute(self, **kwargs):
        return super().execute(**kwargs)
    
    def construct(self, parent):
        return super().construct(parent)