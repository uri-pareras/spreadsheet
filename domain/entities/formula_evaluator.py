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
from domain.entities.content import Formula


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
                raise ValueError("Expected opening parenthesis after function name.")

            # Obtain arguments
            arguments = []
            while tokens[i].type != TokenType.CLOSING_PARENTHESIS:
                argument = []
                while tokens[i].type != TokenType.SEMICOLON:
                    if tokens[i].type == TokenType.NUMBER:
                        argument.append(NumericalValue(float(tokens[i].value)))
                    elif tokens[i].type == TokenType.OPERATOR:
                        raise ValueError("Operators are not allowed in function arguments.")
                    elif tokens[i].type == TokenType.OPENING_PARENTHESIS or tokens[
                        i].type == TokenType.CLOSING_PARENTHESIS:
                        raise ValueError("Operations are not allowed in function arguments.")
                    elif tokens[i].type == TokenType.CELL_IDENTIFIER:
                        argument.append(self.spreadsheet.get_cell(CellIdentifier(tokens[i].value)))
                    elif tokens[i].type == TokenType.COLON:
                        start_arg_cell_id = argument.pop(-1)
                        end_arg_cell_id = self.spreadsheet.get_cell(CellIdentifier(tokens[i + 1].value))
                        i += 1
                        if isinstance(start_cell_id, CellIdentifier) and isinstance(end_cell_id, CellIdentifier):
                            argument.append(Range(start_arg_cell_id, end_arg_cell_id, self.spreadsheet))
                        else:
                            raise ValueError("The start and end of the range must be cells.")
                    elif tokens[i].type == TokenType.FUNCTION:
                        func, i = create_function(tokens, i)
                        argument.append(func)
                    else:
                        raise ValueError("Invalid expression.")
                    i += 1
                arguments.append(argument.pop(-1))
            pass
            i += 1

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
                components.append(self.spreadsheet.get_cell(CellIdentifier(tokens[i].value)))
            elif tokens[i].type == TokenType.COLON:
                start_cell_id = components.pop(-1)
                end_cell_id = self.spreadsheet.get_cell(CellIdentifier(tokens[i + 1].value))
                i += 1
                if isinstance(start_cell_id, CellIdentifier) and isinstance(end_cell_id, CellIdentifier):
                    components.append(Range(start_cell_id, end_cell_id, self.spreadsheet))
                else:
                    raise ValueError("The start and end of the range must be cells.")
            elif tokens[i].type == TokenType.FUNCTION:
                func, i = create_function(tokens, i)
                components.append(func)
            else:
                raise ValueError("Invalid expression.")
            i += 1

        return components

    def generate_expression(self, formula: Cell) -> list:
        """
        This method generates the expression from the formula.

        Keyword arguments:
        formula -- the formula to be evaluated (str)
        return -- the list of tokens (list)
        """

        tokens = list(self.tokenizer.tokenize(formula.content.textual_representation))
        print(tokens)
        tokens = self.parser.parse(tokens)
        expression = self.convert_to_formula_components(tokens)
        if self.dependency_manager.detect_circular_dependencies(formula):
            raise ValueError("Circular dependencies detected.")
        return expression

    @abc.abstractmethod
    def evaluate_expression(self, formula: list) -> float:
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

    def evaluate_expression(self, formula: list) -> float:
        """
        This method evaluates the formula.

        Keyword arguments:
        formula -- the formula to be evaluated (str)
        return -- the result of the evaluation (float)
        """

        postfix_expression = self.shunting_yard.generate_postfix_expression(formula)
        return self.shunting_yard.evaluate_postfix_expression(postfix_expression)
        pass


if __name__ == "__main__":
    # Test generate_postfix_expression()
    # expr = [Parenthesis(opens=True), NumericalValue(5), Operator("*"), NumericalValue(4), Operator("+"),
    #         NumericalValue(3), Operator("*"), NumericalValue(2), Parenthesis(opens=False), Operator("-"),
    #         NumericalValue(1)]
    s = Spreadsheet()
    form_eval = FormulaEvaluatorPostfix(s)

    formula = Cell(CellIdentifier("A1"), Formula("(5*4+3*2)-1"))
    # s.add_cell(formula)
    expr = form_eval.generate_expression(formula)

    # tokens_list = [Token(TokenType.OPENING_PARENTHESIS,"("), Token(TokenType.NUMBER,"5"),
    #                Token(TokenType.OPERATOR,"*"), Token(TokenType.NUMBER, "4"), Token(TokenType.OPERATOR, "+"),
    #                Token(TokenType.NUMBER,"3"), Token(TokenType.OPERATOR,"*"),
    #                Token(TokenType.NUMBER,"2"),Token(TokenType.CLOSING_PARENTHESIS, ")"),
    #                Token(TokenType.OPERATOR,"-"), Token(TokenType.OPERATOR,"1")]
    # expr = f.convert_to_formula_components(tokens_list)
    postfix_expr = form_eval.shunting_yard.generate_postfix_expression(expr)
    for item in postfix_expr:
        try:
            print(item.value)
        except AttributeError:
            try:
                print(item._type)
            except AttributeError:
                print("()")
    print("RESULT:")
    print(form_eval.evaluate_expression(expr))
