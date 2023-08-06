# PyCrawlerX
PyCrawlerX is a Python CLI tool to crawl through directories and execute files.

## Installation
```python -m pip install pycrawlerx```

## Example Usage

### Read input from command line
```python
import sys
from PyCrawlerX import PyCrawlerX

if __name__ == "__main__":
    pcx = PyCrawlerX()
    code_folder = sys.argv[1]
    pcx.run_pycrawlerx(folder_path = code_folder)

```

### Read input from the script
```python
from PyCrawlerX import PyCrawlerX

if __name__ == "__main__":
    pcx = PyCrawlerX()
    code_folder = './test'
    pcx.run_pycrawlerx(folder_path = code_folder)

```

### Load environment variables
```python
from PyCrawlerX import PyCrawlerX

if __name__ == "__main__":
    pcx = PyCrawlerX()
    code_folder = './test'
    pcx.run_pycrawlerx(folder_path = code_folder)
    pcx.load_environment_variables(key_value = {"key": "value"})

```