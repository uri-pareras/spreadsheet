"""
This file contains the operator class.
"""
from formula_component import FormulaComponent

class Operator(FormulaComponent):
    """
    This is a concrete implementation of the FormulaComponent class.
    This class represents an operator.
    """

    def __init__(self, type: str):
        """
        This method initializes the operator.

        Keyword arguments:
        type -- the type of the operator (str)
        """
        self._type = type
        
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
                return left_operand / right_operand
            case _:
                raise ValueError("The operator is not valid.")
