from core.io import style
from typing import Any

def tostring(data: Any, indent: int = 0) -> str:
    tab = ' ' * (4 * indent)
    lines = []

    if isinstance(data, dict):
        for name, value in data.items():
            lines.append(
                tab + style(f"{name}:", fg='white', end='\n' if isinstance(value, (dict, list, tuple, set)) else ' ') +
                (tostring(value, indent + 1) if isinstance(value, (dict, list, tuple, set)) else tostring(value))
            )
    elif isinstance(data, (list, tuple, set)):
        for item in data:
            lines.append(
                tab + style('-', fg='white', end='\n' if isinstance(item, (dict, list, tuple, set)) else ' ') +
                (tostring(item, indent + 1) if isinstance(item, (dict, list, tuple, set)) else tostring(item))
            )
    elif isinstance(data, str):
        return style(f"'{data}'", fg='green')
    elif data is None:
        return style('None', fg='gray')
    else:
        return style(str(data), fg='yellow')

    return '\n'.join(lines)

print(tostring({
    "name": "my-project",
    "version": "1.0.0",
    "description": "A sample project",
    "main": "index.js",
    "scripts": {
        "start": "node index.js",
        "dev": "bun run dev",
        "build": "bun run build",
        "test": "bun test"
    },
    "keywords": ["example", "project", "bun", "node"],
    "author": "Your Name",
    "license": "MIT",
    "dependencies": {
        "react": "^18.2.0",
        "react-dom": "^18.2.0"
    },
    "devDependencies": {
        "typescript": "^5.6.3",
        "@types/react": "^18.2.28",
        "@types/react-dom": "^18.2.14"
    }
}))
