from devtools.core.lang.json import CompilerOptions, TSConfigJson
from devtools.core.template import Template

def tsconfig_node() -> Template:
    return Template(
        filename='tsconfig.json',
        contents = TSConfigJson(
            compilerOptions=CompilerOptions(
                module='nodenext',
                moduleResolution='nodenext',
                resolvePackageJsonExports=True,
                esModuleInterop=True,
                isolatedModules=True,
                declaration=True,
                removeComments=True,
                emitDecoratorMetadata=True,
                experimentalDecorators=True,
                allowSyntheticDefaultImports=True,
                target='ES2023',
                sourceMap=True,
                outDir='dist',
                baseUrl='.',
                incremental=True,
                skipLibCheck=True,
                strictNullChecks=True,
                forceConsistentCasingInFileNames=True,
                noImplicitAny=False,
                strictBindCallApply=False,
                noFallthroughCasesInSwitch=False,
                useDefineForClassFields=False
            )
        ).todict()
    )

def tsconfig_deno() -> Template:
    return Template(
        filename='tsconfig.json',
        contents = TSConfigJson(
            include=['src'],
            compilerOptions=CompilerOptions(
                target='esnext',
                module='esnext',
                moduleResolution='nodenext',
                experimentalDecorators=True,
                emitDecoratorMetadata=True,
                strict=True,
                noEmit=True,
                esModuleInterop=True,
                skipLibCheck=True,
                useDefineForClassFields=False
            ),
            exclude=['node_modules', 'dist']
        ).todict()
    )

def tsconfig_bun() -> Template:
        return Template(
        filename='tsconfig.json',
        contents = TSConfigJson(
            include=['src'],
            compilerOptions=CompilerOptions(
                target='esnext',
                module='esnext',
                moduleResolution='bundler',
                esModuleInterop=True,
                experimentalDecorators=True,
                emitDecoratorMetadata=True,
                strict=True,
                noEmit=True,
                skipLibCheck=True,
                baseUrl='.',
                paths = {
                    '@/*': ['src/*'],
                }
            ),
            exclude=['node_modules', 'dist']
        ).todict()
    )