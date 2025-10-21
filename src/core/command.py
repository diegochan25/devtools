from abc import ABC, abstractmethod
import argparse

class Command(ABC):
    _name: str
    _help: str

    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def help(self) -> str:
        return self._help
    
    @help.setter
    def help(self, value: str) -> None:
        self._help = value 
    
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def construct(self, parent: argparse._SubParsersAction) -> argparse.ArgumentParser:
        return parent.add_parser(self._name, help=self._help)