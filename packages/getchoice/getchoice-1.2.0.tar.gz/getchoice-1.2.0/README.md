# getchoice

A simple library to allow a user to select from a list of options on the command line. Like [pick](https://github.com/wong2/pick), but with two major differences:
 
- `getchoice` is intended for use alongside [python prompt toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit); its output can be styled using PPT-style `(styling, text)` format.
- `getchoice` does not use `curses`, and does not clear the screen when used.

Install it from PyPI: `pip install getchoice`

```python 
from getchoice import ChoicePrinter
from datetime import date

choice_printer = ChoicePrinter(normal_style="green italic")


items = [ 
    ("February 1", date(2023, 2, 1)), 
    ("Pi Day", date(2023, 3, 14)), 
    ("Stanislav Petrov Day", date(2023, 9, 26))
  ]

choice_printer.getchoice(items, title = "Select a date")
```

This displays an interactive prompt menu for the choices, that the user can navigate with the arrow or j/k keys, and select and item with space or enter. `choice_printer.getchoice()` returns a tuple of the form `(selected_index: int, selected_object)`

For further details, see the `getchoice/getchoice.py` file; it's quite simple and hopefully unsuprising.
