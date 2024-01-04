"""
This file contains the formula evaluator class and its subclasses. 
"""
from spreadsheet import Spreadsheet
from cell import CellIdentifier
from content import Formula
from value import NumericalValue
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
        token_list_no_cell_id = self.translate_cell_identifiers(parsed_token_list)  # Translate cell identifiers
        result = self._shunting_yard.evaluate_shunting_yard(token_list_no_cell_id)  # Third step, evaluate shunting yard
        return result

    def cell_identifier_to_value(self, cell_identifier: CellIdentifier):
        """
        This method translates the cell identifier to the numerical value.

        Keyword arguments:
        cell_identifier -- the cell identifier (CellIdentifier)
        return -- the numerical value (float)
        """
        if not isinstance(cell_identifier, CellIdentifier):
            raise TypeError("Invalid cell identifier")
        cell = self._spreadsheet.get_cell(cell_identifier)
        if not isinstance(cell.content.value, NumericalValue):
            raise TypeError("Invalid cell content: Not a numerical value")
        return cell.content.value.value  # Return the numerical value

    def translate_cell_identifiers(self, token_list: list) -> list:
        """
        This method changes the cell identifiers in the token list to the numerical values.
        It returns the same token list but instead of the cell identifiers it has the numerical values.

        Keyword arguments:
        token_list -- the token list (list)
        return -- the cell identifier list (list)
        """
        if not isinstance(token_list, list):
            raise TypeError("Invalid token list")
        return_list = []
        for token in token_list:
            if token.type == TokenType.CELL_IDENTIFIER:
                value = self.cell_identifier_to_value(token.value)
                new_token = Token(TokenType.NUMBER, value)
                return_list.append(new_token)
            else:
                return_list.append(token)
        return return_list

