import os
import re
from setuptools import setup

_long_description = """

## An example:
``` python
from rubip import rubip

proxies = {'https': 'https://localhost:8080'}

bot = rubip("Auth Account",proxies=proxies)

gap = "guids"

bot.sendMessage(gap,"pyrubika")
```


### How to import the Rubik's library

``` bash
from rubip import rubip
```

### How to install the library

``` bash
pip install rubip
```

### My ID in Rubika

``` bash
@mamadcoder1
```
## And My ID Channel in Rubika

``` bash
@python_java_source 
```
"""

setup(
    name = "rubip",
    version = "2.0.6",
    author = "mamadcoder",
    author_email = "mamadcoder@gmail.com",
    description = ("Another example of the library making the Rubik's robot"),
    license = "MIT",
    keywords = ["rubika","bot","robot","library","rubikalib","rubikalib.ml","rubikalib.ir","rubika.ir","Rubika","Python","Pyrubika","pyrubika"],
    url = "https://rubika.ir/python_java_source",
    packages=['rubip'],
    long_description=_long_description,
    long_description_content_type = 'text/markdown',
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    "Programming Language :: Python :: Implementation :: PyPy",
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10'
    ],
)
