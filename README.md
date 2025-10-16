# DevTools CLI

devtools_cli/
│
├── cli.py                     # Entry point for the CLI (main parser and dispatcher)
├── __init__.py
│
├── core/                      # Core framework (independent of specific commands)
│   ├── __init__.py
│   ├── file.py                # File abstraction (create, delete, check, etc.)
│   ├── command.py             # Command base class (construct + execute)
│   ├── template.py            # Template base class (create file contents)
│   ├── decorators.py          # Decorators (for AOP-like behavior)
│   ├── io.py                  # IO and terminal interface (colors, input, etc.)
│   └── utils.py               # Shared utilities (string formatting, paths, etc.)
│
├── commands/                  # CLI subcommands
│   ├── __init__.py
│   ├── init.py                # Example command: `devtools init`
│   ├── generate.py            # Example command: `devtools generate`
│   └── ...                    # Additional commands
│
├── templates/                 # Default file templates
│   ├── __init__.py
│   ├── base_template.py
│   ├── controller_template.py
│   └── ...
│
├── tests/                     # Unit tests
│   ├── test_file.py
│   ├── test_command.py
│   ├── test_template.py
│   └── ...
│
├── pyproject.toml             # Project metadata and dependencies
└── README.md
