"""
This file contains the DependencyManager class.
"""

from domain.entities.spreadsheet import Spreadsheet
from domain.entities.cell import Cell

class DependencyManager:
    """
    This class is responsible for managing the dependencies and detecting circular dependencies.
    """

    def __init__(self, spreadsheet: Spreadsheet):
        """
        This method initializes the dependency manager.

        Keyword arguments:
        spreadsheet -- the spreadsheet (Spreadsheet)

        Attributes:
        _spreadsheet -- the spreadsheet (Spreadsheet)
        """
        self._spreadsheet = spreadsheet

    def detect_circular_dependencies(self, cell: Cell) -> bool:
        """
        This method detects circular dependencies.

        Keyword arguments:
        cell -- the cell containing the new Formula to check (Cell)
        return -- True if there are circular dependencies, False otherwise (bool)
        """
        dependencies = cell.dependencies
        for dependency in dependencies:
            if dependency.identifier.coordinate == cell.identifier.coordinate:
                return True
            else:
                return self.detect_circular_dependencies(dependency)

        return False