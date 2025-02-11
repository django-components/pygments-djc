from pygments.token import Keyword, Literal, Name, Operator, Punctuation, Text
from pygments.lexers.css import CssLexer
from pygments.lexers.javascript import JavascriptLexer
from pygments.lexers.templates import HtmlDjangoLexer

from pygments_djc import DjangoComponentsPythonLexer


def test_djcpy_html():
    code = '''
class Calendar(Component):
    template = """
        <div>Hello</div>
    """
    '''
    lexer = DjangoComponentsPythonLexer()
    tokens = list(lexer.get_tokens(code))

    html_tokens = list(HtmlDjangoLexer().get_tokens("<div>Hello</div>"))
    assert html_tokens == [
        (Punctuation, "<"),
        (Name.Tag, "div"),
        (Punctuation, ">"),
        (Text, "Hello"),
        (Punctuation, "<"),
        (Punctuation, "/"),
        (Name.Tag, "div"),
        (Punctuation, ">"),
        (Text, "\n"),
    ]

    assert tokens == [
        (Keyword, "class"),
        (Text.Whitespace, " "),
        (Name.Class, "Calendar"),
        (Punctuation, "("),
        (Name, "Component"),
        (Punctuation, ")"),
        (Punctuation, ":"),
        (Text.Whitespace, "\n"),
        (Text, "    "),
        (Name.Variable, "template"),
        (Text, " "),
        (Operator, "="),
        (Text, " "),
        (Literal.String.Doc, '"""'),
        (Text, "\n        "),
        # Syntax highlighting for the HTML
        *html_tokens[:-1],
        # End of the HTML
        (Text, "\n    "),
        (Literal.String.Doc, '"""'),
        (Text.Whitespace, "\n"),
        (Text, "    "),
        (Text.Whitespace, "\n"),
    ]


def test_djcpy_js():
    code = '''
class Calendar(Component):
    js = """
        console.log("Hello");
    """
    '''
    lexer = DjangoComponentsPythonLexer()
    tokens = list(lexer.get_tokens(code))

    js_tokens = list(JavascriptLexer().get_tokens('console.log("Hello");'))

    assert js_tokens == [
        (Name.Other, "console"),
        (Punctuation, "."),
        (Name.Other, "log"),
        (Punctuation, "("),
        (Literal.String.Double, '"Hello"'),
        (Punctuation, ")"),
        (Punctuation, ";"),
        (Text.Whitespace, "\n"),
    ]

    assert tokens == [
        (Keyword, "class"),
        (Text.Whitespace, " "),
        (Name.Class, "Calendar"),
        (Punctuation, "("),
        (Name, "Component"),
        (Punctuation, ")"),
        (Punctuation, ":"),
        (Text.Whitespace, "\n"),
        (Text, "    "),
        (Name.Variable, "js"),
        (Text, " "),
        (Operator, "="),
        (Text, " "),
        (Literal.String.Doc, '"""'),
        (Text, ""),
        (Text.Whitespace, "\n        "),
        # Syntax highlighting for the JS
        *js_tokens[:-1],
        # End of the JS
        (Text.Whitespace, "\n    "),
        (Literal.String.Doc, '"""'),
        (Text.Whitespace, "\n"),
        (Text, "    "),
        (Text.Whitespace, "\n"),
    ]


