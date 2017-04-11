# PX-Labeler
Pixelwise image labeler for creating ground truth labels

## Getting Started

Currently, the application is built with Python 3, using openCV and PyQt5 libraries. You will need to install Python 3 and preferably virtual environment.

### Prerequisites

Installation of all prerequisites in Windows environment is described in:

```
SETUP_WIN.md
```

Installation of all prerequisites in Mac OSX environment is described in:

```
SETUP_MAC.md
```

### Running the App

Once all of the prerequisites have been installed, download or clone the repository into your local machine. You can run the application directly by calling the using the `python` command from the repository root directory.

```
python px-labeler/main.py
```

_If you are using virtual environment, make sure that the correct environment is turned on._

This will launch the GUI window. Open a directory containing images that you want to tag using the **Load** button in the top right corner of the window. The application will read the contents of the directory and populate the table with available images in the _.png_, _.jpg_, _.gif_, or _.bmp_ formats.

You can navigate through the images by clicking on them in the table, by using the **Next** or **Prev** buttons, or by using keyboard shortcuts **D** for the next frame and **A** for the previous frame. **_Moving to a new image will automatically save the current labels unless no change has been made or the labels are empty._** The table also includes the label status for the images. If an image has been labeled, they will be labeled as _True_ and highlighted _Green_.

Labels can be made directly on the image by clicking and dragging in the desired position. The label marker type can be selected using the dropdown menu. Currently, there are 10 different labels that can be used. Label names can be edited using the **Edit** button. This will produce a dialog with a table of label markers. _Double-click on the label name to edit_.

Label marker settings are saved in the `[px-labeler root]/px-labeler/settings/px_marker.pkl` pickle file. This file contains the label marker table in the Edit dialog mentioned above. This allows the application to access previously edited label markers between sessions.

Image labels are saved in the `[image database dir]/labels/[image_fname].pkl` pickle file. This consists of a numpy array with size `image height x image widgth` which is filled with the feature class defined in label marker settings (0-10). A preview of the labels as an overlay on the original image is provided in the `[image database dir]/labels_display/[image_fname].png`.


## Deployment

The code is ready for deployment using [Pyinstaller](http://www.pyinstaller.org/). To create a .exe or .app file, install `pyinstaller` through `pip`:

```
pip install pyinstaller
```

Once installed, in the project root directory, run the following command:

```
python pyinstaller --onefile --windowed --icon=px-labeler/pxgui/icon.icns --name=PX-Labeler px-labeler/main.py
```

If you in Windows, use the `.ico` file for the icon. After the above command, a `build` and `dist` folder will be available in the project root folder along with a `.spec` file. The `.exe` file is located in the `dist` folder.

If you are in OSX, use the `.icns` file for the icon. Similar to Windows, a `build` and `dist` folders will be created along with the `.spec` file. However, to view the app in full resolution, you will need to edit the `.spec` file, specifically the `app=BUNDLE(...)` part of the file. In this file, include the bundle identifier and the info_plist below.

```
app = BUNDLE(exe,
             name='PX-Labeler.app',
             icon='px-labeler/pxgui/icon.icns',
             bundle_identifier='com.mohikhsan.macos.pxlabeler',
             info_plist={
                'NSHighResolutionCapable': 'True'
                },
             )
```

After the `.spec` file has been edited, `pyinstaller` needs to be run again using the edited `.spec` file.

```
python pyinstaller PX-Labeler.spec
```

This will produce the correct `.app` file in the `dist` directory.

_Note: Currently, `pyinstaller` through `pip` is not supported in Python 3.6. If you are using Python 3.6, you need to use the development version of `pyinstaller`. Download or clone the development version through their [GitHub page](https://github.com/pyinstaller/pyinstaller). You can use `python setup.py install` to install into your environment, or just use the `pyinstaller.py` file directly into the build command._


## Built With

* [Python 3](https://www.python.org/) - Programming Language
* [PyQt5](https://pypi.python.org/pypi/PyQt5/5.8.1) - GUI Library
* [openCV](https://github.com/opencv/opencv) - Image Processing Library

## Versioning

For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

## To-Do

- [ ] Add revert button to revert labels to previous version
- [ ] Remove the need for openCV library (use only PyQt5 and numpy)
- [ ] Add keyboard shortcut for selecting the marker types
- [ ] Replace button text with button icons

## Authors

* **Mohammad Ikhsan** - *Initial work* - [mohikhsan](https://github.com/mohikhsan)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
