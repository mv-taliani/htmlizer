import collections.abc
import html
from functools import singledispatch

import wtforms


@singledispatch
def htmlize(obj: object) -> str:
    text = html.escape(repr(obj))
    return text


@htmlize.register
def _(text: str) -> str:
    content = html.escape(text).replace("\n", "<br/>\n")
    return f"<p>{content}</p>"


@htmlize.register
def _(seq: collections.abc.Sequence) -> str:
    content = "</li>\n<li>".join(htmlize(item) for item in seq)
    return "<ul>\n<li>" + content + "</li>\n</ul>"


@htmlize.register
def _(form: wtforms.Form, **kwargs) -> str:
    content = kwargs.get("sep", "<br>").join(htmlize(field) for field in form)
    props = htmlize(kwargs)
    return f"<form {props}>\n" + content + "\n</form>"


@htmlize.register
def _(dictio: dict, sep="=") -> str:
    return " ".join(
        f'{prop}{sep}{value if not isinstance(value, dict) else htmlize(value, sep=":")}'
        for prop, value in dictio.items()
    )


@htmlize.register
def _(field: wtforms.Field, **kwargs) -> str:
    sep = kwargs.pop("sep", "<br>")
    return f"{field.label()} {sep} {field(**kwargs)}"


@htmlize.register
def _(field: wtforms.HiddenField) -> str:
    return field()


if __name__ == "__main__":
    from flask import Flask
    from flask_wtf import FlaskForm
    from wtforms.fields import DateField, StringField

    app = Flask(__name__)
    app.config["SECRET_KEY"] = "asdadsdaa"

    class TesteForm(FlaskForm):
        texto = DateField("batata")
        texte = StringField("nhoque")

    @app.route("/")
    def _():
        return "<br>".join(
            htmlize(i)
            for i in [
                TesteForm(),
                "Batatinhas",
                (
                    1,
                    2,
                    4,
                    5,
                    6,
                ),
                {"aiaiai": "bb"},
                5,
            ]
        )

    app.run(debug=True)