def test_djcpy_css():
    code = '''
class Calendar(Component):
    css = """
        .calendar {
            background-color: red;
        }
    """
    '''
    lexer = DjangoComponentsPythonLexer()
    tokens = list(lexer.get_tokens(code))

    css_tokens = list(CssLexer().get_tokens(".calendar { background-color: red; }"))

    assert css_tokens == [
        (Punctuation, "."),
        (Name.Class, "calendar"),
        (Text.Whitespace, " "),
        (Punctuation, "{"),
        (Text.Whitespace, " "),
        (Keyword, "background-color"),
        (Punctuation, ":"),
        (Text.Whitespace, " "),
        (Keyword.Constant, "red"),
        (Punctuation, ";"),
        (Text.Whitespace, " "),
        (Punctuation, "}"),
        (Text.Whitespace, "\n"),
    ]

    assert tokens == [
        (Keyword, "class"),
        (Text.Whitespace, " "),
        (Name.Class, "Calendar"),
        (Punctuation, "("),
        (Name, "Component"),
        (Punctuation, ")"),
        (Punctuation, ":"),
        (Text.Whitespace, "\n"),
        (Text, "    "),
        (Name.Variable, "css"),
        (Text, " "),
        (Operator, "="),
        (Text, " "),
        (Literal.String.Doc, '"""'),
        (Text.Whitespace, "\n        "),
        # Syntax highlighting for the CSS
        (Punctuation, "."),
        (Name.Class, "calendar"),
        (Text.Whitespace, " "),
        (Punctuation, "{"),
        (Text.Whitespace, "\n            "),
        (Keyword, "background-color"),
        (Punctuation, ":"),
        (Text.Whitespace, " "),
        (Keyword.Constant, "red"),
        (Punctuation, ";"),
        (Text.Whitespace, "\n        "),
        (Punctuation, "}"),
        (Text.Whitespace, "\n    "),
        # End of the CSS
        (Literal.String.Doc, '"""'),
        (Text.Whitespace, "\n"),
        (Text, "    "),
        (Text.Whitespace, "\n"),
    ]


def test_djcpy_combined():
    code = '''
class Calendar(Component):
    template = """
        <div>Hello</div>
    """
    js = """
        console.log("Hello");
    """
    css = """
        .calendar {
            background-color: red;
        }
    """

    def get_context_data(self):
        return {
            "hello": "world",
        }
    '''
    lexer = DjangoComponentsPythonLexer()
    tokens = list(lexer.get_tokens(code))

    assert tokens == [
        (Keyword, "class"),
        (Text.Whitespace, " "),
        (Name.Class, "Calendar"),
        (Punctuation, "("),
        (Name, "Component"),
        (Punctuation, ")"),
        (Punctuation, ":"),
        (Text.Whitespace, "\n"),
        (Text, "    "),
        (Name.Variable, "template"),
        (Text, " "),
        (Operator, "="),
        (Text, " "),
        (Literal.String.Doc, '"""'),
        # HTML
        (Text, "\n        "),
        (Punctuation, "<"),
        (Name.Tag, "div"),
        (Punctuation, ">"),
        (Text, "Hello"),
        (Punctuation, "<"),
        (Punctuation, "/"),
        (Name.Tag, "div"),
        (Punctuation, ">"),
        (Text, "\n    "),
        # End of the HTML
        (Literal.String.Doc, '"""'),
        (Text.Whitespace, "\n"),
        (Text, "    "),
        (Name.Variable, "js"),
        (Text, " "),
        (Operator, "="),
        (Text, " "),
        (Literal.String.Doc, '"""'),
        # JS
        (Text, ""),
        (Text.Whitespace, "\n        "),
        (Name.Other, "console"),
        (Punctuation, "."),
        (Name.Other, "log"),
        (Punctuation, "("),
        (Literal.String.Double, '"Hello"'),
        (Punctuation, ")"),
        (Punctuation, ";"),
        (Text.Whitespace, "\n    "),
        # End of the JS
        (Literal.String.Doc, '"""'),
        (Text.Whitespace, "\n"),
        (Text, "    "),
        (Name.Variable, "css"),
        (Text, " "),
        (Operator, "="),
        (Text, " "),
        (Literal.String.Doc, '"""'),
        (Text.Whitespace, "\n        "),
        # CSS
        (Punctuation, "."),
        (Name.Class, "calendar"),
        (Text.Whitespace, " "),
        (Punctuation, "{"),
        (Text.Whitespace, "\n            "),
        (Keyword, "background-color"),
        (Punctuation, ":"),
        (Text.Whitespace, " "),
        (Keyword.Constant, "red"),
        (Punctuation, ";"),
        (Text.Whitespace, "\n        "),
        (Punctuation, "}"),
        (Text.Whitespace, "\n    "),
        (Literal.String.Doc, '"""'),
        # End of the CSS
        (Text.Whitespace, "\n"),
        (Text.Whitespace, "\n"),
        (Text, "    "),
        # get_context_data
        (Keyword, "def"),
        (Text.Whitespace, " "),
        (Name.Function, "get_context_data"),
        (Punctuation, "("),
        (Name.Builtin.Pseudo, "self"),
        (Punctuation, ")"),
        (Punctuation, ":"),
        (Text.Whitespace, "\n"),
        (Text, "        "),
        (Keyword, "return"),
        (Text, " "),
        (Punctuation, "{"),
        (Text.Whitespace, "\n"),
        (Text, "            "),
        (Literal.String.Double, '"'),
        (Literal.String.Double, "hello"),
        (Literal.String.Double, '"'),
        (Punctuation, ":"),
        (Text, " "),
        (Literal.String.Double, '"'),
        (Literal.String.Double, "world"),
        (Literal.String.Double, '"'),
        (Punctuation, ","),
        (Text.Whitespace, "\n"),
        (Text, "        "),
        (Punctuation, "}"),
        (Text.Whitespace, "\n"),
        # End of the get_context_data
        (Text, "    "),
        (Text.Whitespace, "\n"),
    ]


