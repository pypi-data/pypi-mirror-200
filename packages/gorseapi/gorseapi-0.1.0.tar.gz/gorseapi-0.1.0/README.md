# GorseAPI

#### Installing

Install and update using pip:

```
$ pip install -U gorseapi
```

#### A Simple Example

```
from gorseapi import GorseAPI


app = GorseAPI(__name__)

@app.route("/")
def hello():
    return "<h1>Hello World!</h1>"

app.run("127.0.0.1", 8000, debug=True)
```

#### Links

- Documentation: [https://github.com/MarkHoo/gorseapi](https://github.com/MarkHoo/gorseapi)
- PyPI Releases: [https://pypi.org/project/gorseapi/](https://pypi.org/project/gorseapi/)
- Source Code: [https://github.com/MarkHoo/gorseapi](https://github.com/MarkHoo/gorseapi)
- Issue Tracker: [https://github.com/MarkHoo/gorseapi/issues](https://github.com/MarkHoo/gorseapi/issues)
- Website: [https://pypi.org/project/gorseapi/](https://pypi.org/project/gorseapi/)

