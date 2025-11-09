from abc import ABC, abstractmethod
from os import linesep
from typing import Literal

class PythonDocstring(ABC):
    @staticmethod
    @abstractmethod
    def generate(
        description: str | None = None,
        params: list[dict[str, Literal['int', 'float', 'bool', 'str'] | str]] | None = None,
        returns: Literal['int', 'float', 'bool', 'str'] | None = None,
        raises: list[str] | None = None
    ) -> str:
        pass

class ReSTDocstring(PythonDocstring):
    @staticmethod
    def generate(
        description: str | None = None,
        params: list[dict[str, Literal['int', 'float', 'bool', 'str'] | str]] | None = None,
        returns: Literal['int', 'float', 'bool', 'str'] | None = None,
        raises: list[str] | None = None
    ) -> str:
        from src.config.rule_set import PythonRules 
        rules = PythonRules.generate()

        docstring = []
        docstring.append(rules.q * 3)
        if description is not None:
            docstring.append(description)
        else:
            docstring.append(f"(Describe your class, method or function here)")
        docstring.append('')
        if params is not None and len(params):
            for param in params:
                name, type = param
                docstring.append(f":param {name}:")
                docstring.append(f":type {name}: {type}")
        if returns is not None:
            docstring.append(f":return:")
            docstring.append(f":rtype: {returns}")
        if raises is not None and len(raises):
            for exception in raises:
                docstring.append(f":raises {exception}:")
        docstring.append(rules.q * 3)
        return linesep.join(docstring)

class GoogleDocstring(PythonDocstring):
    @staticmethod
    def generate(
        description: str | None = None,
        params: list[dict[str, Literal['int', 'float', 'bool', 'str'] | str]] | None = None,
        returns: Literal['int', 'float', 'bool', 'str'] | None = None,
        raises: list[str] | None = None
    ) -> str: 
        from src.config.rule_set import PythonRules 
        rules = PythonRules.generate()

        docstring = []
        docstring.append(rules.q * 3)
        if description is not None:
            docstring.append(description)
        else:
            docstring.append(f"(Describe your class, method or function here)")
        if params is not None and len(params):
            docstring.append('')
            docstring.append('Args:')
            for param in params:
                name, type = param
                docstring.append(f"{rules.t}{name} ({type}):")
        if returns is not None:
            docstring.append('')
            docstring.append('Returns:')
            docstring.append(f"{rules.t}{returns}:")
        if raises is not None and len(raises):
            docstring.append('')
            docstring.append('Raises:')
            for exception in raises:
                docstring.append(f"{rules.t}{exception}:")
        docstring.append(rules.q * 3)
        return linesep.join(docstring)

class NumPyDocstring(PythonDocstring):
    @staticmethod
    def generate(
        description: str | None = None,
        params: list[dict[str, Literal['int', 'float', 'bool', 'str'] | str]] | None = None,
        returns: Literal['int', 'float', 'bool', 'str'] | None = None,
        raises: list[str] | None = None
    ) -> str: 
        from src.config.rule_set import PythonRules 
        rules = PythonRules.generate()

        docstring = []
        docstring.append(rules.q * 3)
        if description is not None:
            docstring.append(description)
        else:
            docstring.append(f"(Describe your class, method or function here)")
        if params is not None and len(params):
            docstring.append('')
            param_title = 'Parameters'
            docstring.append(param_title)
            docstring.append('-' * len(param_title))
            for param in params:
                name, type = param
                docstring.append(f"{name}: {type}")
                docstring.append(rules.t)
        if returns is not None:
            return_title = 'Returns'
            docstring.append('')
            docstring.append(return_title)
            docstring.append('-' * len(return_title))
            docstring.append(returns)
            docstring.append(rules.t)
        if raises is not None and len(raises):
            except_title = 'Raises'
            docstring.append('')
            docstring.append(except_title)
            docstring.append('-' * len(except_title))
            for exception in raises:
                docstring.append(f"{exception}")
                docstring.append(rules.t)
        docstring.append(rules.q * 3)
        return linesep.join(docstring)