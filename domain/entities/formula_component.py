"""
This file contains the formula component class.
"""
import abc

class FormulaComponent(abc.ABC):
    """
    This is an abstract class that represents a formula component.
    """
    @abc.abstractmethod
    def __init__(self):
        """
        This method initializes the formula component.
        """
        pass

class Parenthesis(FormulaComponent):
    """
    This class represents a parenthesis.
    """
    def __init__(self, opens: bool) -> None:
        """
        This method initializes the parenthesis.
        """
        self._opens = opens
    
    def opens(self) -> bool:
        """
        This method returns whether the parenthesis opens or closes.
        """
        return self._opens