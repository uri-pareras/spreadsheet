"""
This file contains the formula evaluator class and its subclasses. 
"""
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
