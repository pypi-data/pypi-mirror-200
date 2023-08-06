import os
import re
from setuptools import setup

requires = ["pycryptodome==3.16.0","websocket_client","requests","rubiran","Pillow==9.4.0","libraryshad","requests","pyrubika"]
_long_description = """


### How to import the rubino library

``` bash
from rabino import rubino
```

### How to install the library

``` bash
pip install rabino==1.0.3
```

### My ID in Rubika

``` bash
@professor_102
```
## And My ID Channel in Rubika

``` bash
@python_java_source 
```
"""

setup(
    name = "rabino",
    version = "1.0.3",
    author = "mamadcoder",
    author_email = "x.coder.2721@gmail.com",
    description = ("Rubika Library Bot"),
    license = "MIT",
    keywords = ["rubika","bot","robot","library","rubikalib","rubikalib.ml","rubikalib.ir","rabino","Rabino","libraryrobiran","Rubika","Python","rubiran","pyrubi","telebot"],
    url = "https://github.com/pypa/sampleproject",
    packages=['rabino'],
    long_description=_long_description,
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
    ],
)