# Carbonizer

A Python CLI to create carbonized versions of your code. 
This projects is based on: [Carbon](carbon.now.sh), [Pyppetter](https://miyakogi.github.io/pyppeteer/index.html)
and the wonderful [Typer](https://typer.tiangolo.com/) Framework.


## Installation:

```bash
$ pip install carbonizer
```


## Usage

```bash 
carbonizer --help
# This creates a carbonized version in the same directory
carbonizer some_file.py 

# To create the output in a specific folder
carbonizer -t target  some_file.py

# This will grab all files and carbonize them
carbonizer -t target . 

# The -c flag directly copied the output into your clipboard
carbonizer -c some_file.py
```

Note: The copy functionality is only Linux  is tested  while Mac is also supported - theoretically.
