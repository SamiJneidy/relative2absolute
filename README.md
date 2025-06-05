# relative2absolute

**relative2absolute** is a Python tool that converts relative import statements into absolute ones based on a specified root directory. It is especially useful for refactoring Python projects to follow absolute import best practices.

## Features

- Converts relative imports (e.g., `from ..core import database`) to absolute imports (e.g., `from package.app.core import database`)
- Allows specifying the root path where absolute imports should start
- Supports nested directories
- Will not affect any existing absolute imports
- Command-line interface with pip installation support

## Description

This tool converts relative imports to absolute imports based on a root package specified via the --root argument. It recursively parses every module and subpackage within the root package and modifies any relative import it finds to an absolute import that begins from the root package.

If a module contains a relative import with a level (i.e., number of .) that exceeds the number of package levels between the root and that module, an error will be raised.

## Installation

Install the tool using pip:

```bash
pip install relative2absolute
```

## Usage

Run the tool from the command line by specifying the path to the directory or file to convert, along with the `--root` argument:

```bash
relative2absolute --root path/to/root/package
```

The `--root` argument determines the starting point for absolute imports. The imports will start from the last element in the path you provide for the `--root` argument. For example, if the root path is:

```
path/to/root/package
```

Then this relative import:

```python
from ..core import database
```

Will be converted to:

```python
from package.app.core import database
```

## Example

### Example directory:

```
example/
│   ├── core/
│   │   ├── database.py
│   │   └── dependencies.py    # conains: from ..utils import send_email 
│   ├── main.py    # contains: from .core.database import get_db
│   └── utils.py        

```

### Command:

```bash
relative2absolute --root path/to/example
```

### Result:

The import in `main.py` will be updated to:

```python
from example.core.database import get_db
```

The import in `dependencies.py` will be updated to:

```python
from example.utils import upload_file
```

## Requirements

- Python 3.6+
- No third-party dependencies

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

## License

This project is licensed under the MIT License.
