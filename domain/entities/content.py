"""
This file contains the Content abstarct class and its implementations.
"""

import abc
from value import Value, TextualValue, NumericalValue


class Content(abc.ABC):
    """
    This is an abstract class that represents a content.
    """

    @abc.abstractmethod
    def __init__(self, value: Value):
        """
        This method initializes the content.

        Keyword arguments:
        value -- the value of the content (Value)

        Attributes:
        _value -- the value of the content (Value)
        """
        self._value = value

    @property
    @abc.abstractmethod
    def value(self):
        """
        Getter for value.
        """
        return self._value

    @value.setter
    @abc.abstractmethod
    def value(self, value):
        """
        Setter for value.
        """
        if not isinstance(value, Value):
            raise ValueError("The value must be a Value.")
        self._value = value


class TextualContent(Content):
    """
    This is a concrete implementation of the Content class.
    It represents a textual content.
    """

    def __init__(self, value: TextualValue):
        """
        This method initializes the textual content.

        Keyword arguments:
        value -- the value of the textual content (TextualValue)

        Attributes:
        _value -- the value of the textual content (TextualValue)
        """
        super().__init__(value)

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
        if not isinstance(value, TextualValue):
            raise ValueError("The value must be a TextualValue.")
        self._value = value


class NumericalContent(Content):
    """
    This is a concrete implementation of the Content class.
    It represents a numerical content.
    """

    def __init__(self, value: NumericalValue):
        """
        This method initializes the numerical content.

        Keyword arguments:
        value -- the value of the numerical content (NumericalValue)

        Attributes:
        _value -- the value of the numerical content (NumericalValue)
        """
        super().__init__(value)

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
        if not isinstance(value, NumericalValue):
            raise ValueError("The value must be a NumericalValue.")
        self._value = value


class Formula(Content):
    """
    This is a concrete implementation of the Content class.
    It represents a formula.
    """

    def __init__(self, value: NumericalValue):
        """
        This method initializes the formula.

        Keyword arguments:
        value -- the value of the formula (NumericalValue)

        Attributes:
        textual_representation -- the textual representation of the formula (str)
        expression -- the expression of the formula (list)
        """
        super().__init__(value)
        self._textual_representation = None
        self._expression = []

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
        if not isinstance(value, NumericalValue):
            raise ValueError("The value must be a NumericalValue.")
        self._value = value

    @property
    def textual_representation(self):
        """
        Getter for textual representation.
        """
        return self._textual_representation

    @textual_representation.setter
    def textual_representation(self, textual_representation):
        """
        Setter for textual representation.
        """
        if not isinstance(textual_representation, str):
            raise ValueError("The textual representation must be a string.")
        self._textual_representation = textual_representation

    @property
    def expression(self):
        """
        Getter for expression.
        """
        return self._expression

    @expression.setter
    def expression(self, expression):
        """
        Setter for expression.
        """
        if not isinstance(expression, list):  # TODO: a list of formula components
            raise ValueError("The expression must be a list.")
        self._expression = expression
