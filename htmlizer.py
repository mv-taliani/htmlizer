from __future__ import annotations

import html
from dataclasses import dataclass, field
from functools import wraps


@dataclass
class Tag:
    name: str
    attributes: dict = field(default_factory=dict)
    content: list[Tag | str] = field(default_factory=list)
    styles: dict = field(default_factory=dict)

    # selector_name: str = ''

    @property
    def html(self):
        attributes = " ".join(
            f'{key}="{value}"' for key, value in self.attributes.items()
        )
        style = self.css
        if self.content:
            content = translate_content(self.content)
            return f"<{self.name} {attributes} {style}> {' '.join(content)} </{self.name}>"
        return f"<{self.name} {style} {attributes}/>"

    @property
    def css(self):
        style = ""
        if self.styles:
            style = (
                    'style= "'
                    + "; ".join(
                f"{css_prop}: {css_value}"
                for css_prop, css_value in self.styles.items()
            )
                    + '"'
            )
        return style

    @property
    def css_stylesheet(self):
        style = ""
        if self.styles:
            style = (
                    "{\n"
                    + ";\n".join(
                f'{css_prop}: "{css_value}"'
                for css_prop, css_value in self.styles.items()
            )
                    + "}"
            )
        return style

    def __add__(self, other: Tag):
        return f"{self.html}\n{other.html}"

    def __lshift__(self, other: Tag):
        self.content.append(other)

    def __rshift__(self, other: Tag):
        other.content.append(self)

    def __rrshift__(self, other):
        self << other


def translate_content(contents: list[Tag | str]) -> list[str]:
    htmls = list()
    for content in contents:
        try:
            htmls.append(content.html)
        except AttributeError:
            htmls.append(content)
    return htmls


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
            tag = Tag(name=name, attributes=props) << result
            return tag

        return inner

    return wrapped
