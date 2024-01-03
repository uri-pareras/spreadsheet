"""
This file contains the formula evaluator utils.
Tokenizer, parser and dependency manager are implemented here.
"""

from enum import Enum
import re

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
    """
    This class represents a token.
    """

    def __init__(self, type: TokenType, value: str):
        """
        This method initializes the token.

        Keyword arguments:
        type -- the type of the token (TokenType)
        value -- the value of the token (str)
        """

        self.type = type
        self.value = value

class Tokenizer():
    """
    This class represents a tokenizer.
    The first step consists in breaking the string representing the formula in a sequence of
    TOKENS. Each token shall be a sequence of one or more characters that represents a basic entity in the
    expression of the formula. For the formulas in a spreadsheet they are: operator, celll identifier,
    number, opening round bracket, closing round bracket, colon character, semi-colon character, comma,
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

    def tokenize(self, s: str):
        """
        Generate tokens from the string s as instances of the Token class.

        Keyword arguments:
        s -- the string to tokenize (str)
        """
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


class Parser():
    """
    This class represents a parser.
    This step takes the sequence of tokens built in step 1 and checks that the sequence meets
    the syntactical rules of regular arithmetic expressions. If there are no errors,
    the output of this process is the same sequence of tokens generated by the tokenizer.
    """

    def __init__(self, tokens: list):
        """
        This method initializes the parser.

        Attributes:
        tokens -- the list of tokens (list)
        current_token -- the current token (Token)
        token_index -- the current token index (int)
        """
        if len(tokens) == 0:
            raise SyntaxError("Empty formula")
        self.tokens = tokens
        self.current_token = None
        self.token_index = -1
        self.advance()

    def advance(self):
        """
        Advance the current token index and set the current token.
        """
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            self.current_token = None

    def parse(self):
        """
        Parse the list of tokens and check the syntactical rules.
        If there are no errors, return the same list of tokens.

        Returns:
        tokens -- the list of tokens (list)
        """

        self.expression()
        return self.tokens

    def expression(self):
        """
        This method checks the syntactical rules of the expression.
        expression -> term { ( '+' | '-' ) term }
        """
        self.term()
        while self.current_token and self.current_token.value in ('+', '-'):
            self.advance()
            self.term()

    def term(self):
        """
        This method checks the syntactical rules of the term.
        term -> factor { ( '*' | '/' ) factor }
        """
        self.factor()
        while self.current_token and self.current_token.value in ('*', '/'):
            self.advance()
            self.factor()

    def factor(self):
        """
        This method checks the syntactical rules of the factor.
        factor -> NUMBER | '(' expression ')' | FUNCTION '(' expression ')' | CELL_IDENTIFIER
        """
        if self.current_token and self.current_token.type == TokenType.NUMBER:
            self.advance()
        elif self.current_token and self.current_token.type == TokenType.OPENING_PARENTHESIS:
            self.advance()
            self.expression()
            if self.current_token and self.current_token.type == TokenType.CLOSING_PARENTHESIS:
                self.advance()
            else:
                raise SyntaxError("Expected closing parenthesis")
        
        elif self.current_token and self.current_token.type == TokenType.FUNCTION:  #Function synthax comprobation.
            self.advance()
            if self.current_token and self.current_token.type == TokenType.OPENING_PARENTHESIS:
                self.advance()
                if self.current_token and self.current_token.type == TokenType.CELL_IDENTIFIER or self.current_token.type == TokenType.NUMBER:
                    self.advance()
                    if self.current_token and self.current_token.type == TokenType.COLON:
                        self.advance()
                        if self.current_token and self.current_token.type == TokenType.CELL_IDENTIFIER or self.current_token.type == TokenType.NUMBER:
                            self.advance()
                        else:
                            raise SyntaxError("Expected cell identifier")
                    else:
                        raise SyntaxError("Expected colon")
                else:
                    raise SyntaxError("Expected cell identifier")
                if self.current_token and self.current_token.type == TokenType.CLOSING_PARENTHESIS:
                    self.advance()
                else:
                    raise SyntaxError("Expected closing parenthesis")
            else:
                raise SyntaxError("Expected opening parenthesis")
        elif self.current_token and self.current_token.type == TokenType.CELL_IDENTIFIER:
            self.advance()
        else:
            raise SyntaxError("Invalid factor")

# Example usage:
tokenizer = Tokenizer()
string_to_parse = "A1 + MAX(5:8) * (10 - 4)"
tokens = list(tokenizer.tokenize(string_to_parse))
parser = Parser(tokens)
result = parser.parse()
for token in result:
    print(token.value)

string_to_parse = "AB1 + PROMEDIO(5:8) * (D3 - 4) / C3 * P0"
tokens = list(tokenizer.tokenize(string_to_parse))
parser = Parser(tokens)
result = parser.parse()
for token in result:
    print(token.value)