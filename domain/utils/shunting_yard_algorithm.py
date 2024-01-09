"""
This file contains the shunting yard algorithm class implementation.
"""
from domain.entities.formula_component import Parenthesis
from domain.entities.operand import Operand
from domain.entities.formula_operator import Operator
from domain.entities.value import NumericalValue


class ShuntingYard:
    """
    This class implements the shunting yard algorithm.
    It implements the following methods:
    - generate_postfix_expression: generates the postfix expression from the list of FormulaComponent
    - evaluate_postfix_expression: evaluates the postfix expression
    """

    @staticmethod
    def generate_postfix_expression(expression: list) -> list:
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
            if isinstance(component, Operand):
                output.append(component)
            elif isinstance(component, Parenthesis) and component.opens():
                stack.append(component)
            elif isinstance(component, Parenthesis) and not component.opens():
                while stack and not (isinstance(stack[-1], Parenthesis) and stack[-1].opens()):
                    output.append(stack.pop())
                stack.pop()
            elif isinstance(component, Operator):
                while stack and not (isinstance(stack[-1], Parenthesis) and stack[-1].opens())\
                        and component.precedence() <= stack[-1].precedence():
                    output.append(stack.pop())
                stack.append(component)
        while stack:
            output.append(stack.pop())  # Don't return the parenthesis
        return output

    @staticmethod
    def evaluate_postfix_expression(expression: list) -> float:
        """
        This method evaluates the postfix expression passed as argument.
        It returns the result of the evaluation.

        Keyword arguments:
        expression -- the postfix expression (list of FormulaComponent objects)
        return -- the result of the evaluation (float)
        """
        stack = []
        for component in expression:
            if isinstance(component, Operand):
                stack.append(component)
            elif isinstance(component, Operator):
                operand2 = stack.pop().get_value_as_operand()
                operand1 = stack.pop().get_value_as_operand()
                stack.append(NumericalValue(component.compute(operand1, operand2)))
        return stack.pop().get_value_as_operand()
