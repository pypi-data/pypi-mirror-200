from pydantic import BaseModel

from .components import Component


class View(BaseModel):
    name: str = None
    components: list[Component]
