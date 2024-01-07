"""
This file contains the function class.
"""
from argument import Argument
import abc


class Function(abc.ABC):
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
        return self.compute()

    def get_values_as_argument(self):
        """
        This method returns the values of the function.

        Keyword arguments:
        return -- the values of the function (list)
        """
        return [self.compute()]


class Max(Function, Argument):  # TODO: REVISAR Argument and get_values_as_argument??
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
        max_value = values[0]
        for argument in values:
            if argument > max_value:
                max_value = argument
        return max_value


class Min(Function, Argument):
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
        min_value = values[0]
        for argument in values:
            if argument < min_value:
                min_value = argument
        return min_value


class Suma(Function, Argument):
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
        for argument in values:
            suma = suma + argument
        return suma


class Promedio(Function, Argument):
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
        for argument in values:
            suma = suma + argument
        return suma/len(values)


if __name__ == "__main__":
    f = Promedio([1, 2, 3])
    isinstance(f, Argument)