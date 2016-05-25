# create-splash
Mobile app splash screen creator

## Overview
This simple Python script was created whilst developing mobile apps for iPhone and Android.  Each of them require a number of splash screens to be submitted in different sizes tailored to the various devices.  Whilst this allows the developer freedom to design splash screens that are perfectly suited to each screen size if all you require is a basic image and some text creating dozens of splash screens can become a chore.

With create-splash you can define the screen dimensions you want to support in an xml file along with the details of the source image and any text overlays you want applied and then by running a single command all of the images are generated in one go.

## Getting Started

### Usage
```python createSplash.py screens.xml```
    
### Prerequisites
create-splash makes use of the Python PIL module.  The easiest way to install this is using: ```pip install Pillow```

PIL itself requires a number of jpeg, png and zip libraries.  Instructions for installing these can be found at: <https://pypi.python.org/pypi/Pillow/2.1.0>

