"""
This file contains the Cell class.
"""

from content import Content, TextualContent, NumericalContent

class CellIdentifier():
    """
    This class represents a cell identifier.
    """
    def __init__(self, coordinate: tuple):
        """
        This method initializes the cell identifier.
        """
        self._coordinate = coordinate
    
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
        if not isinstance(coordinate[0], str):
            raise ValueError("The row must be a string.")
        if not isinstance(coordinate[1], int):
            raise ValueError("The row must be an integer.")
        self._coordinate = coordinate

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
        self._dependencies = []
    
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