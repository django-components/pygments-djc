# pygments-djc

[![PyPI - Version](https://img.shields.io/pypi/v/pygments-djc)](https://pypi.org/project/pygments-djc/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pygments-djc)](https://pypi.org/project/pygments-djc/) [![PyPI - License](https://img.shields.io/pypi/l/pygments-djc)](https://github.com/django-components/pygments-djc/blob/main/LICENSE) [![PyPI - Downloads](https://img.shields.io/pypi/dm/pygments-djc)](https://pypistats.org/packages/pygments-djc) [![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/django-components/pygments-djc/tests.yml)](https://github.com/django-components/pygments-djc/actions/workflows/tests.yml)

_[Pygments](https://pygments.org/) Lexers for [django-components](https://pypi.org/project/django-components/)._

## Installation

1. Install the package:
    ```bash
    pip install pygments-djc
    ```

2. Add the lexers to your Pygments configuration by simply importing `pygments_djc`
    ```python
    import pygments_djc
    ```

## Lexers

### `DjangoComponentsPythonLexer`

Code blocks: `djc_py` / `djc_python`

This is the same as Python3 Lexer, but also highlights nested JS / CSS / HTML code blocks within `Component` classes:

```python
class MyComponent(Component):
    template = """
      <div>Hello World</div>
    """
```

The syntax highlight then looks like this:

![Django Components Python Lexer Example](./assets/demo.png)

## Release notes

Read the [Release Notes](https://github.com/django-components/pygments-djc/tree/main/CHANGELOG.md)
to see the latest features and fixes.

## Development

### Tests

To run tests, use:

```bash
pytest
```
