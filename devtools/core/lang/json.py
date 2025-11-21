import json
from dataclasses import dataclass
from json import JSONDecodeError
from os import getcwd, path
from devtools.core.lib import Serializable
from typing import Any, Literal, Optional, TypedDict

class PackageJsonBugsDict(TypedDict):
    url: Optional[str]
    email: Optional[str]

class PackageJsonPeopleDict(TypedDict):
    name: Optional[str]
    email: Optional[str]
    url: Optional[str]

class PackageJsonFundingDict(TypedDict):
    type: Optional[str]
    url: Optional[str]

class PackageJsonRepositoryDict(TypedDict):
    type: Optional[str]
    url: Optional[str]
    directory: Optional[str]

@dataclass
class PackageJson(Serializable):
    name: Optional[str] = None
    version: Optional[str] = None
    description: Optional[str] = None
    keywords: Optional[list[str]] = None
    type: Optional[Literal['commonjs', 'module']] = None
    homepage: Optional[str] = None
    bugs: Optional[str | PackageJsonBugsDict] = None
    license: Optional[str] = None
    author: Optional[str | PackageJsonPeopleDict] = None
    contributors: Optional[list[str | PackageJsonPeopleDict]] = None
    funding: Optional[str | PackageJsonFundingDict | list[str | PackageJsonFundingDict]] = None
    files: Optional[list[str]] = None
    exports: Optional[str | dict[str, str]] = None
    main: Optional[str] = None
    browser: Optional[str] = None
    module: Optional[str] = None
    bin: Optional[str | dict[str, str]] = None
    man: Optional[str | list[str]] = None
    repository: Optional[str | PackageJsonRepositoryDict] = None
    scripts: Optional[dict[str, str]] = None
    config: Optional[dict[str, Any]] = None
    dependencies: Optional[dict[str, str]] = None
    devDependencies: Optional[dict[str, str]] = None
    peerDependencies: Optional[dict[str, str]] = None
    peerDependenciesMeta: Optional[dict[str, dict[str, bool]]] = None
    bundleDependencies: Optional[dict[str, str]] = None
    optionalDependencies: Optional[dict[str, str]] = None
    overrides: Optional[dict[str, str]] = None
    engines: Optional[dict[str, str]] = None
    os: Optional[list[str]] = None
    cpu: Optional[list[str]] = None
    libc: Optional[str] = None
    devEngines: Optional[dict[str, Any]] = None
    private: Optional[bool] = None
    publishConfig: Optional[dict[str, Any]] = None
    workspaces: Optional[list[str] | dict[str, list[str]]] = None

    @staticmethod
    def find(at: str = getcwd()) -> str | None:
        cwd = path.abspath(at)
        while not path.abspath(cwd) == path.abspath(path.dirname(cwd)):
            package_json_path = path.join(cwd, 'package.json')
            if path.isfile(package_json_path):
                return package_json_path
            else:
                cwd = path.dirname(cwd)
        return None
    
    @staticmethod
    def load(filepath: str) -> PackageJson | None:
        if not path.isfile(filepath) or not path.getsize(filepath):
            return None
        with open(filepath, 'r', encoding='utf-8') as file:
            try:
                pkg_json_dict = json.load(file)
            except JSONDecodeError:
                return None
            else:
                return PackageJson.fromdict(pkg_json_dict)
                 

