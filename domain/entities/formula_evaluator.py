"""
This file contains the formula evaluator class and its subclasses. 
"""
from domain.entities.formula_component import Parenthesis
from domain.entities.formula_operator import Operator
from domain.utils.tokenizer import Tokenizer
from domain.utils.parser import Parser
import abc
from domain.entities.value import NumericalValue
from domain.entities.spreadsheet import Spreadsheet
from domain.entities.cell import CellIdentifier
from domain.entities.range import Range
from domain.utils.tokenizer import TokenType, Token
from domain.entities.function import Suma, Max, Min, Promedio
from domain.utils.shunting_yard_algorithm import ShuntingYard
from domain.utils.dependency_manager import DependencyManager
from domain.entities.cell import Cell
from domain.entities.content import Formula, NumericalContent
# from domain.exceptions.exceptions import CircularDependencyException, ContentException
from entities.circular_dependency_exception import CircularDependencyException
from entities.content_exception import ContentException


class FormulaEvaluator(abc.ABC):
    """
    This is an abstract class represents a formula evaluator.
    """
    def __init__(self, spreadsheet: Spreadsheet) -> None:
        self.spreadsheet = spreadsheet
        self.tokenizer = Tokenizer()
        self.parser = Parser()
        self.shunting_yard = ShuntingYard()
        self.dependency_manager = DependencyManager(spreadsheet)

    def convert_to_formula_components(self, tokens: list) -> list:
        """
        This method converts the list of tokens to a list of FormulaComponent objects.

        Keyword arguments:
        tokens -- the list of tokens (list)
        return -- the list of FormulaComponent objects (list)
        """

        def create_function(tokens: list, i: int) -> tuple:
            """
            This method creates a function from the list of tokens passed as argument.

            Keyword arguments:
            tokens -- the list of tokens (list)
            i -- the current index iterating the tokens list(int)
            return -- the function object (Function)
            """

            # Save function type
            func_type = tokens[i].value

            # Skip the parenthesis after the function name
            if tokens[i + 1].type == TokenType.OPENING_PARENTHESIS:
                i += 2
            else:
                raise ContentException("Expected opening parenthesis after function name.")

            # Obtain arguments
            arguments = []
            while tokens[i].type != TokenType.CLOSING_PARENTHESIS:
                argument = []
                while tokens[i].type != TokenType.SEMICOLON and tokens[i].type != TokenType.CLOSING_PARENTHESIS:
                    if tokens[i].type == TokenType.NUMBER:
                        argument.append(NumericalValue(float(tokens[i].value)))
                    elif tokens[i].type == TokenType.OPERATOR:
                        raise ContentException("Operators are not allowed in function arguments.")
                    elif tokens[i].type == TokenType.OPENING_PARENTHESIS or tokens[
                        i].type == TokenType.CLOSING_PARENTHESIS:
                        raise ContentException("Operations are not allowed in function arguments.")
                    elif tokens[i].type == TokenType.CELL_IDENTIFIER:
                        c = self.spreadsheet.get_cell(CellIdentifier(tokens[i].value))
                        if c is not None:
                            argument.append(c)
                        else:  # if it doesn't exist, create it. Dependency manager will take care of the rest
                            self.spreadsheet.add_cell(Cell(CellIdentifier(tokens[i].value), NumericalContent(NumericalValue(None))))
                            argument.append(self.spreadsheet.get_cell(CellIdentifier(tokens[i].value)))
                    elif tokens[i].type == TokenType.COLON:
                        start_arg_cell_id = argument.pop(-1).identifier
                        end_arg_cell_id = CellIdentifier(tokens[i + 1].value)
                        i += 1
                        if isinstance(start_arg_cell_id, CellIdentifier) and isinstance(end_arg_cell_id, CellIdentifier):
                            argument.append(Range(start_arg_cell_id, end_arg_cell_id, self.spreadsheet))
                        else:
                            raise ContentException("The start and end of the range must be cells.")
                    elif tokens[i].type == TokenType.FUNCTION:
                        func, i = create_function(tokens, i)
                        argument.append(func)
                    else:
                        raise ContentException("Invalid expression.")
                    i += 1
                if argument: arguments.append(argument.pop(-1))
                if i < (len(tokens) - 1) and tokens[i].type != TokenType.CLOSING_PARENTHESIS: i += 1

            # Create function object
            if func_type == "SUMA":
                return Suma(arguments), i
            elif func_type == "MAX":
                return Max(arguments), i
            elif func_type == "MIN":
                return Min(arguments), i
            elif func_type == "PROMEDIO":
                return Promedio(arguments), i

        # Convert tokens to FormulaComponent objects
        i = 0
        components = []
        while i < len(tokens):
            if tokens[i].type == TokenType.NUMBER:
                components.append(NumericalValue(float(tokens[i].value)))
            elif tokens[i].type == TokenType.OPERATOR:
                components.append(Operator(tokens[i].value))
            elif tokens[i].type == TokenType.OPENING_PARENTHESIS:
                components.append(Parenthesis(opens=True))
            elif tokens[i].type == TokenType.CLOSING_PARENTHESIS:
                components.append(Parenthesis(opens=False))
            elif tokens[i].type == TokenType.CELL_IDENTIFIER:
                cell = self.spreadsheet.get_cell(CellIdentifier(tokens[i].value))
                if cell is not None:
                    components.append(cell)
                else:  # if it doesn't exist, create it. Dependency manager will take care of the rest
                    self.spreadsheet.add_cell(Cell(CellIdentifier(tokens[i].value), NumericalContent(NumericalValue(None))))
                    components.append(self.spreadsheet.get_cell(CellIdentifier(tokens[i].value)))
            elif tokens[i].type == TokenType.COLON:
                start_cell_id = components.pop(-1)
                end_cell_id = self.spreadsheet.get_cell(CellIdentifier(tokens[i + 1].value))
                i += 1
                if isinstance(start_cell_id, CellIdentifier) and isinstance(end_cell_id, CellIdentifier):
                    components.append(Range(start_cell_id, end_cell_id, self.spreadsheet))
                else:
                    raise ContentException("The start and end of the range must be cells.")
            elif tokens[i].type == TokenType.FUNCTION:
                func, i = create_function(tokens, i)
                components.append(func)
            else:
                raise ContentException("Invalid expression.")
            i += 1

        return components

    def generate_expression(self, formula_cell: Cell):
        """
        This method generates the expression from the formula.

        Keyword arguments:
        formula -- the formula to be evaluated (str)
        return -- the list of tokens (list)
        """

        tokens = list(self.tokenizer.tokenize(formula_cell.content.textual_representation))
        tokens = self.parser.parse(tokens)
        expression = self.convert_to_formula_components(tokens)
        self.dependency_manager.remove_old_dependencies(formula_cell)
        formula_cell.depends_on = self.dependency_manager.get_dependencies(expression)
        self.dependency_manager.update_depends_on_me_lists(formula_cell.identifier, formula_cell.depends_on)
        self.dependency_manager.detect_circular_dependencies(formula_cell.identifier, formula_cell)
        formula_cell.content.expression = expression

    @abc.abstractmethod
    def evaluate_expression(self, formula: Cell):
        """
        This method evaluates the formula.

        Keyword arguments:
        formula -- the formula to be evaluated (str)
        return -- the result of the evaluation (float)
        """
        pass


