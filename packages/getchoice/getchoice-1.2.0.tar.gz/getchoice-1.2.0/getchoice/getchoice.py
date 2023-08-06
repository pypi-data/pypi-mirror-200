import sys
from enum import Enum, auto
from typing import Optional, TypeVar

from getkey import getkey, keys
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style


class PromptAction(Enum):
    NONE = auto()
    UP = auto()
    DOWN = auto()
    SELECT = auto()


T = TypeVar("T")


def make_choice_style(
    title: str = "",
    selected: str = "",
    unselected: str = "",
):
    return Style.from_dict(
        {"title": title, "selected": selected, "unselected": unselected}
    )


def _format_tags(text, tag):
    return f"<{tag}>{text}</{tag}>"


class ChoicePrinter:
    def __init__(
        self,
        style: Optional[Style] = None,
        pointer: str = "*",
        show_numbers: bool = False,
    ) -> None:
        self.style = style
        self.pointer = pointer
        self.show_numbers = show_numbers

    def read_key(self) -> PromptAction:
        key = getkey()

        if key in (keys.DOWN, keys.J):
            return PromptAction.DOWN

        if key in (keys.UP, keys.K):
            return PromptAction.UP

        if key in (keys.SPACE, keys.ENTER):
            return PromptAction.SELECT

        return PromptAction.NONE

    def print_styled(self, text: str, tag: str):
        tagged = _format_tags(text, tag)
        print_formatted_text(HTML(tagged), style=self.style)

    def clear_lines(self, count: int):
        sys.stdout.write(f"\x1b[{count}F")

        sys.stdout.write("\r")

        sys.stdout.write("\x1b[0J")

    def hide_cursor(self):
        print("\033[?25l", end="")

    def show_cursor(self):
        print("\033[?25h", end="")

    def print_choices(
        self, choices: list[str], selected: int, title: Optional[str] = None
    ):
        assert 0 <= selected < len(choices)

        if title is not None:
            self.print_styled(title, "title")

        for i, text in enumerate(choices):
            this_style = "unselected"
            prefix = " " * len(self.pointer)

            if i == selected:
                this_style = "selected"
                prefix = self.pointer

            num = f"{i + 1: <2}" if self.show_numbers else ""

            self.print_styled(f"{prefix}{num}{text}", this_style)

    def getchoice(
        self,
        options: list[tuple[str, T]],
        title: Optional[str] = None,
    ) -> tuple[int, T]:
        selected: int = 0
        self.hide_cursor()

        additional_lines = 0
        if title is not None:
            additional_lines = len(title.split("\n"))

        self.print_choices([o[0] for o in options], selected=selected, title=title)

        user_input = self.read_key()
        while True:
            match user_input:
                case PromptAction.UP:
                    selected = max(selected - 1, 0)

                case PromptAction.DOWN:
                    selected = min(len(options) - 1, selected + 1)

                case PromptAction.SELECT:
                    _, item = options[selected]
                    self.show_cursor()
                    return (selected, item)

                case _:
                    continue

            self.clear_lines(len(options) + additional_lines)

            self.print_choices([o[0] for o in options], selected=selected, title=title)

            user_input = self.read_key()

    def yes_no(self, title: Optional[str] = None):
        return self.getchoice(title=title, options=[("Yes", True), ("No", False)])
