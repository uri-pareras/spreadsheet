"""
This file contains the function class.
"""

from content import Content, TextualContent, NumericalContent
from argument import Argument
from value import Value, TextualValue, NumericalValue
from cell import CellIdentifier
import abc

class Function(abc.ABC):
    @abc.abstractmethod
    def __init__(self, arguments: list):
        """
        This method initializes the function.
        """
        self._arguments = arguments
        self._argument_values = self.obtain_values_from_arguments(arguments)

    @abc.abstractmethod
    def obtain_values_from_arguments(arguments):
        """
        This method obtains the values from the arguments.
        """
        values = []
        for argument in arguments:
            values = values + argument.get_values_as_argument()  #List concatenation
        return values
    
    @abc.abstractmethod
    def compute(self):
        """
        This method computes the function.
        """
        pass

class Max(Function, Argument):
    def __init__(self, arguments: list):
        """
        This method initializes the function.
        """
        super().__init__(arguments)
    
    def compute(self):
        """
        This method computes the function Max.
        This returns the maximum value of the arguments.
        """
        max = 0
        for argument in self._argument_values:
            if argument > max:
                max = argument
        return max
    
class Min(Function, Argument):
    def __init__(self, arguments: list):
        """
        This method initializes the function.
        """
        super().__init__(arguments)
    
    def compute(self):
        """
        This method computes the function Min.
        This returns the minimum value of the arguments.
        """
        min = 0
        for argument in self._argument_values:
            if argument < min:
                min = argument
        return min
    
class Suma(Function, Argument):
    def __init__(self, arguments: list):
        """
        This method initializes the function.
        """
        super().__init__(arguments)

    def compute(self):
        """
        This method computes the function Suma.
        This returns the sum of the arguments.
        """
        suma = 0
        for argument in self._argument_values:
            suma = suma + argument
        return suma
    
class Promedio(Function, Argument):
    def __init__(self, arguments: list):
        """
        This method initializes the function.
        """
        super().__init__(arguments)

    def compute(self):
        """
        This method computes the function Promedio.
        This returns the average of the arguments.
        """
        suma = 0
        for argument in self._argument_values:
            suma = suma + argument
        return suma/len(self._argument_values)