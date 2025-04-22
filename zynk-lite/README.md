<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="../mimes/zl-mime.png" alt="ZynkMime"></a>
</p>

# ZynkLite

[![PyPI Version](https://img.shields.io/pypi/v/zynk-lite.svg)](https://pypi.org/project/zynk-lite)
[![Python Versions](https://img.shields.io/pypi/pyversions/zynk-lite.svg)](https://pypi.org/project/zynk-lite)
[![License: GPLv3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

> Minimalist scripting language for embedding and extensibility

## Features

- Lightweight interpreter (<500KB)
- Python/C interoperable (Future)
- Native file I/O and array operations
- Clean syntax with zero dependencies

## Quick Start

```python
from zynk_lite import Interpreter

zl = Interpreter()
zl.eval('print "Hello from ZynkLite!";')
```

## Installation
```bash
pip install zynk-lite
```

## CLI Usage
```bash
zynkl run script.zl    # Execute file
zynkl cli             # Interactive mode
```

## Documentation
Full language spec and documentation at [Github](https://github.com/Guille-ux/ZynkLite)

## License

`zynk-lite` is distributed under the terms of the [GPLv3](https://spdx.org/licenses/GPL-3.0-or-later.html) license. license.