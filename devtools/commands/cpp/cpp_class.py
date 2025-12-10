from devtools.core.command import Command
from devtools.core.io import die
from os import getcwd, makedirs, path, scandir
from devtools.core.decorators import abortable, requires
from devtools.core.lib import case_map
from devtools.templates.cpp.cpp_class import cpp_class_h, cpp_class_impl

class CppClass(Command):
    _name = 'class'
    _help = 'Create C++ class header and implementation files, relative to the project\'s CMakeLists.txt'
    
    @abortable
    @requires('path')
    def execute(self, **kwargs):
        dirname = getcwd()
        namespace = kwargs.get('namespace', None)
        relpath = path.relpath(path.abspath(kwargs.get('path')), dirname)
        no_impl = bool(kwargs.get('no_impl', False))
        enum = bool(kwargs.get('enum', False))

        if not path.exists(path.join(dirname, 'CMakeLists.txt')):
            die('Could not find a CMakeLists.txt file in current or parent directories.')

        if not path.exists(path.join(dirname, 'src'))  and not path.exists(path.join(dirname, 'Src')):
            makedirs(path.join(dirname, 'src'), exist_ok=True)
        if not path.exists(path.join(dirname, 'include'))  and not path.exists(path.join(dirname, 'Include')):
            makedirs(path.join(dirname, 'include'), exist_ok=True)

        names = case_map(path.basename(relpath))

        kwargs = {'names': names, 'enum': enum}

        if not namespace:
            items = list(scandir(path.join(dirname, 'include')))
            if len(items) == 1 and (ns := items[0]).is_dir():
                namespace = ns.name
        if namespace:
            kwargs['namespace'] = namespace



        class_h = cpp_class_h(**kwargs)
        fullpath_h = path.join(dirname, 'include', namespace or '', path.dirname(relpath))
        makedirs(fullpath_h, exist_ok=True)
        success_h = class_h.touch(at=fullpath_h)
        
        sucess_cpp = True

        if not no_impl and not enum:
            class_cpp = cpp_class_impl(**kwargs)
            fullpath_cpp = path.join(dirname, 'src', namespace or '', path.dirname(relpath))
            makedirs(fullpath_cpp, exist_ok=True)
            class_cpp.touch(at=fullpath_cpp)
            
        if success_h and sucess_cpp:
            die(f"Class '{names.pascal}' successfully created at {relpath}", fg='green', code = 0)
        else:
            die(f"There was a problem creating a class at {relpath}")

    def construct(self, parent):
        parser = super().construct(parent)
        parser.add_argument('path', help='Path to the class files to create, relative to the src/include folders')
        parser.add_argument(
            '--namespace',
            help='If set to a non-empty value, creates a namespace declaration to place the class in.'
        )
        parser.add_argument(
            '--no-impl',
            action='store_true',
            help='If set, creates only a header file, without the .cpp implementation file.'
        )
        parser.add_argument(
            '--enum',
            action='store_true',
            help='If set, creates only a header file, with an enum class declaration.'
        )
        parser.set_defaults(fn=self.execute)
        return parser