"""
This file contains the operand interface.   
"""
from formula_component import FormulaComponent
import abc

class Operand(FormulaComponent):  #TODO: Perque hereta de FormulaComponent?
    """
    This class is an interface for the arguments.
    The method must be implemented in the subclasses.
    """

    @abc.abstractmethod
    def get_value_as_operand(self):
        """
        This method returns the values of the argument as an operand.
        """
        pass
    
