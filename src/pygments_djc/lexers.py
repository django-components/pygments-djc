from typing import List, Tuple

from pygments.lexer import Lexer, bygroups, using
from pygments.lexers.css import CssLexer
from pygments.lexers.javascript import JavascriptLexer
from pygments.lexers.python import PythonLexer
from pygments.lexers.templates import HtmlDjangoLexer
from pygments.token import Name, Operator, Punctuation, String, Text


# Since this Lexer will be used only in documentation, it's a naive implementation
# that detects the nested JS / CSS / HTML blocks by searching for following patterns:
# - `js = """`
# - `js: some.Type = """`
# - `css = """`
# - `css: some.Type = """`
# - `template = """`
# - `template: some.Type = """`
#
# However, this Lexer is NOT sensitive to where the variable is defined. So this highlighting rule
# will be triggered even when the variable is NOT defined on the Component class.
#
# In other words, we want to highlight cases like this:
# ```py
# class MyComponent(Component):
#     template = """
#     <div>Hello World</div>
#     """
# ```
#
# But NOT cases like this:
# ```py
# js = """
# ```
#
# But our implementation still highlights the latter.
def _gen_code_block_capture_rule(var_name: str, next_state: str) -> Tuple[str, str, str]:
    # In Pygments, capture rules are defined as a tuple of 3 elements:
    # - The pattern to capture
    # - The token to highlight
    # - The next state
    return (
        # Captures patterns like `template = """` or `template: some.Type = """`
        rf'({var_name})(\s*)(?:(:)(\s*)([^\s=]+))?(\s*)(=)(\s*)((?:"""|\'\'\'))',
        #  ^           ^       ^  ^    ^          ^    ^  ^    ^
        #  1           2       3  4    5          6    7  8    9
        #
        # The way Pygments Lexers work, when we match something, we have to define how to highlight it.
        # Since the match pattern contains complex structures, we use `bygroups` to highlight individual
        # parts of the match.
        # fmt: off
        bygroups(
            Name.Variable,  # 1
            Text,           # 2
            Punctuation,    # 3
            Text,           # 4
            Name.Class,     # 5
            Text,           # 6
            Operator,       # 7
            Text,           # 8
            String.Doc,     # 9
        ),
        # fmt: on
        # Lastly, we tell the Lexer what the next state should be
        next_state,
    )


# This generates capture rules for when we are already inside the code block
def _gen_code_block_rules(lexer: Lexer) -> List[Tuple[str, str, str]]:
    return [
        # We're inside the code block and we came across a """ or ''',
        # so the code block ends.
        # This is the FIRST item in the list, so it takes precedence over the other rules.
        # `#pop` tells the Lexer to go back to the previous state.
        (r'(?:"""|\'\'\')', String.Doc, "#pop"),
        # Take everything until """ or ''', and pass it to corresponding lexer (e.g. JS / CSS / HTML Lexers)
        (r'((?!"""|\'\'\')(?:.|\n))+', using(lexer)),  # type: ignore
    ]


class DjangoComponentsPythonLexer(PythonLexer):
    """
    Lexer for Django Components Python code blocks.

    This Lexer behaves like a normal Python Lexer, but also highlights
    nested JS / CSS / HTML code blocks within Component classes:

    ```py
    class MyComponent(Component):
        template = \"\"\"
          <div>Hello World</div>
        \"\"\"
        js = \"\"\"
          console.log("Hello World")
        \"\"\"
        css = \"\"\"
          .my-component {
            color: red;
          }
        \"\"\"
    ```
    """

    name = "Django Components Python"
    aliases = ["djc_py", "djc_python"]

    tokens = {
        **PythonLexer.tokens,
        "root": [
            _gen_code_block_capture_rule("template", "template_string"),
            _gen_code_block_capture_rule("js", "js_string"),
            _gen_code_block_capture_rule("css", "css_string"),
            *PythonLexer.tokens["root"],
        ],
        "template_string": _gen_code_block_rules(HtmlDjangoLexer),
        "js_string": _gen_code_block_rules(JavascriptLexer),
        "css_string": _gen_code_block_rules(CssLexer),
    }
