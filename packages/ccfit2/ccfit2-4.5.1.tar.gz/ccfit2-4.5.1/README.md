# ccfit2

ccfit2 is a package for fitting AC and DC magnetisation data to obtain magnetic
relaxation rates, and then to model the field- and/or temperature-dependence of
these rates with parameterised models of spin-phonon coupling mechanisms.

# Installation

## Users - executable version (AC only)

Download and install the executable version of `ccfit2` from [here](https://www.nfchilton.com/cc-fit.html).

## Users - command line version and module (Full functionality)

Install `ccfit2` with `pip`

`pip install ccfit2`

## Developers

First uninstall any other copies of `ccfit2`

```
pip uninstall ccfit2
```

In the `HEAD` directory of the repository, run

```shell
pip install -e .
```
to install an editable version of the package.

# Documentation

The online documentation for `ccfit2` is a work in progress and can be found [here](https://chilton-group.gitlab.io/cc-fit2/).

Up-to-date, but to-be-replaced, PDF documentation can be found in the `old_docs` directory of this repository.

# Compiling standalone ccfit2 executable

First, install the required packages listed in `setup.py` using `pip`.

## Linux
Install pyinstaller
```
pip install pyinstaller
```

Then run
```
mv ccfit2_exe.py ccfit2.py
pyinstaller --onefile ccfit2.py
mv ccfit2 ccfit2.x
mv ccfit2.py ccfit2_exe.py
```

## Windows
Install pyinstaller
```
pip install pyinstaller
```

Then run

```
mv ccfit2_exe.py ccfit2.py
pyinstaller --onefile --icon=ccfit.ico ccfit2.py
mv ccfit2.py ccfit2_exe.py
```
## MacOS:

Install `py2app`

```
python3 -m pip install -U py2app
```

Then run

```
mv ccfit2_exe.py ccfit2.py
py2applet --make-setup ccfit2.py
python3 setup.py py2app --packages=PIL,ssl
mv ccfit2.py ccfit2_exe.py
```

Then add the ccfit2 logo to `.app` file using the info window, and compress ccfit2.app for download.
