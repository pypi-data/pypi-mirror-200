# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['getchoice']

package_data = \
{'': ['*']}

install_requires = \
['getkey>=0.6.5,<0.7.0', 'prompt-toolkit>=3.0.38,<4.0.0']

setup_kwargs = {
    'name': 'getchoice',
    'version': '1.2.0',
    'description': 'Simple, extensible user selection interface for CLI applications',
    'long_description': '# getchoice\n\nA simple library to allow a user to select from a list of options on the command line. Like [pick](https://github.com/wong2/pick), but with two major differences:\n \n- `getchoice` is intended for use alongside [python prompt toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit); its output can be styled using PPT-style `(styling, text)` format.\n- `getchoice` does not use `curses`, and does not clear the screen when used.\n\nInstall it from PyPI: `pip install getchoice`\n\n```python \nfrom getchoice import ChoicePrinter\nfrom datetime import date\n\nchoice_printer = ChoicePrinter(normal_style="green italic")\n\n\nitems = [ \n    ("February 1", date(2023, 2, 1)), \n    ("Pi Day", date(2023, 3, 14)), \n    ("Stanislav Petrov Day", date(2023, 9, 26))\n  ]\n\nchoice_printer.getchoice(items, title = "Select a date")\n```\n\nThis displays an interactive prompt menu for the choices, that the user can navigate with the arrow or j/k keys, and select and item with space or enter. `choice_printer.getchoice()` returns a tuple of the form `(selected_index: int, selected_object)`\n\nFor further details, see the `getchoice/getchoice.py` file; it\'s quite simple and hopefully unsuprising.\n',
    'author': 'Keaton Guderian',
    'author_email': 'keagud@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/keagud/getchoice',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
