"""
This file contains the formula evaluator class and its subclasses. 
"""
from formula_component import FormulaComponent
from formula_operator import Operator
from operand import Operand
import abc

class FormulaEvaluator(abc.ABC):
    """
    This is an abstract class represents a formula evaluator.
    """

    @abc.abstractmethod
    def evaluate(self, formula: str) -> float:
        """
        This method evaluates the formula.

        Keyword arguments:
        formula -- the formula to be evaluated (str)
        return -- the result of the evaluation (float)
        """
        pass