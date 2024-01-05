"""
This file contains the formula evaluator class and its subclasses. 
"""
from formula_component import FormulaComponent, Parenthesis
from formula_operator import Operator
from operand import Operand
from domain.utils.tokenizer import Tokenizer, Token, TokenType
from domain.utils.parser import Parser
import abc
from value import NumericalValue


class FormulaEvaluator(abc.ABC):
    """
    This is an abstract class represents a formula evaluator.
    """
    def __init__(self) -> None:
        self.tokenizer = Tokenizer()
        self.parser = Parser()
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
        #TODO: Manage dependencies
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
        expression = self.generate_postfix_expression(expression)
        return self.evaluate_postfix_expression(expression)
        pass

    def convert_to_formula_components(self, tokens: list) -> list:
        '''
        This method converts the list of tokens to a list of FormulaComponent objects.
        '''
        pass  # Todo: Aquesta funció ha de convertir els tokens a FormulaComponent objects


    def generate_postfix_expression(self, expression: list) -> list:
        """
        This method generates the postfix expression from the list of FormulaComponent
        objects passed as argument. It uses the Shunting-yard algorithm, and outputs
        a list of FormulaComponent objects. This list alternates between Operand
        and Operator objects.

        Keyword arguments:
        expression -- the list of FormulaComponent objects (list of FormulaComponent objects
        return -- the postfix expression (list of FormulaComponent objects)
        """
        output = []
        stack = []
        for component in expression:
            if isinstance(component,Operand):
                output.append(component)
            elif isinstance(component, Operator):
                while stack and isinstance(stack[-1],Operator):
                    if component.precedence() <= stack[-1].precedence():
                        output.append(stack.pop())
                    else:
                        break
                stack.append(component)
            elif isinstance(component, Parenthesis) and component.opens():
                stack.append(component)
            elif isinstance(component, Parenthesis) and not component.opens():
                while stack and isinstance(stack[-1],Parenthesis) and stack[-1].opens():
                    output.append(stack.pop())
                stack.pop()

        return output + stack[::-1]


    def evaluate_postfix_expression(self, expression: list) -> float:
        """
        This method evaluates the postfix expression passed as argument.
        """
        stack = []
        for component in expression:
            if isinstance(component,Operand):
                stack.append(component)
            elif isinstance(component,Operator):
                operand2 = stack.pop().get_value_as_operand()
                operand1 = stack.pop().get_value_as_operand()
                stack.append(component.compute(operand1,operand2))
        return stack.pop().value


if __name__ == "__main__":
    # Test generate_postfix_expression()
    expr = [Parenthesis(opens=True),NumericalValue(5), Operator("*"), NumericalValue(4), Operator("+"),
            NumericalValue(3), Operator("*"), NumericalValue(2), Parenthesis(opens=False), Operator("-"), NumericalValue(1)]
    f = FormulaEvaluatorPostfix()
    postfix_expr = f.generate_postfix_expression(expr)
    for item in postfix_expr:
        try:
            print(item.value)
        except AttributeError:
            try:
                print(item._type)
            except AttributeError:
                print("()")
