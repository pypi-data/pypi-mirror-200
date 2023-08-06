# gorse

#### Installing

Install and update using pip:

```
$ pip install -U gorse
```

#### A Simple Example

```
from gorse import route, run, template


@route("/hello/<name>")
def hello(name):
    return template("<b1>Hello {{name}}</b1>!", name=name)


@route("/")
def index():
    return "<h1>Hello world!</h1>"

run(host="127.0.0.1", port=8000, debug=True)
```

#### Links

- Documentation: [https://github.com/MarkHoo/gorse](https://github.com/MarkHoo/gorse)
- PyPI Releases: [https://pypi.org/project/gorse/](https://pypi.org/project/gorse/)
- Source Code: [https://github.com/MarkHoo/gorse](https://github.com/MarkHoo/gorse)
- Issue Tracker: [https://github.com/MarkHoo/gorse/issues](https://github.com/MarkHoo/gorse/issues)
- Website: [https://pypi.org/project/gorse/](https://pypi.org/project/gorse/)

