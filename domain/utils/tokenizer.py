"""
This file contains the tokenizer, Token and TokenType classes.
"""
from enum import Enum
import re

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


class TokenType(Enum):
    """
    This class is an enum that represents the token type.
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


class Token:
    """
    This class represents a token.
    """

    def __init__(self, token_type: TokenType, value: str):
        """
        This method initializes the token.

        Keyword arguments:
        type -- the type of the token (TokenType)
        value -- the value of the token (str)
        """

        self.type = token_type
        self.value = value


class Tokenizer:
    """
    This class represents a tokenizer.
    The first step consists in breaking the string representing the formula in a sequence of
    TOKENS. Each token shall be a sequence of one or more characters that represents a basic entity in the
    expression of the formula. For the formulas in a spreadsheet they are: operator, cell identifier,
    number, opening round bracket, closing round bracket, colon character, semicolon character, comma,
    function name, and range.
    """

    def __init__(self):
        """
        This method initializes the tokenizer.

        Attributes:
        tokens -- the list of tokens (list)
        current_token_index -- the current token index (int)
        """
        self._tokens = []
        self._current_token_index = 0

    @staticmethod
    def tokenize(formula_string: str):
        """
        Generate tokens from the string s as instances of the Token class.

        Keyword arguments:
        formula_string -- the string to tokenize (str)
        return -- the list of tokens (list)
        """
        for match in _TOKEN_RE.finditer(formula_string):
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
