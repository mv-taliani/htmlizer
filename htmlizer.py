from dataclasses import dataclass, field
from functools import wraps


@dataclass
class Tag:
    name: str
    attributes: dict = field(default_factory=dict)
    content: str | None = ''
    selector_name: str = ''

    @property
    def html(self):
        attributes = " ".join(f'{key}="{value}"' for key, value in self.attributes.items())
        if self.content:
            return f'<{self.name} {attributes}> {self.content} </{self.name}>'
        return f'<{self.name} {attributes}/>'


def htmlize(name, **props):
    def wrapped(func):
        @wraps(func)
        def inner(*args, **kwargs):
            result = func(*args, *kwargs)
            return Tag(name=name, attributes=props, content=result)

        return inner

    return wrapped


def csslize(prop: str, **styles):
    css = (f'  {proper}: "{value}"' for proper, value in styles.items())
    return prop + " { \n" + ";\n".join(css) + "\n}"
