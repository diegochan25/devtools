from abc import abstractmethod
from argparse import _SubParsersAction, ArgumentParser

class Command:
    _name: str
    _help: str

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def help(self) -> str:
        return self._help
    
    @abstractmethod
    def execute(self, **kwargs) -> None:
        pass

    def construct(self, parent: _SubParsersAction) -> ArgumentParser | _SubParsersAction:
        parser = parent.add_parser(name=self._name, help=self._help)
        return parser