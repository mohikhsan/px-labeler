# Installing Dependenices on Windows (Easy Way) #

This file will show you the quick and easy way on how to install all the
prerequisites and get the Python files running. This uses prebuilt Python packages from [Christoph
Gohlke's website](http://www.lfd.uci.edu/~gohlke/pythonlibs/).

### Install Visual Studio ###

To run Python packages from Christoph Gohlke's website, we need to follow his
built requirements. If you are using Python 3.5/3.6, install [Visual Studio
Community 2015](https://www.visualstudio.com/downloads/) so that the Visual
C++ 2015 Redistributable Packages are included. The Python Tools in Visual Studio are also pretty good for editing python scripts.

### Install Python ###

For this project, Python 3 was used. You can download the latest
version of Python from the Python website. Make sure to download the 64-bit
version of Python.

### Install Python Libraries ###

Python libraries can be installed by downloading the wheel files in [Christoph
Gohlke's website](http://www.lfd.uci.edu/~gohlke/pythonlibs/). For each package, make sure to download the correct wheel file
based on the Python version (e.g. cp36-win_amd64 for Python 3.6 64-bit).

The packages that need to be downloaded:
```
- numpy-mkl
- scipy
- opencv
```
Since PyQt5 wheel file is not available in the website, it will be installed using `pip`.

`pip install PyQt5`

Note: if the `pip` command returns an error, try `pip3`.
