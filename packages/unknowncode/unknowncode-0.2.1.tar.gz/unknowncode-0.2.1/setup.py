# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['unknowncode']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'unknowncode',
    'version': '0.2.1',
    'description': 'Small portions of code I use, gathered into one group for ease of access. Like a mod library for a game. Built with poetry',
    'long_description': '# UnknownCode Guide/Compendium\n\n## This file is a list of all the information and commands in unknowncode.\nArguments in **Bold** are required arguments.\nArguments in *Italics* are optional arguments\n\n##### custom_response(**response_list**,**cap_sense**,**prompt**)\n> response_list is a list of (guess what?) allowed responses, anything you want a user to be able to reply with\nExample: `response_list = ["Sure","Yeah!"]`\ncap_sense is wether you want it to be Case Sensitive. If True then it will be Case Sensitive.\nprompt is any string that you want the user to respond to\nExample: `prompt = "Are you ready to code?"`\n\n##### yes_no(**prompt**)\n> yes_no() is a preset version of custom_response_input, preset with a list of ["Yes","yes","Y","y"]`.\nprompt is any string that you want the user to respond to\nExample: `prompt = "Are you ready to code?"`\nIf the user respondses with anything that is Yes or Y (includng lowercase)\n\n\n\n# UnknownCode Changelog 0.2.0 (Last version 0.1.0)\n\n##### Added:\n>README.md\nCHANGELOG.md\ncustom_response()\n#\n# UnknownCode Guide/Compendium\n###### (version 0.2.1)\n---\nArguments in **Bold** are required arguments.\nArguments in *Italics* are optional arguments\n\n##### custom_response(**response_list**,**cap_sense**,**prompt**)\n#\n> response_list is a list of (guess what?) allowed responses, anything you want a user to be able to reply with\nExample: `response_list = ["Sure","Yeah!"]`\ncap_sense is wether you want it to be Case Sensitive. If True then it will be Case Sensitive.\nprompt is any string that you want the user to respond to\nExample: `prompt = "Are you ready to code?"`\n\n##### yes_no(**prompt**)\n#\n> yes_no() is a preset version of custom_response_input, preset with a list of ["Yes","yes","Y","y"]`.\nprompt is any string that you want the user to respond to\nExample: `prompt = "Are you ready to code?"`\nIf the user respondses with anything that is Yes or Y (includng lowercase)\n\n#\n---\n#\n\n## UnknownCode Changelog 0.2.1 (Last version 0.2.1)\n\n##### Added:\n#\n>README.md\nCHANGELOG.md\ncustom_response()',
    'author': 'UnknownSources',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
