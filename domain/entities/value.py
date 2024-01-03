"""
This file contains the value abstract class and its implementations.
"""

import abc
from argument import Argument
from operand import Operand

class Value(abc.ABC):
    """
    This class represents a value.
    """
    @abc.abstractmethod
    def __init__(self, value):
        """
        This method initializes the value.
        """
        self._value = value

    @abc.abstractmethod
    @property
    def value(self):
        """
        This method returns the value.
        """
        return self._value
    
    @abc.abstractmethod
    @value.setter
    def value(self, value):
        """
        This method sets the value.
        """
        self._value = value

class TextualValue(Value):
    """
    This class represents a textual value.
    """
    def __init__(self, value):
        """
        This method initializes the textual value.
        """
        super().__init__(value)
    
    @property
    def value(self):
        """
        This method returns the textual value.
        """
        return self._value
    
    @value.setter
    def value(self, value):
        """
        This method sets the textual value.
        """
        if not isinstance(value, str):
            raise ValueError("The value must be a string.")
        self._value = value
    
class NumericalValue(Value, Argument, Operand):
    """
    This class represents a numerical value.
    """
    def __init__(self, value):
        """
        This method initializes the numerical value.
        """
        super().__init__(value)
    
    @property
    def value(self):
        """
        This method returns the numerical value.
        """
        return self._value
    
    @value.setter
    def value(self, value):
        """
        This method sets the numerical value.
        """
        if not isinstance(value, (int, float)):
            raise ValueError("The value must be a number.")
        self._value = value

    def get_values_as_argument(self):
        """
        This method returns a list of the value as an argument.
        """
        return [self._value]
    
    def get_value_as_operand(self):
        """
        This method returns the value as an operand.
        """
        return self._value