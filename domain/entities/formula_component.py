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
