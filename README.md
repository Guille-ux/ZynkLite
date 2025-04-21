<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="mimes/zl-mime.png" alt="ZynkMime"></a>
</p>

<h3 align="center">Project Title</h3>

<div align="center">

  [![Status](https://img.shields.io/badge/status-active-success.svg)]() 
  [![GitHub Issues](https://img.shields.io/github/issues/Guille-ux/ZynkLite.svg)](https://github.com/Guille-ux/ZynkLite/issues)
  [![GitHub Pull Requests](https://img.shields.io/github/issues-pr/Guille-ux/ZynkLite.svg)](https://github.com/Guille-ux/ZynkLite/pulls)
  [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

</div>

---

<p align="center"> Few lines describing your project.
    <br> 
</p>

## 📝 Table of Contents
- [About](#about)
- [Currently Working On](#current)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Built Using](#built_using)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## 🧐 About <a name = "about"></a>
ZynkLite is a programming language made in python, the objective is remake this in C for a better speed at programs.

## Currently Working on <a name = "current"></a>
- Structures
- Better Module Importing
- Language Interoperability
- Arrays
- Bytecode

## 🏁 Getting Started <a name = "getting_started"></a>
How to install zynk-py

### Prerequisites
What things you need to install ZynkLite and how to install them.

- ```Python3``` → [python3](https://python.org)
- ```pip``` → [pip](https://bootstrap.pypa.io/get-pip.py)


### Installing


```bash
pip install zynk-py
```
if you want the mime-types go to mimes and run (only on linux)

```bash
bash install.sh
```


now you can import the interpreter!

## 🎈 Usage <a name="usage"></a>
```python
from zynk_lite import interpreter as intp

iterpreter = intp.ZynkLInterpreter() # options like stdlib path or debug...
interpreter.eval('print "hola";') # example
# or if you want run a file...
interpreter.eval_file("program.zl") # program path
```

or use the command line
```bash
zynkl run [file]
```
run files
```bash
zynkl cli
```
Interactive Interpreter


## ⛏️ Built Using <a name = "built_using"></a>
- [Python3](https://python.org)
- [Hatch](https://hatch.pypa.io/)

## ✍️ Authors <a name = "authors"></a>
- [@guille-ux](https://github.com/Guille-ux) - ZynkPy and ZynkLite

See also the list of [contributors](https://github.com/Guille-ux/ZynkLite/contributors) who participated in this project.

## 🎉 Acknowledgements <a name = "acknowledgement"></a>
- Readme Template from ```The-Documentation-Compendium```
