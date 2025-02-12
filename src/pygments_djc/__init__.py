from pygments.lexers import LEXERS

# Public API
from pygments_djc.lexers import DjangoComponentsPythonLexer

__all__ = ["DjangoComponentsPythonLexer"]


# Register the Lexer. Unfortunately Pygments doesn't support registering a Lexer
# without it living in the pygments codebase.
# See https://github.com/pygments/pygments/issues/1096#issuecomment-1821807464
LEXERS["DjangoComponentsPythonLexer"] = (
    "pygments_djc",
    "Django Components Python",
    # The aliases of the Lexer - This means that code blocks like
    # ```djc_py
    # ```
    # will be highlighted by this Lexer.
    ["djc_py", "djc_python"],
    [],
    [],
)
