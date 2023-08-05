__author__ = 'marsson87'
__author_email__ = 'marsson87@gmail.com'

import copy
import json
from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkFont

from scrollableframe import ScrollableFrame


class PreferencesGUI:
    def __init__(self, master, config_filename, title, width, height, bgcolor, fgcolor, button_bgcolor, button_fgcolor, debug):
        self.master = master
        self.config_filename = config_filename

        self.master.title(title)

        self.debug = debug

        # Calculate relative font size depending on OS
        ref_font = tkFont.Font(family="TkDefaultFont")
        ref_text = '0'
        self.f_px = ref_font.measure(ref_text)

        self.total_width = width
        self.total_height = height

        self.bgcolor = bgcolor
        self.fgcolor = fgcolor
        self.button_bgcolor =button_bgcolor
        self.button_fgcolor =button_fgcolor

        # Initialize style
        s = ttk.Style()
        s.theme_use('clam')

        # Create style for the frame and labels
        s.configure('TFrame', background=self.bgcolor)
        s.configure('TLabel', background=self.bgcolor, foreground=self.fgcolor)
        # s.configure('TCombobox', background=self.bgcolor, fieldbackground=self.bgcolor, foreground=self.fgcolor)

        # Create style for the buttons
        s.configure('TButton', relief='flat', background=self.bgcolor, foreground=self.fgcolor)
        s.map('TButton',
              foreground=[('active', self.button_fgcolor)],
              background=[('active', self.button_bgcolor)])

        # Create style for the separator
        s.configure('vert.TSeparator', background='gray')

        # Add frame for categories container
        self.frame_left = ttk.Frame(self.master)
        self.frame_left.grid(column=0, row=0, sticky=N)

        # Add scrollable frame for settings container
        self.create_scrollable_frame()

        # Add frame for buttons container
        self.frame_bottom = ttk.Frame(self.master)
        self.frame_bottom.grid(column=0, columnspan=3, row=1)

        self.create_separator()

        self.create_buttons()

        # Set predefined starting values and empty lists
        self.current_category_selection = None
        self.category_current_row = 0
        self.category_buttons = []
        self.options_current_row = 0
        self.options_fields = []
        self.options_fields_values = []

        # Load json settings
        self.working_config = json.load(open(self.config_filename))
        if self.debug: print(self.working_config)

        self.reference_config = copy.deepcopy(self.working_config)

        self.initiate_settings_from_file()

    def create_scrollable_frame(self):
        self.frame_right_sc = ScrollableFrame(self.master,
                                              total_width=self.total_width,
                                              total_height=self.total_height,
                                              bgcolor=self.bgcolor)
        self.frame_right_sc.grid(column=2, row=0, sticky=N)

    def create_separator(self):
        self.separator = ttk.Separator(self.master, orient=VERTICAL, style='vert.TSeparator',
                                       takefocus=0) # cursor='plus'
        self.separator.grid(column=1, row=0, ipady=int(self.total_height // 2), padx=5)

    def create_buttons(self):
        self.ok_button = ttk.Button(self.frame_bottom, text='OK', command=self.clicked_ok_button)
        self.ok_button.grid(column=0, row=0, padx=5, pady=10)

        self.cancel_button = ttk.Button(self.frame_bottom, text='Cancel', command=self.close_window)
        self.cancel_button.grid(column=1, row=0, padx=5, pady=10)

    def initiate_settings_from_file(self):
        for i, item in enumerate(self.working_config):
            if i == 0:
                first_item = item
            if self.debug: print(item)
            self.add_category(label=item)

        self.current_category_selection = first_item
        self.add_options(parent_label=first_item)

    def add_category(self, label):
        self.category_buttons.append(ttk.Button(
            self.frame_left,
            text=label,
            command=lambda c=len(self.category_buttons): self.change_tool(c)
        ))
        self.category_buttons[-1].grid(
            column=0,
            row=self.category_current_row,
            sticky=W + E,
            padx=4,
            pady=2)

        self.category_current_row += 1

    def add_options(self, parent_label):
        if self.debug: print(f"parent label: {parent_label}")
        self.current_category_selection = parent_label
        for item in self.working_config[parent_label]:
            conf_name = item
            label = self.working_config[parent_label][item]['field_description']
            tag = self.working_config[parent_label][item]['type']
            current = self.working_config[parent_label][item]['current']

            ttk.Label(self.frame_right_sc.scrollable_frame,
                      text=label,
                      wraplength=self.total_width - 5).grid(row=self.options_current_row,
                                                            column=0,
                                                            padx=5,
                                                            pady=5,
                                                            sticky=N + W)

            self.options_current_row += 1

            if tag == 'dropdown':
                options = self.working_config[parent_label][item]['options']
                self.add_options_dropdown(options_list=options, current_selection=current, name=conf_name)
            else:
                self.add_options_entry(current_text=current, name=conf_name)

            self.options_current_row += 1

    def add_options_dropdown(self, options_list, current_selection, name):
        self.options_fields_values.append(tk.StringVar())
        self.options_fields.append(ttk.Combobox(self.frame_right_sc.scrollable_frame,
                                                textvariable=self.options_fields_values[-1],
                                                width=15,
                                                state='readonly'))
        self.options_fields[-1]['values'] = tuple(options_list)
        self.options_fields[-1].current(current_selection)
        self.options_fields[-1].option_id = name
        self.options_fields[-1].grid(row=self.options_current_row,
                                     column=0,
                                     padx=5,
                                     pady=5,
                                     sticky=N + W)

    def add_options_entry(self, current_text, name):
        self.options_fields_values.append(StringVar(self.master, value=current_text))
        self.options_fields.append(ttk.Entry(self.frame_right_sc.scrollable_frame,
                                             textvariable=self.options_fields_values[-1],
                                             width=int(self.total_width // self.f_px)))
        self.options_fields[-1].option_id = name
        self.options_fields[-1].grid(row=self.options_current_row,
                                     column=0,
                                     padx=5,
                                     pady=5,
                                     sticky=N + W)

    def update_config_dict(self, node, value):
        self.working_config[self.current_category_selection][node]['current'] = value

    def update_working_config(self):
        for item in self.options_fields:
            current_id = item.option_id
            if self.debug: print(current_id)
            if isinstance(item, tk.ttk.Combobox):
                # print(item['values'])
                current_selection = item.current()
                self.update_config_dict(node=current_id, value=current_selection)
            elif isinstance(item, tk.ttk.Entry):
                entry_value = item.get()
                self.update_config_dict(node=current_id, value=entry_value)
            else:
                print('not defined widget')

        if self.debug:
            print(f"Reference config: {self.reference_config}")
            print(f"Current config: {self.working_config}")

    def close_window(self):
        self.master.quit()

    def clicked_ok_button(self):
        self.update_working_config()
        with open(self.config_filename, 'w') as f:
            json.dump(self.working_config, f, indent=2)
        self.close_window()

    @staticmethod
    def clear_widget(target_frame):
        for widget in target_frame.winfo_children():
            widget.destroy()

    def change_tool(self, index):
        # Take current values and update temporary config dictionary
        self.update_working_config()

        btn_name = self.category_buttons[index].cget("text")

        self.clear_widget(self.frame_right_sc)
        self.options_current_row = 0
        self.options_fields = []
        self.options_fields_values = []

        self.create_scrollable_frame()
        self.add_options(parent_label=btn_name)