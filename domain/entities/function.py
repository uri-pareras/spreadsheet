"""
This file contains the function class.
"""
from domain.entities.argument import Argument
from domain.entities.operand import Operand
from domain.entities.value import NumericalValue
import abc


class Function(Argument, Operand, abc.ABC):
    """
    This is an abstract class that represents a function.
    """
    @abc.abstractmethod
    def __init__(self, arguments: list):
        """
        This method initializes the function.

        Keyword arguments:
        arguments -- the arguments of the function (list)
        """
        self._arguments = arguments

    @property
    def arguments(self):
        """
        Getter for arguments.
        """
        return self._arguments

    def obtain_values_from_arguments(self):
        """
        This method obtains the values from the arguments.

        Keyword arguments:
        arguments -- the arguments of the function (list)
        return -- the values of the arguments (list)
        """
        values = []
        for argument in self._arguments:
            values = values + argument.get_values_as_argument()  # List concatenation
        return values
    
    @abc.abstractmethod
    def compute(self):
        """
        This method computes the function.
        """
        pass

    def get_value_as_operand(self):  # TODO: As operand??
        """
        This method returns the value of the function.

        Keyword arguments:
        return -- the value of the function (Value)??
        """
        output = self.compute()
        if output is None:
            return None
        return output

    def get_values_as_argument(self):
        """
        This method returns the values of the function.

        Keyword arguments:
        return -- the values of the function (list)
        """
        output = self.compute()
        if output is None:
            return []
        return [self.compute()]


class Max(Function):  # TODO: REVISAR Argument and get_values_as_argument??
    """
    This class is a concrete implementation of the Function class.
    It also inherits from the Argument interface to obtain the 
    get_values_as_argument method.
    It represents the Max function.
    """
    def __init__(self, arguments: list):
        """
        This method initializes the function.

        Keyword arguments:
        arguments -- the arguments of the function (list)
        """
        super().__init__(arguments)
    
    def compute(self):
        """
        This method computes the function Max.

        Keyword arguments:
        return -- the maximum value of the arguments (float)
        """

        values = self.obtain_values_from_arguments()
        if len(values) == 0:
            return None
        max_value = values[0]
        for argument in values:
            if argument > max_value:
                max_value = argument
        return max_value


class Min(Function):
    """
    This class is a concrete implementation of the Function class.
    It also inherits from the Argument interface to obtain the 
    get_values_as_argument method.
    It represents the Min function.
    """
    def __init__(self, arguments: list):
        """
        This method initializes the function.

        Keyword arguments:
        arguments -- the arguments of the function (list)
        """
        super().__init__(arguments)
    
    def compute(self):
        """
        This method computes the function Min.

        Keyword arguments:
        return -- the minimum value of the arguments (float)
        """
        values = self.obtain_values_from_arguments()
        if len(values) == 0:
            return None
        min_value = values[0]
        for argument in values:
            if argument < min_value:
                min_value = argument
        return min_value


class Suma(Function):
    """
    This class is a concrete implementation of the Function class.
    It also inherits from the Argument interface to obtain the 
    get_values_as_argument method.
    It represents the Suma function.
    """
    def __init__(self, arguments: list):
        """
        This method initializes the function.

        Keyword arguments:
        arguments -- the arguments of the function (list)
        """
        super().__init__(arguments)

    def compute(self):
        """
        This method computes the function Suma.

        Keyword arguments:
        return -- the sum of the arguments (float)
        """
        suma = 0
        values = self.obtain_values_from_arguments()
        if len(values) == 0:
            return None
        for argument in values:
            suma = suma + argument
        return suma


class Promedio(Function):
    """
    This class is a concrete implementation of the Function class.
    It also inherits from the Argument interface to obtain the 
    get_values_as_argument method.
    It represents the Promedio function.
    """
    def __init__(self, arguments: list):
        """
        This method initializes the function.
        """
        super().__init__(arguments)

    def compute(self):
        """
        This method computes the function Promedio.
        
        Keyword arguments:
        return -- the average of the arguments (float)
        """
        suma = 0
        values = self.obtain_values_from_arguments()
        if len(values) == 0:
            return None
        for argument in values:
            suma = suma + argument
        return suma/len(values)


if __name__ == "__main__":
    f = Promedio([1, 2, 3])
    isinstance(f, Argument)