"""
This file contains the operand class.   
"""
from formula_component import FormulaComponent
from value import Value
import abc

class Operand(FormulaComponent):
    """
    This class is an interface for the arguments.
    The method must be implemented in the subclasses.
    """

    @abc.abstractmethod
    def get_value_as_operand(self):
        """
        This method returns the values of the argument.
        """
        pass
    