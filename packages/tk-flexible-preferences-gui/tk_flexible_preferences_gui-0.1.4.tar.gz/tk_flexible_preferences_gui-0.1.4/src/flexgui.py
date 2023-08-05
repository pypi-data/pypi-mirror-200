__author__ = 'marsson87'
__author_email__ = 'marsson87@gmail.com'

from tkinter import *

from preferencesgui import PreferencesGUI


def create_gui(config_json_filename,
               title=None,
               width=None,
               height=None,
               bgcolor=None,
               fgcolor=None,
               button_bgcolor=None,
               button_fgcolor=None,
               debug=False):
    # Manage passed arguments
    if not title:
        title = "Flexible Preferences GUI"
    # Set default window size if not defined in class instance
    if not width:
        width = 500
    if not height:
        height = 300

    root = Tk()

    if not bgcolor:
        bgcolor = root.cget("background")
    if not fgcolor:
        fgcolor = 'black'

    if not button_bgcolor:
        button_bgcolor = '#27cd95'

    if not button_fgcolor:
        button_fgcolor = 'white'

    root.configure(background=bgcolor)

    root.resizable(False, False)  # This code helps to disable windows from resizing

    # Remove the Title bar of the window
    # root.overrideredirect(True)

    PreferencesGUI(root, config_json_filename, title, width, height, bgcolor, fgcolor, button_bgcolor, button_fgcolor, debug)

    root.unbind_all('<<NextWindow>>')  # Unbinding the behavior that causes Tab Cycling
    root.mainloop()


if __name__ == "__main__":
    create_gui(config_json_filename='conf.json')