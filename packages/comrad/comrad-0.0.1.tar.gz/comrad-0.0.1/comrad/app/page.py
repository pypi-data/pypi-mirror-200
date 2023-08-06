from typing import Callable, Iterable, Mapping, Union

from .components import Component
from .view import View


class Page:
    def __init__(
        self, name: str, controller: Mapping, components: Iterable[Component]
    ) -> None:
        self.name = name
        self.controller = controller  # TODO - extend controller parsing to accept mapping and str: Union[Controller, Mapping, str]
        self.components = components  # TODO - extend components parsing to also accept a callable: Union[Iterable[Component], Callable]
        self.view: View = View(name=name, components=components)
