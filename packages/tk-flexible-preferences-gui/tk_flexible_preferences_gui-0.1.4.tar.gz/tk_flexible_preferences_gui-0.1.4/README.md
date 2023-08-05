# flex-preferences-gui
A flexible GUI based on Tkinter. An easy way to visualise preferences defined in a json file, including option controllers. User friendly and easy to implement in projects.

Many developers struggle with difficulties how to handle a whole groups of settings.
There is a handy way to visualize them and control by included widgets as:

* groups of settings
* dropdown menus for boolean values
* text fields


How to use it:
1. Install the module using ```pip```.
2. Start from preparation of json file with options and allowed values. Please keep the structure and keywords.
3. Import ```flexgui``` wrapper
4. Make a call of function ```create_gui()``` with at least config.json

Optional arguments for Tkinter window definition are:
* title
* width
* height