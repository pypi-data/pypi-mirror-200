# CHANGE DETECTOR

```
 .d8888b. 888
d88P  Y88b888
888    888888
888       88888b.  8888b. 88888b.  .d88b.  .d88b.
888       888 "88b    "88b888 "88bd88P"88bd8P  Y8b
888    888888  888.d888888888  888888  88888888888
Y88b  d88P888  888888  888888  888Y88b 888Y8b.
 "Y8888P" 888  888"Y888888888  888 "Y88888 "Y8888
                                       888
                                  Y8b d88P
                                   "Y88P"
8888888b.         888                   888
888  "Y88b        888                   888
888    888        888                   888
888    888 .d88b. 888888 .d88b.  .d8888b888888
888    888d8P  Y8b888   d8P  Y8bd88P"   888
888    88888888888888   88888888888     888
888  .d88PY8b.    Y88b. Y8b.    Y88b.   Y88b.
8888888P"  "Y8888  "Y888 "Y8888  "Y8888P "Y888
```

[![Pypi](https://img.shields.io/badge/VERSION-0.0.6-blue?style=for-the-badge&logo=pypi)](https://pypi.org/project/changedetector/)

## CHANGE DETECTOR

### Installation

```bash
pip install changedetector
```

Change detector is a tool that can be used to detect changes in your code.
It works with a simple syntax.

```python
from changedetector import detectchange
detectchange.activate()
```
It detects changes in your root directory. And executes the scripts chosen
when the script is executed.

It can be used to detect changes in python, ruby, Cpp  and C files.

You can execute the script on a second `Thread`.
