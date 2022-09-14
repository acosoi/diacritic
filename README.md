# Diacritic

Diacritic allows you to define and use your own custom shortcuts for language-specific special characters.

### Installation

Download and unzip the most recent release from Releases here on GitHub, then run `diacritic.exe`. There is no installation required, nor do you require any admin rights.

Windows will warn you that the build is not signed and ask if you want to run it anyway, that's normal.

### Usage Guide

Once Diacritic is running, you should see a new icon in the task bar. This lets you know that Diacritic is currently running.

To use custom shortcuts, hit `Ctrl + Alt`, then the shortcut for your desired character. You can find the list of characters and configurations in `config.json`, such as:

```
{
			"name": "French",
			"keys": {
				"`": "ç",
				"1": "à",
				"2": "â",
				"3": "é",
        ...
}
```

For example, in order to type out `à`, you would need to first press `Ctrl + Alt`, then `1` (separately, you don't need to press `Ctrl + Alt + 1` at the same time).

You can right click on the task bar icon in order to switch between languages (called "configurations"). If you change `config.json`, you can use the `Reload Configurations` option in order to refresh the shortcut definitions.

### Building From Source

If you want to build the code yourself or make changes to the code then you'll need to use Python 3.x in order to run `diacritic.py`, as well as the `keyboard` and `PySimpleGUIQt` packages, which you can install using `pip`.

If you're looking to build an executable file, I'd recommend using `auto-py-to-exe`, which you can also install using `pip`. When building the executable, remember to include the `app.ico` and `config.json` files in the bundle, otherwise you'll get errors or weird behavior when booting the application.

When building the executable you'll want to use Python 3.8 or earlier if you're targeting Windows 7, otherwise 3.9+ can be used as well.

### Development Backlog

This is a list of things that I'd like to add in the future (no promises though):
* UI for configuring shortcuts;
* The ability to change the initial shortcut (`Ctrl + Alt`) without having to change the code;
* Support for adding Diacritic to the system start-up via app settings;
* Automated reloading of `config.json` when the file changes;
* Better validation and error handling, especially for issues encountered when parsing `config.json`;
* Test Diacritic on Mac and Linux, fix any issues and provide releases for these platforms.
