from abc import ABC, abstractmethod
from os import linesep
from typing import Literal, TypedDict


class DocStringValues(TypedDict):
    description: str | None
    params: list[tuple[str, Literal['int', 'float', 'str', 'bool'] | str]]
    returns: Literal['int', 'float', 'str', 'bool'] | str
    raises: list[str]

class PythonDocstring(ABC):
    @staticmethod
    @abstractmethod
    def generate(values: DocStringValues) -> str:
        pass

class ReSTDocstring(PythonDocstring):
    @staticmethod
    def generate(values: DocStringValues) -> str:
        # Stubbed ruleset-generated values
        quotes = '"'

        docstring = []
        docstring.append(quotes * 3)
        if (description := values.get('description')) is not None:
            docstring.append(description)
        else:
            docstring.append(f"(Describe your class, method or function here)")
        docstring.append('')
        for param in values.get('params', []):
            name, type = param
            docstring.append(f":param {name}:")
            docstring.append(f":type {name}: {type}")
        if (returns := values.get('returns')) is not None:
            docstring.append(f":return:")
            docstring.append(f":rtype: {returns}")
        for exception in values.get('raises', []):
            docstring.append(f":raises {exception}:")
        docstring.append(quotes * 3)
        return linesep.join(docstring)

class GoogleDocstring(PythonDocstring):
    @staticmethod
    def generate(values: DocStringValues) -> str: 
        # Stubbed ruleset-generated values
        quotes = '"'
        indent = ' ' * 4

        docstring = []
        docstring.append(quotes * 3)
        if (description := values.get('description')) is not None:
            docstring.append(description)
        else:
            docstring.append(f"(Describe your class, method or function here)")
        if (params := values.get('params', [])):
            docstring.append('')
            docstring.append('Args:')
            for param in params:
                name, type = param
                docstring.append(f"{indent}{name} ({type}):")
        if (returns := values.get('returns')) is not None:
            docstring.append('')
            docstring.append('Returns:')
            docstring.append(f"{indent}{returns}:")
        if (raises := values.get('raises', [])):
            docstring.append('')
            docstring.append('Raises:')
            for exception in raises:
                docstring.append(f"{indent}{exception}:")
        docstring.append(quotes * 3)
        return linesep.join(docstring)

class NumPyDocstring(PythonDocstring):
    @staticmethod
    def generate(values: DocStringValues) -> str: 
        # Stubbed ruleset-generated values
        quotes = '"'
        indent = ' ' * 4

        docstring = []
        docstring.append(quotes * 3)
        if (description := values.get('description')) is not None:
            docstring.append(description)
        else:
            docstring.append(f"(Describe your class, method or function here)")
        if (params := values.get('params', [])):
            docstring.append('')
            param_title = 'Parameters'
            docstring.append(param_title)
            docstring.append('-' * len(param_title))
            for param in params:
                name, type = param
                docstring.append(f"{name}: {type}")
                docstring.append(indent)
        if (returns := values.get('returns')) is not None:
            return_title = 'Returns'
            docstring.append('')
            docstring.append(return_title)
            docstring.append('-' * len(return_title))
            docstring.append(returns)
            docstring.append(indent)
        if (raises := values.get('raises', [])):
            except_title = 'Raises'
            docstring.append('')
            docstring.append(except_title)
            docstring.append('-' * len(except_title))
            for exception in raises:
                docstring.append(f"{exception}")
                docstring.append(indent)
        docstring.append(quotes * 3)
        return linesep.join(docstring)


print(GoogleDocstring.generate({ 'description': 'Greets the user', 'params': [ ('name', 'str'), ('age', 'int') ], 'returns': 'str', 'raises': ['ValueError'] }))