def test_djcpy_type_hints():
    code = '''
class Calendar(Component):
    template: types.html = """
        <div>Hello</div>
    """
    '''
    lexer = DjangoComponentsPythonLexer()
    tokens = list(lexer.get_tokens(code))

    assert tokens == [
        (Keyword, "class"),
        (Text.Whitespace, " "),
        (Name.Class, "Calendar"),
        (Punctuation, "("),
        (Name, "Component"),
        (Punctuation, ")"),
        (Punctuation, ":"),
        (Text.Whitespace, "\n"),
        (Text, "    "),
        (Name.Variable, "template"),
        (Punctuation, ":"),
        (Text, " "),
        (Name.Class, "types.html"),
        (Text, " "),
        (Operator, "="),
        (Text, " "),
        (Literal.String.Doc, '"""'),
        (Text, "\n        "),
        # Syntax highlighting for the HTML
        (Punctuation, "<"),
        (Name.Tag, "div"),
        (Punctuation, ">"),
        (Text, "Hello"),
        (Punctuation, "<"),
        (Punctuation, "/"),
        (Name.Tag, "div"),
        (Punctuation, ">"),
        # End of the HTML
        (Text, "\n    "),
        (Literal.String.Doc, '"""'),
        (Text.Whitespace, "\n"),
        (Text, "    "),
        (Text.Whitespace, "\n"),
    ]


def test_djcpy_triple_single_quotes():
    code = """
class Calendar(Component):
    template = '''
        <div>Hello</div>
    '''
    """
    lexer = DjangoComponentsPythonLexer()
    tokens = list(lexer.get_tokens(code))

    assert tokens == [
        (Keyword, "class"),
        (Text.Whitespace, " "),
        (Name.Class, "Calendar"),
        (Punctuation, "("),
        (Name, "Component"),
        (Punctuation, ")"),
        (Punctuation, ":"),
        (Text.Whitespace, "\n"),
        (Text, "    "),
        (Name.Variable, "template"),
        (Text, " "),
        (Operator, "="),
        (Text, " "),
        (Literal.String.Doc, "'''"),
        (Text, "\n        "),
        (Punctuation, "<"),
        (Name.Tag, "div"),
        (Punctuation, ">"),
        (Text, "Hello"),
        (Punctuation, "<"),
        (Punctuation, "/"),
        (Name.Tag, "div"),
        (Punctuation, ">"),
        (Text, "\n    "),
        (Literal.String.Doc, "'''"),
        (Text.Whitespace, "\n"),
        (Text, "    "),
        (Text.Whitespace, "\n"),
    ]
