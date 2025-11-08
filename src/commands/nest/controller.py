from src.core.command import Command


class NestController(Command):
    def execute(self, **kwargs):
        return super().execute(**kwargs)
    
    def construct(self, parent):
        return super().construct(parent)