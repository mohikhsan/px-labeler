# Installing Dependenices on Mac #

This file will show you how to install all the dependencies on Mac. Most of the
dependencies are installed through `homebrew` and `pip`.

### Install and Validate XCode ###

- Install XCode from the App Store
- Validate XCode license in terminal: `sudo xcodebuild -license accept`
- Activate XCode command line tools: `sudo xcode-select --install`

### Install Homebrew ###

- Homebrew can be installed from the terminal using the following command.
```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
```
- Ensure that Homebrew is updated: `brew update`
- Update the bash file `~/.bash_profile` using a text editor with the following content:
```
#Homebrew
export PATH=/usr/local/bin:$PATH
```
- Commit the bash file changes: `source ~/.bash_profile`

### Install Python from Homebrew ###

Use the following commands in the terminal to install Python 3 using Homebrew:

```
brew install python3
brew linkapps python3
```

You can check if the installation is complete using `which python3` which should
return and output of `/usr/local/bin/python3`

### Install Virtual Environment and Wrapper for Python ###

Install the virtual environment and its wrapper using the following command:
`pip3 install virtualenv virtualenvwrapper`

Add the following lines to the bash file as before:
```
# Virtualenv/VirtualenvWrapper
export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python3
source /usr/local/bin/virtualenvwrapper.sh
```

### Setup a Virtual Environment with Python 3 Support ###

Setup the virtual environment: `mkvirtualenv pxlabeler -p python3`
Activate the virtual environment: `workon pxlabeler`

### Install Python Packages ###

The following python packages are installed using pip. Install these python
packages while inside virtual environment:
```
pip3 install numpy
pip3 install scipy
pip3 install PyQt5
```

### Install OpenCV with Python3 Support through Homebrew ###

Install OpenCV with Python3 and OpenCV-Contrib support using the following
commands:

```
brew tap homebrew/science
brew install opencv3 --with-contrib --with-python3 --HEAD
```

Resolve Python 3 naming issue and move libs (Example for 3.6):
```
cd /usr/local/opt/opencv3/lib/python3.6/site-packages/
mv cv2.cpython-36m-darwin.so cv2.so
cd ~
echo /usr/local/opt/opencv3/lib/python3.6/site-packages >> /usr/local/lib/python3.6/site-packages/opencv3.pth
```

Open virtual environment `workon pxlabeler` and sym-link opencv libraries.

Since we are using Python 3 (Example is for 3.6):
```
cd ~/.virtualenvs/pxlabeler/lib/python3.6/site-packages/
ln -s /usr/local/opt/opencv3/lib/python3.6/site-packages/cv2.so cv2.so
cd ~
```

Check OpenCV Python is working using:
```
$ python
>>> import cv2
>>> cv2.__version__
```

Which should produce the output `'3.2.0-dev'`
