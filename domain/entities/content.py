"""
This file contains the Content abstarct class and its implementations.
"""

import abc
from value import Value, TextualValue, NumericalValue

class Content(abc.ABC):
    """
    This class represents a content.
    """
    @abc.abstractmethod
    def __init__(self, value: Value):
        """
        This method initializes the content.
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
        if not isinstance(value, Value):
            raise ValueError("The value must be a Value.")
        self._value = value

class TextualContent(Content):
    """
    This class represents a textual content.
    """
    def __init__(self, value: TextualValue):
        """
        This method initializes the textual content.
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
        if not isinstance(value, TextualValue):
            raise ValueError("The value must be a TextualValue.")
        self._value = value

class NumericalContent(Content):
    """
    This class represents a numerical content.
    """
    def __init__(self, value: NumericalValue):
        """
        This method initializes the numerical content.
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
        if not isinstance(value, NumericalValue):
            raise ValueError("The value must be a NumericalValue.")
        self._value = value

class Formula(Content):
    """
    This class represents a formula.
    """
    def __init__(self, value: NumericalValue):
        """
        This method initializes the formula.
        """
        super().__init__(value)
        self._textual_representation = None
        self._expression = []
    
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
        if not isinstance(value, NumericalValue):
            raise ValueError("The value must be a NumericalValue.")
        self._value = value

    @property
    def textual_representation(self):
        """
        This method returns the textual representation.
        """
        return self._textual_representation
    
    @textual_representation.setter
    def textual_representation(self, textual_representation):
        """
        This method sets the textual representation.
        """
        if not isinstance(textual_representation, str):
            raise ValueError("The textual representation must be a string.")
        self._textual_representation = textual_representation

    @property
    def expression(self):
        """
        This method returns the expression.
        """
        return self._expression
    
    @expression.setter
    def expression(self, expression):
        """
        This method sets the expression.
        """
        if not isinstance(expression, list): #TODO: a list of formula components
            raise ValueError("The expression must be a list.")
        self._expression = expression