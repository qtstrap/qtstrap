# Project Structure
This is the project structure that's created by running `qtstrap init`:

```
|-- src
|   |-- main.py
|   |-- application.py
|   |-- mainwindow.py
|-- resources
|   |-- application.ico
|   |-- icon.svg
|-- bundle.spec
|-- installer.iss
|-- Makefile
|-- project.ini
|-- requirements.txt
```

# Files

## `src` folder
Your application's python source code should all be placed here. A newly created qtstrap project contains `src/main.py`, `src/application.py`, and `src/main_window.py`.

## [`Makefile`](makefile.md)
The provided Makefile has several targets that assist with general project development. Using the Makefile means that you do not have to activate the venv unless you need to interact with it directly. The Makefile uses specially constructed targets to automatically build the venv and execute using the venv's python installation.

Most of the time you'll just use `make run` to start your application. When you're ready to package up your app for distribution, you'll want to use `make bundle`, `make zip`, and (on Windows) `make installer`.

More information about the Makefile and it's targets can found [here](makefile.md)

## `project.ini`
Contains information about the project like the Application Name and Publisher. This file is referenced by `bundle.spec` and `installer.iss`, and used to feed information to PyInstaller and InnoSetup.

The project file defines the following fields:

- `AppName` your app's name
- `AppVersion` your app's version number
- `AppPublisher` your app's publisher, which is most likely you
- `AppExeName` the name of the executable created by `make bundle`
- `AppIconName` the path to your application's icon
- `AppId` a GUID used by Inno Setup to uniquely identify your app

## `resources/application.ico` and `icon.svg`
Icon files that are automatically applied to the app's titlebar, taskbar entry, bundle, and installer. When running the bundled executable, the installer, or the installed version of your app, the icon should also appear in Windows Task Manager.

## `requirements.txt`
Your application's python dependecies. If your application uses any packages, you should list them here, preferably with the versions pinned.

A fresh project created with `qtstrap init` looks something like this:
```
altgraph==0.17
click==7.1.2
future==0.18.2
pefile==2019.4.18
prompt-toolkit==1.0.14
Pygments==2.8.1
PyInquirer==1.0.3
pyinstaller==4.2
pyinstaller-hooks-contrib==2021.1
PySide2==5.15.2
pywin32-ctypes==0.2.0
qtstrap==0.0.7
regex==2021.3.17
shiboken2==5.15.2
six==1.15.0
wcwidth==0.2.5
```

## `bundle.spec`
A [PyInstaller](https://www.pyinstaller.org/) spec file that creates a single-folder executable. The bundle is created at `./dist/$AppName/`, and the executable at `./dist/$AppName/$AppName.exe`.

## `installer.iss`
An [Inno Setup](https://jrsoftware.org/isinfo.php) setup compiler script that creates a Windows installer. The installer is created at `/dist/installer/$AppName-$AppVersion-Setup.exe`