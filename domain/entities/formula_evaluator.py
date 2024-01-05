"""
This file contains the formula evaluator class and its subclasses. 
"""
from formula_component import Parenthesis
from formula_operator import Operator
from domain.utils.tokenizer import Tokenizer
from domain.utils.parser import Parser
import abc
from value import NumericalValue
from domain.utils.shunting_yard_algorithm import ShuntingYard


class FormulaEvaluator(abc.ABC):
    """
    This is an abstract class represents a formula evaluator.
    """
    def __init__(self) -> None:
        self.tokenizer = Tokenizer()
        self.parser = Parser()
        self.shunting_yard = ShuntingYard()
        # self.dependency_manager = DependencyManager()

    def generate_expression(self, formula: str) -> list:
        """
        This method generates the expression from the formula.

        Keyword arguments:
        formula -- the formula to be evaluated (str)
        return -- the list of tokens (list)
        """
        tokens = self.tokenizer.tokenize(formula)
        tokens = self.parser.parse(tokens)
        # TODO: Manage dependencies
        return tokens

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

    def __init__(self) -> None:
        super().__init__()

    def evaluate_expression(self, formula: list) -> float:
        """
        This method evaluates the formula.

        Keyword arguments:
        formula -- the formula to be evaluated (str)
        return -- the result of the evaluation (float)
        """
        expression = self.convert_to_formula_components(formula)
        expression = self.shunting_yard.generate_postfix_expression(expression)
        return self.shunting_yard.evaluate_postfix_expression(expression)
        pass

    def convert_to_formula_components(self, tokens: list) -> list:
        """
        This method converts the list of tokens to a list of FormulaComponent objects.
        """
        pass  # Todo: Aquesta funció ha de convertir els tokens a FormulaComponent objects


if __name__ == "__main__":
    # Test generate_postfix_expression()
    expr = [Parenthesis(opens=True), NumericalValue(5), Operator("*"), NumericalValue(4), Operator("+"),
            NumericalValue(3), Operator("*"), NumericalValue(2), Parenthesis(opens=False), Operator("-"),
            NumericalValue(1)]
    f = FormulaEvaluatorPostfix()
    postfix_expr = f.shunting_yard.generate_postfix_expression(expr)
    for item in postfix_expr:
        try:
            print(item.value)
        except AttributeError:
            try:
                print(type(item))
            except AttributeError:
                print("()")
