from setuptools import setup

setup(
name = 'tk_flexible_preferences_gui',
version = '0.1.4',
description = 'A flexible GUI based on Tkinter. An easy way to visualise preferences defined in a json file, including option controllers. User friendly and easy to implement in projects.',

py_modules = ["flexgui", "preferencesgui", "scrollableframe"],

package_dir = {'': 'src'},

#     packages = ['ThePackageName1',
#                 'ThePackageName2',
#                 ...
#  ],

package_data={
        "confing_template": ["conf.json"],
    },

author = 'marsson87',
author_email = 'marsson87@gmail.com',

# long_description = open('README.md').read() + '\n\n' + open('CHANGELOG.md').read(),
long_description = open('README.md').read(),
long_description_content_type = "text/markdown",

url = 'https://github.com/marsson87/tk_flexible_preferences_gui',

include_package_data = True,

classifiers = [
    'Development Status :: 4 - Beta',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'License :: OSI Approved :: MIT License',
    'Intended Audience :: Developers',
    'Topic :: Desktop Environment',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Operating System :: OS Independent',
],


install_requires = [

    # 'pandas ~= 1.2.4',
    # ...

],

keywords = ['GUI', 'Preferences', 'Settings', 'Options', 'Tkinter', 'JSON'],

)