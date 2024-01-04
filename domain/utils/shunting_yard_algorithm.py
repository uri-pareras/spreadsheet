"""
This file contains the shunting yard algorithm class implementation.
"""

from domain.entities.formula_evaluator import FormulaEvaluator
from parser import TokenType


class ShuntingYard:
    """
    This class implements the shunting yard algorithm.
    """

    def __init__(self):
        """
        This method initializes the shunting yard algorithm.
        """
        self._output_queue = []
        self._operator_stack = []

    def clean(self):
        """
        This method cleans the shunting yard algorithm.
        """
        self._output_queue = []
        self._operator_stack = []

    def evaluate_shunting_yard(self, token_list: list):
        """
        Given a token list this method evaluates the shunting yard algorithm.
        This will return the result of the computation.

        Keyword arguments:
        token_list -- the token list (list of tokens)
        return -- the result of the computation (float)
        """
        """self.clean()
        for token in token_list:
            if token.type == TokenType.NUMBER:   # We will only have numbers
                self._output_queue.append(token)
            elif token.type == TokenType.OPERATOR:
                self._operator_stack.append(token)
            elif token.type == TokenType.OPENING_PARENTHESIS:
                self._operator_stack.append(token)
            elif token.type == TokenType.CLOSING_PARENTHESIS:
                while self._operator_stack[-1].type != TokenType.OPENING_PARENTHESIS:
                    self._output_queue.append(self._operator_stack.pop())
                self._operator_stack.pop()
            else:
                raise SyntaxError("Invalid token")"""
        pass
