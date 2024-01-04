"""
This file contains the formula evaluator class and its subclasses. 
"""
from spreadsheet import Spreadsheet
from content import Formula
from domain.utils.parser import Tokenizer, Parser, TokenType, Token
from domain.utils.shunting_yard_algorithm import ShuntingYard


class FormulaEvaluator:
    """
    This class represents the formula evaluator.
    It is the class that handles the tokenizer, parser and shunting yard algorithm.
    This class also translates the cell identifiers to the numerical values.
    """
    def __init__(self, spreadsheet: Spreadsheet):
        """
        This method initializes the formula evaluator.

        Keyword arguments:
        spreadsheet -- the spreadsheet (Spreadsheet)
        """
        if not isinstance(spreadsheet, Spreadsheet):
            raise TypeError("Invalid spreadsheet")
        self._spreadsheet = spreadsheet
        self._tokenizer = Tokenizer()
        self._parser = Parser()
        self._shunting_yard = ShuntingYard()

    def evaluate(self, formula: str) -> float:
        """
        This method evaluates the formula.

        Keyword arguments:
        formula -- the formula to be evaluated (str)
        return -- the result of the evaluation (float)
        """
        token_list = self._tokenizer.tokenize(formula)  # First step, tokenize the formula
        parsed_token_list = self._parser.parse(token_list)  # Second step, parse the token list
        result = self._shunting_yard.evaluate_shunting_yard(parsed_token_list)  # Third step, evaluate the shunting yard
        return result

