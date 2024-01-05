"""
This file contains the formula evaluator class and its subclasses. 
"""
from formula_component import FormulaComponent, Parenthesis
from formula_operator import Operator
from domain.utils.tokenizer import Tokenizer, Token, TokenType
from domain.utils.parser import Parser
from operand import Operand
import abc

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
    def evaluate(self, formula: list) -> float:
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

    def convert_to_formula_components(tokens: list) -> list:
        '''
        This method converts the list of tokens to a list of FormulaComponent objects.
        '''


    def generate_postfix_expression(expression: list) -> list:
        '''
        This method generates the postfix expression from the list of FormulaComponent
        objects passed as argument. It uses the Shunting-yard algorithm, and outputs
        a list of FormulaComponent objects. This list alternates between Operand
        and Operator objects.
        '''
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

from value import NumericalValue
# Test generate_postfix_expression()
expr = [NumericalValue(1), Operator("+"), NumericalValue(2), Operator("*"), NumericalValue(3)]
f = FormulaEvaluatorPostfix()
print(f.generate_postfix_expression(expr))
