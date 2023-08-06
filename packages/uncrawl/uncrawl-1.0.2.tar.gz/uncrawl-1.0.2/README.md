# Uncrawl

A lightweight package for webpage scraping and content extraction.

## Installation

```sh
pip install uncrawl
```

## Example

```python
from uncrawl import uncrawl

url = "https://example.com/article"
path = "docs/article"

uncrawl(url, path)
"""
:type url: str
:type path: int
  path with markdown filename
"""
```
