from typing import Callable, Literal, Optional, Union

from patch.util.code import code_to_text
from pydantic import BaseModel


class BaseComponent(BaseModel):
    required: bool = False

    # holds the order of the fields to be populated when positional args are passed
    _positional_fields = []

    def __init__(self, *args, **kwargs) -> None:
        for idx, arg in enumerate(args):
            kwargs[self._positional_fields[idx]] = arg
        super(BaseComponent, self).__init__(**kwargs)


class Paragraph(BaseComponent):
    text: str

    _positional_fields = ["text"]


class Button(BaseComponent):
    text: str
    action: Optional[str] = None
    handler: Optional[Callable] = None

    _positional_fields = ["text", "action"]


class ButtonBar(BaseComponent):
    buttons: list[Button]

    _positional_fields = ["buttons"]


class TextInput(BaseComponent):
    name: str

    _positional_fields = ["name"]


def _strip_empty_lines(param):
    lines = param.splitlines()
    lines = [line for line in lines if not line.isspace()]
    return "\n".join(lines)


class Chart(BaseComponent):
    type: Literal["Chart"] = "Chart"
    code: Optional[str] = None
    function_name: Optional[str] = None

    def __init__(self, generator: Callable = None, **kwargs):
        super().__init__(**kwargs)
        self.set_generator(generator)

    def set_generator(self, value):
        if value:
            self.code = _strip_empty_lines(code_to_text(value))
            self.function_name = value.__name__


Component = Union[Paragraph, Button, Chart]
