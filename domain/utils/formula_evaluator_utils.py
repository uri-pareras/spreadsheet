"""
This file contains the formula evaluator utils.
Tokenizer, parser and dependency manager are implemented here.
"""

from enum import Enum
import re

class TokenType(Enum):
    """
    This class represents the token type.
    """
    OPERATOR = 1
    CELL_IDENTIFIER = 2
    NUMBER = 3
    OPENING_PARENTHESIS = 4
    CLOSING_PARENTHESIS = 5
    COLON = 6
    SEMICOLON = 7
    COMMA = 8
    FUNCTION = 9

_TOKEN_RE = re.compile(r'''
    \s*(?:              # Optional whitespace, followed by one of:
    ([+*/-])         # Punctuation or operator
    |([a-z]+[0-9]+|[A-Z]+[0-9]+:[A-Z]+[0-9]+)  # Cell Identifier or Range
    |([0-9]+(?:\.[0-9]*)?) # Number
    |(\()               # Opening parenthesis
    |(\))               # Closing parenthesis
    |(:)                # Colon
    |(;)                # Semicolon
    |(,)                # Comma
    |(MAX|MIN|SUMA|PROMEDIO)  # Function names
    |(\S))              # Anything else is an error
''', re.VERBOSE | re.IGNORECASE)

class Token():
    """Class representing a token."""

    def __init__(self, type: TokenType, value: str):
        self.type = type
        self.value = value

class Tokenizer():
    """
    This class represents a tokenizer.
    """
    def __init__(self):
        """
        This method initializes the tokenizer.
        """
        self._tokens = []
        self._current_token_index = 0

    def tokenize(self, s):
        """Generate tokens from the string s as instances of the Token class."""
        for match in _TOKEN_RE.finditer(s):
            operator, cell_id, number, open_paren, close_paren, colon, semicolon, comma, func, error = match.groups()
            if operator:
                yield Token(TokenType.OPERATOR, operator)
            elif cell_id:
                yield Token(TokenType.CELL_IDENTIFIER, cell_id)
            elif number:
                yield Token(TokenType.NUMBER, float(number))
            elif open_paren:
                yield Token(TokenType.OPENING_PARENTHESIS, open_paren)
            elif close_paren:
                yield Token(TokenType.CLOSING_PARENTHESIS, close_paren)
            elif colon:
                yield Token(TokenType.COLON, colon)
            elif semicolon:
                yield Token(TokenType.SEMICOLON, semicolon)
            elif comma:
                yield Token(TokenType.COMMA, comma)
            elif func:
                yield Token(TokenType.FUNCTION, func.upper())  # Converting function name to uppercase
            else:
                raise SyntaxError("Expected a token but found {!r}".format(error))

# Example usage:
tokenizer = Tokenizer()
string_to_tokenize = "AAA1:B232 + 3.14 - MAX(C4, D5)"
for token in tokenizer.tokenize(string_to_tokenize):
    print(token.type, token.value)