@dataclass
class CompilerOptions(Serializable):
    # Type Checking
    allowUnreachableCode: Optional[bool] = None
    allowUnusedLabels: Optional[bool] = None
    alwaysStrict: Optional[bool] = None
    exactOptionalPropertyTypes: Optional[bool] = None
    noFallthroughCasesInSwitch: Optional[bool] = None
    noImplicitAny: Optional[bool] = None
    noImplicitOverride: Optional[bool] = None
    noImplicitReturns: Optional[bool] = None
    noImplicitThis: Optional[bool] = None
    noPropertyAccessFromIndexSignature: Optional[bool] = None
    noUncheckedIndexedAccess: Optional[bool] = None
    noUnusedLocals: Optional[bool] = None
    noUnusedParameters: Optional[bool] = None
    strict: Optional[bool] = None
    strictBindCallApply: Optional[bool] = None
    strictBuiltinIteratorReturn: Optional[bool] = None
    strictFunctionTypes: Optional[bool] = None
    strictNullChecks: Optional[bool] = None
    strictPropertyInitialization: Optional[bool] = None
    useUnknownInCatchVariables: Optional[bool] = None

    # Modules
    allowArbitraryExtensions: Optional[bool] = None
    allowImportingTsExtensions: Optional[bool] = None
    allowUmdGlobalAccess: Optional[bool] = None
    baseUrl: Optional[str] = None
    customConditions: Optional[list[str]] = None
    module: Optional[Literal['none', 'commonjs', 'amd', 'umd', 'system', 'es6', 'es2015', 'es2020', 'es2022', 'esnext', 'node16', 'node18', 'node20', 'nodenext', 'preserve']] = None
    moduleResolution: Optional[Literal['classic', 'node10', 'node', 'node16', 'nodenext', 'bundler']] = None
    moduleSuffixes: Optional[list[str]] = None
    noResolve: Optional[bool] = None
    noUncheckedSideEffectImports: Optional[bool] = None
    paths: Optional[dict[str, list[str]]] = None
    resolveJsonModule: Optional[bool] = None
    resolvePackageJsonExports: Optional[bool] = None
    resolvePackageJsonImports: Optional[bool] = None
    rewriteRelativeImportExtensions: Optional[bool] = None
    rootDir: Optional[str] = None
    rootDirs: Optional[list[str]] = None
    typeRoots: Optional[list[str]] = None
    types: Optional[list[str]] = None

    # Emit
    declaration: Optional[bool] = None
    declarationDir: Optional[str] = None
    declarationMap: Optional[bool] = None
    downLevelIteration: Optional[bool] = None
    emitBOM: Optional[bool] = None
    emitDeclarationOnly: Optional[bool] = None
    importHelpers: Optional[bool] = None
    inlineSourceMap: Optional[bool] = None
    inlineSources: Optional[bool] = None
    mapRoot: Optional[str] = None
    newLine: Optional[Literal['lf', 'crlf']] = None
    noEmit: Optional[bool] = None
    noEmitHelpers: Optional[bool] = None
    noEmitOnError: Optional[bool] = None
    outDir: Optional[str] = None
    outFile: Optional[str] = None
    preserveConstEnums: Optional[bool] = None
    removeComments: Optional[bool] = None
    sourceMap: Optional[bool] = None
    sourceRoot: Optional[str] = None
    stripInternal: Optional[bool] = None

    # JavaScript Support
    allowJs: Optional[bool] = None
    checkJs: Optional[bool] = None
    maxNodeModuleJsDepth: Optional[int] = None

    # Editor Support
    disableSizeLimit: Optional[bool] = None
    plugins: Optional[list[dict[str, Any]]] = None

    # Interop Constraints
    allowSyntheticDefaultImports: Optional[bool] = None
    erasableSyntaxOnly: Optional[bool] = None
    esModuleInterop: Optional[bool] = None
    forceConsistentCasingInFileNames: Optional[bool] = None
    isolatedDeclarations: Optional[bool] = None
    isolatedModules: Optional[bool] = None
    preserveSymlinks: Optional[bool] = None
    verbatimModuleSyntax: Optional[bool] = None

    # Backwards Compatibility
    charset: Optional[str] = None
    importsNotUsedAsValues: Optional[Literal['remove', 'preserve', 'error']] = None
    keyofStringsOnly: Optional[bool] = None
    noImplicitUseStrict: Optional[bool] = None
    noStrictGenericChecks: Optional[bool] = None
    out: Optional[str] = None
    preserveValueImports: Optional[bool] = None
    suppressExcessPropertyErrors: Optional[bool] = None
    suppressImplicitAnyIndexErrors: Optional[bool] = None

    # Language and Environment
    emitDecoratorMetadata: Optional[bool] = None
    experimentalDecorators: Optional[bool] = None
    jsx: Optional[Literal['preserve', 'react', 'react-native', 'react-jsx', 'react-jsxdev']] = None
    jsxFactory: Optional[str] = None
    jsxFragmentFactory: Optional[str] = None
    jsxImportSource: Optional[str] = None
    lib: Optional[list[str]] = None
    libReplacement: Optional[bool] = None
    moduleDetection: Optional[Literal['legacy', 'auto', 'force']] = None
    noLib: Optional[bool] = None
    reactNamespace: Optional[str] = None
    target: Optional[Literal['es3', 'es5', 'es6', 'es2015', 'es2016', 'es2017', 'es2018', 'es2019', 'es2020', 'es2021', 'es2022', 'es2023', 'es2024', 'esnext']] = None
    useDefineForClassFields: Optional[bool] = None

    # Compiler Diagnostics
    diagnostics: Optional[bool] = None
    explainFiles: Optional[bool] = None
    extendedDiagnostics: Optional[bool] = None
    generateTrace: Optional[bool] = None
    listEmittedFiles: Optional[bool] = None
    listFiles: Optional[bool] = None
    noCheck: Optional[bool] = None
    traceResolution: Optional[bool] = None

    # Projects
    composite: Optional[bool] = None
    disableReferencedProjectLoad: Optional[bool] = None
    disableSolutionSearching: Optional[bool] = None
    disableSourceOfProjectReferenceRedirect: Optional[bool] = None
    incremental: Optional[bool] = None
    tsBuildInfoFile: Optional[str] = None

    # Output Formatting
    noErrorTruncation: Optional[bool] = None
    preserveWatchOutput: Optional[bool] = None
    pretty: Optional[bool] = None
    skipDefaultLibCheck: Optional[bool] = None
    skipLibCheck: Optional[bool] = None

@dataclass
class TSConfigJson(Serializable):
    files: Optional[list[str]] = None
    include: Optional[list[str]] = None
    exclude: Optional[list[str]] = None
    extends: Optional[str] = None
    references: Optional[list[dict[str, Any]]] = None
    compilerOptions: Optional[CompilerOptions] = None
