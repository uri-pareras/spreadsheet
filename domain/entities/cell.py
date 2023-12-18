"""
This file contains the Cell class.
"""

from content import Content, TextualContent, NumericalContent
import re

class CellIdentifier():
    """
    This class represents a cell identifier.
    """
    def __init__(self, coordinate: str):
        """
        This method initializes the cell identifier.
        """
        #Check if the coordinate is valid
        if not isinstance(coordinate, str):
            raise ValueError("The coordinate must be a string.")
        if self.coordinate_is_valid(coordinate):
            self._coordinate = coordinate
            
            #Get the row and the column
            position = re.search(r"\d", s1)
            self._column = coordinate[:position.start()]
            self._row = coordinate[position.start():]

    def coordinate_is_valid(coordinate: str):
        """
        This method checks if the coordinate is valid.
        Returns True if it is valid and False otherwise.
        """
        for i, c in enumerate(coordinate):
            if c.isdigit():
                first_number_index = i
                break
        if first_number_index == 0:
            raise ValueError("The column must be a string of letters.")
        if first_number_index == len(coordinate) - 1:
            raise ValueError("The row must be a string of numbers.")
        column = coordinate[:first_number_index]
        row = coordinate[first_number_index:]
        if not column.isalpha():
            raise ValueError("The column must be a string of letters.")
        if not row.isdigit():
            raise ValueError("The row must be a string of numbers.")
        return True
    
    @property
    def coordinate(self):
        """
        This method returns the row.
        """
        return self._coordinate
    
    @coordinate.setter
    def coordinate(self, coordinate):
        """
        This method sets the row.
        """
        if not isinstance(coordinate, str):
            raise ValueError("The coordinate must be a string.")
        if self.coordinate_is_valid(coordinate):
            self._coordinate = coordinate

    @property
    def column(self):
        """
        This method returns the column.
        """
        return self._column
    
    @property
    def row(self):
        """
        This method returns the row.
        """
        return self._row

class Cell():
    """
    This class represents a cell.
    """
    def __init__(self, identifier: CellIdentifier, content: Content):
        """
        This method initializes the cell.
        """
        self._identifier = identifier
        self._content = content
        self._depends_on_me = []
    
    @property
    def identifier(self):
        """
        This method returns the identifier.
        """
        return self._identifier
    
    @identifier.setter
    def identifier(self, identifier):
        """
        This method sets the identifier.
        """
        if not isinstance(identifier, CellIdentifier):
            raise ValueError("The identifier must be a CellIdentifier.")
        self._identifier = identifier
    
    @property
    def content(self):
        """
        This method returns the content.
        """
        return self._content
    
    @content.setter
    def content(self, content):
        """
        This method sets the content.
        """
        if not isinstance(content, Content):
            raise ValueError("The content must be a Content.")
        self._content = content

    @property
    def dependencies(self):
        """
        This method returns the dependencies.
        """
        return self._dependencies
    @dependencies.setter
    def dependencies(self, dependencies):
        """
        This method sets the dependencies.
        """
        if not isinstance(dependencies, list):
            raise ValueError("The dependencies must be a list.")
        self._dependencies = dependencies

    def add_dependency(self, dependency: CellIdentifier):
        """
        This method adds a dependency.
        """
        if not isinstance(dependency, CellIdentifier): #TODO: CellIdentifier or Cell?
            raise ValueError("The dependency must be a CellIdentifier.")
        self._dependencies.append(dependency)
    
    def remove_dependency(self, dependency: CellIdentifier):
        """
        This method removes a dependency.
        """
        if not isinstance(dependency, CellIdentifier):
            raise ValueError("The dependency must be a CellIdentifier.")
        self._dependencies.remove(dependency)