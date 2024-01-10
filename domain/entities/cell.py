"""
This file contains the Cell class.
"""

from domain.entities.content import Content, NumericalContent, Formula
from domain.entities.argument import Argument
from domain.entities.operand import Operand
import re
from test.entities.bad_coordinate_exception import BadCoordinateException


class CellIdentifier:
    """
    This class represents a cell identifier.
    """
    def __init__(self, coordinate: str):
        """
        This method initializes the cell identifier.

        Keyword arguments:
        coordinate -- the coordinate of the cell (str ex: A1)

        Attributes:
        _coordinate -- the coordinate of the cell (str)
        _column -- the column of the cell (str)
        _row -- the row of the cell (str)
        """
        # Check if the coordinate is valid
        if not isinstance(coordinate, str):
            raise BadCoordinateException("The coordinate must be a string.")
        if self.coordinate_is_valid(coordinate):
            self._coordinate = coordinate
            
            # Get the row and the column
            position = re.search(r"\d", coordinate)
            self._column = coordinate[:position.start()]
            self._row = coordinate[position.start():]

    @staticmethod
    def coordinate_is_valid(coordinate: str):
        """
        This method checks if the coordinate is valid.
        Returns True if it is valid and False otherwise.

        Keyword arguments:
        coordinate -- the coordinate of the cell (str)
        return -- True if the coordinate is valid and False otherwise (bool)
        """
        if not isinstance(coordinate, str):
            raise BadCoordinateException("The coordinate must be a string.")
        elif coordinate == "":
            raise BadCoordinateException("The coordinate cannot be empty.")
        
        first_number_index = len(coordinate)
        for i, c in enumerate(coordinate):
            if c.isdigit():
                first_number_index = i
                break
        if first_number_index == 0: # If the first character is a number
            raise BadCoordinateException("The column must be a string of letters.")
        if first_number_index == len(coordinate):  # If there is no number
            raise BadCoordinateException("The row must be a string of numbers.")
        
        column = coordinate[:first_number_index]
        row = coordinate[first_number_index:]
        if not column.isalpha():
            raise BadCoordinateException("The column must be a string of letters.")
        if not row.isdigit():
            raise BadCoordinateException("The row must be a string of numbers.")
        return True
    
    @property
    def coordinate(self):
        """
        Getter for the coordinate.
        """
        return self._coordinate
    
    @coordinate.setter
    def coordinate(self, coordinate):
        """
        Setter for the coordinate.
        """
        if not isinstance(coordinate, str):
            raise BadCoordinateException("The coordinate must be a string.")
        if self.coordinate_is_valid(coordinate):
            self._coordinate = coordinate

    @property
    def column(self):
        """
        Getter for the column.
        """
        return self._column
    
    @property
    def row(self):
        """
        Getter for the row.
        """
        return self._row

    def __eq__(self, other):
        """
        This method checks if two cell identifiers are equal.
        """
        if isinstance(other, CellIdentifier):
            return self.coordinate == other.coordinate
        else:
            return False

    def __hash__(self):
        """
        This method returns the hash of the cell identifier.
        """
        return hash(self.coordinate)


class Cell(Argument, Operand):
    """
    This class represents a cell.
    """
    def __init__(self, identifier: CellIdentifier, content: Content):
        """
        This method initializes the cell.
        
        Keyword arguments:
        identifier -- the identifier of the cell (CellIdentifier)
        content -- the content of the cell (Content)

        Attributes:
        _identifier -- the identifier of the cell (CellIdentifier)
        _content -- the content of the cell (Content)
        _dependencies -- the cells that the cell depends on (list)
        """
        self._identifier = identifier
        self._content = content
        self._depends_on_me = []
        self._depends_on = []
    
    @property
    def identifier(self):
        """
        Getter for the identifier.
        """
        return self._identifier
    
    @identifier.setter
    def identifier(self, identifier):
        """
        Setter for identifier.
        """
        if not isinstance(identifier, CellIdentifier):
            raise ValueError("The identifier must be a CellIdentifier.")
        self._identifier = identifier
    
    @property
    def content(self):
        """
        Getter for content.
        """
        return self._content
    
    @content.setter
    def content(self, content):
        """
        Setter for content.
        """
        if not isinstance(content, Content):
            raise ValueError("The content must be a Content.")
        self._content = content

    @property
    def depends_on_me(self):
        """
        Getter for dependencies.
        """
        return self._depends_on_me
    
    @depends_on_me.setter
    def depends_on_me(self, dependencies):
        """
        Setter for dependencies.
        """
        if not isinstance(dependencies, list):
            raise ValueError("The dependencies must be a list.")
        self._depends_on_me = dependencies

    @property
    def depends_on(self):
        """
        Getter for dependencies.
        """
        return self._depends_on

    @depends_on.setter
    def depends_on(self, dependencies):
        """
        Setter for dependencies.
        """
        if not isinstance(dependencies, list):
            raise ValueError("The dependencies must be a list.")
        self._depends_on = dependencies

    def add_dependency(self, dependency: CellIdentifier):
        """
        This method adds a dependency to the attribute _depends_on_me.

        keyword arguments:
        dependency -- the dependency to add (CellIdentifier)
        """
        if not isinstance(dependency, CellIdentifier):
            raise ValueError("The dependency must be a Cell.")
        self._depends_on_me.append(dependency)
    
    def remove_dependency(self, dependency: CellIdentifier):
        """
        This method removes a dependency from the attribute _dependencies.

        Keyword arguments:
        dependency -- the dependency to remove (CellIdentifier)
        """
        if not isinstance(dependency, CellIdentifier):
            raise ValueError("The dependency must be a CellIdentifier.")
        self._depends_on_me.remove(dependency)

    def get_values_as_argument(self):
        """
        This method returns the values of the cell as an argument.

        Keyword arguments:
        return -- the values of the cell (list)
        """
        if isinstance(self._content, NumericalContent):
            if self._content.value.value is None:
                return []
            return [self._content.value.value]
        else:  # This is redundant, but it is here to make it clear
            raise ValueError("The content must be a NumericalContent.")
    
    def get_value_as_operand(self):
        """
        This method returns the value of the cell as an operand.

        Keyword arguments:
        return -- the value of the cell (float)
        """
        if isinstance(self._content, NumericalContent) or isinstance(self._content, Formula):
            return self._content.value.value
        else:
            raise ValueError("The content must be a NumericalContent.")