class FormulaEvaluatorPostfix(FormulaEvaluator):
    """
    This class represents a postfix formula evaluator.
    """

    def __init__(self,  spreadsheet: Spreadsheet) -> None:
        super().__init__(spreadsheet)

    def evaluate_expression(self, formula: Cell):
        """
        This method evaluates the formula.

        Keyword arguments:
        formula -- the formula to be evaluated (str)
        return -- the result of the evaluation (float)
        """

        postfix = self.shunting_yard.generate_postfix_expression(formula.content.expression)
        formula.content.value = NumericalValue(self.shunting_yard.evaluate_postfix_expression(postfix))
        pass


if __name__ == "__main__":
    # Test generate_postfix_expression()
    s = Spreadsheet()
    fe = FormulaEvaluatorPostfix(s)
    s.add_cell("B1", "5")
    s.add_cell("B2", "3")

    s.add_cell("D2", "=4-B2")
    fe.generate_expression(s.get_cell(CellIdentifier("D2")))
    fe.evaluate_expression(s.get_cell(CellIdentifier("D2")))

    s.add_cell("A1","=(B1*D2+3*2)-MAX(4;MIN(B1:C2))")
    fe.generate_expression(s.get_cell(CellIdentifier("A1")))
    fe.evaluate_expression(s.get_cell(CellIdentifier("A1")))

    s.add_cell("D3","=A1")
    fe.generate_expression(s.get_cell(CellIdentifier("D3")))
    fe.evaluate_expression(s.get_cell(CellIdentifier("D3")))

    # for item in postfix_expr:
    #     try:
    #         print(item.value)
    #     except AttributeError:
    #         try:
    #             print(item._type)
    #         except AttributeError:
    #             print("()")
    print("RESULTS:")
    print("A1:", s.get_cell(CellIdentifier("A1")).content.value.value)
    print("B1:", s.get_cell(CellIdentifier("B1")).content.value.value)
    print("B2:", s.get_cell(CellIdentifier("B2")).content.value.value)
    print("D2:", s.get_cell(CellIdentifier("D2")).content.value.value)
    print("D3:", s.get_cell(CellIdentifier("D3")).content.value.value)

    ### Test Dependency Manager
    # s = Spreadsheet()
    # fe = FormulaEvaluatorPostfix(s)
    # s.add_cell(Cell(CellIdentifier("B1"), NumericalContent(NumericalValue(1))))
    # s.add_cell(Cell(CellIdentifier("B2"), Formula("B1+1")))
    # s.add_cell(Cell(CellIdentifier("B3"), Formula("4-B2 + MAX(E1:F5)")))
    # s.add_cell(Cell(CellIdentifier("B4"), Formula("B3")))
    # fe.generate_expression(s.get_cell(CellIdentifier("B2")))
    # fe.generate_expression(s.get_cell(CellIdentifier("B3")))
    # fe.generate_expression(s.get_cell(CellIdentifier("B4")))
    # fe.evaluate_expression(s.get_cell(CellIdentifier("B2")))
    # print("B1 depends on me:")
    # [print(d.coordinate, end=' ') for d in s.get_cell(CellIdentifier("B1")).depends_on_me]
    # print()
    # fe.evaluate_expression(s.get_cell(CellIdentifier("B3")))
    # print("B2 depends on me:")
    # [print(d.coordinate, end=' ') for d in s.get_cell(CellIdentifier("B2")).depends_on_me]
    # print()
    # fe.evaluate_expression(s.get_cell(CellIdentifier("B4")))
    # print("B3 depends on me:")
    # [print(d.coordinate, end=' ') for d in s.get_cell(CellIdentifier("B3")).depends_on_me]
    # print()
    # s.get_cell(CellIdentifier("B2")).content = Formula("B4")
    # fe.generate_expression(s.get_cell(CellIdentifier("B2")))
    # fe.evaluate_expression(s.get_cell(CellIdentifier("B2")))
    # print("CIRCULARITY")
    # print("B1 depends on me:")
    # [print(d.coordinate, end=' ') for d in s.get_cell(CellIdentifier("B1")).depends_on_me]
    # print()
    # fe.evaluate_expression(s.get_cell(CellIdentifier("B3")))
    # print("B2 depends on me:")
    # [print(d.coordinate, end=' ') for d in s.get_cell(CellIdentifier("B2")).depends_on_me]
    # print()
    # fe.evaluate_expression(s.get_cell(CellIdentifier("B4")))
    # print("B3 depends on me:")
    # [print(d.coordinate, end=' ') for d in s.get_cell(CellIdentifier("B3")).depends_on_me]
    # print()
