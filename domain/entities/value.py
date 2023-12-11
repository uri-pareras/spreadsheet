"""
This file contains the value abstract class and its implementations.
"""

import abc

class Value(abc):
    """
    This class represents a value.
    """
    @abc.abstractmethod
    def __init__(self, value):
        """
        This method initializes the value.
        """
        self._value = value

    @property
    def value(self):
        """
        This method returns the value.
        """
        return self._value
    
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
    
class NumericalValue(Value):
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