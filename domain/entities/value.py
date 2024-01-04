"""
This file contains the value abstract class and its implementations.
"""

import abc
from argument import Argument
from operand import Operand


class Value(abc.ABC):
    """
    This is an abstract class that represents a value.
    """

    @abc.abstractmethod
    def __init__(self, value):
        """
        This method initializes the value.

        Keyword arguments:
        value -- the value (any)
        """
        self._value = value

    @abc.abstractmethod
    @property
    def value(self):
        """
        Getter for value.
        """
        return self._value

    @abc.abstractmethod
    @value.setter
    def value(self, value):
        """
        Setter for value.
        """
        self._value = value


class TextualValue(Value):
    """
    This is a concrete implementation of the Value class.
    It represents a textual value.
    """

    def __init__(self, value):
        """
        This method initializes the textual value.

        Keyword arguments:
        value -- the value of the textual value (string)
        """
        super().__init__(value)
        self._type = "textual"

    @property
    def type(self):
        """
        Getter for type.
        """
        return self._type

    @property
    def value(self):
        """
        Getter for value.
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Setter for value.
        """
        if not isinstance(value, str):
            raise ValueError("The value must be a string.")
        self._value = value


class NumericalValue(Value, Argument, Operand):
    """
    This is a concrete implementation of the Value class.
    It represents a numerical value.
    """

    def __init__(self, value):
        """
        This method initializes the numerical value.

        Keyword arguments:
        value -- the value of the numerical value (number)
        """
        super().__init__(value)
        self._type = "numerical"

    @property
    def type(self):
        """
        Getter for type.
        """
        return self._type

    @property
    def value(self):
        """
        Getter for value
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        setter for value
        """
        if not isinstance(value, (int, float)):
            raise ValueError("The value must be a number.")
        self._value = value

    def get_values_as_argument(self):
        """
        This method returns a list of the value as an argument.

        Keyword arguments:
        return -- the value as an argument (list)
        """
        return [self._value]

    def get_value_as_operand(self):
        """
        This method returns the value as an operand.

        Keyword arguments:
        return -- the value as an operand (Value)
        """
        return self._value
