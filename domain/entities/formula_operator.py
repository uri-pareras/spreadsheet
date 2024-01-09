"""
This file contains the operator class.
"""
from domain.entities.formula_component import FormulaComponent


class Operator(FormulaComponent):
    """
    This is a concrete implementation of the FormulaComponent class.
    This class represents an operator.
    """

    def __init__(self, operator_type: str):
        """
        This method initializes the operator.

        Keyword arguments:
        type -- the type of the operator (str)
        """
        self._type = operator_type
        
    def compute(self, left_operand, right_operand):
        """
        This method computes the value of the operator.

        Keyword arguments:
        left_operand -- the left operand (float)
        right_operand -- the right operand (float)
        return -- the result of the computation (float)
        """
        match self._type:  # python 3.10 or newer REQUIRED TODO: Add to readme?
            case "+":
                return left_operand + right_operand
            case "-":
                return left_operand - right_operand
            case "*":
                return left_operand * right_operand
            case "/":
                return left_operand / right_operand  #Todo: check if right_operand is 0
            case _:
                raise ValueError("The operator is not valid.")
            
    def precedence(self):
        """
        This method returns the precedence of the operator.
        """
        match self._type:
            case "+":
                return 1
            case "-":
                return 1
            case "*":
                return 2
            case "/":
                return 2
            case _:
                raise ValueError("The operator is not valid.")
