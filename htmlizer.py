from dataclasses import dataclass, field
from functools import wraps


@dataclass
class Tag:
    name: str
    attributes: dict = field(default_factory=dict)
    content: str | None = ''
    styles: dict = field(default_factory=dict)
    # selector_name: str = ''

    @property
    def html(self):
        attributes = " ".join(f'{key}="{value}"' for key, value in self.attributes.items())
        style = ''
        if self.styles:
            style = 'style= "' + "; ".join(f'{css_prop}: {css_value}' for css_prop, css_value in self.styles.items()
                                           ) + '"'
        if self.content:
            return f'<{self.name} {attributes} {style}> {self.content} </{self.name}>'
        return f'<{self.name} {style} {attributes}/>'


def create_css(**styles):
    def wrapped(func):
        @wraps(func)
        def inner(*args, **kwargs):
            result: Tag = func(*args, **kwargs)
            result.styles.update(styles)
            return result
        return inner
    return wrapped


def htmlize(name, **props):
    def wrapped(func):
        @wraps(func)
        def inner(*args, **kwargs):
            result = func(*args, *kwargs)
            try:
                content = result.html
            except AttributeError:
                content = result

            return Tag(name=name, attributes=props, content=content)

        return inner

    return wrapped
