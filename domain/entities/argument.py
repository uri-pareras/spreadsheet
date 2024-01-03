"""
This file contains the argument class.
"""

import abc

class Argument(abc.ABC):
    """
    This class is an interface for the arguments.
    The method must be implemented in the subclasses.
    """
    
    def get_values_as_argument(self):
        """
        This method returns the values of the argument.
        """
        pass
    