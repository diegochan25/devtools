from os import path
from src.core.command import Command
from src.core.decorators import abortable, requires
from src.core.io import die
from src.core.js import JS

class NestController(Command):
    
    @abortable
    @requires('path')
    def execute(self, **kwargs):
        super().execute()
        rel_path = kwargs.get('path')

        package_json_path = JS.find_package_json()
        if package_json_path is None:
            die('Could not find a package.json file in current or parent directories.')
        package_json = JS.load_package_json(package_json_path)

        if package_json is None:
            die(f"Unable to parse contents of file at {package_json_path} to JSON.")
        
        entry_point = package_json.main or package_json.module

        if not entry_point:
            die('Entry point not specified in package.json')
        
        file_path = path.join(path.dirname(package_json_path), path.dirname(entry_point), rel_path)
        print(file_path)
        

            

    def construct(self):
        super().construct()


NestController().execute(path='user/user-profile')

