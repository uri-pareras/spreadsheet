"""
This file contains the spreadsheet class.
"""

from domain.entities.cell import Cell, CellIdentifier


class Spreadsheet:
    """
    This class represents a spreadsheet.
    """

    def __init__(self) -> None:
        """
        This method initializes the spreadsheet.

        Attributes:
        _cells -- the cells of the spreadsheet (dict)
        """
        self._cells = {}

    @property
    def cells(self):  # TODO: is necessary?
        """
        Getter for the cells.
        """
        return self._cells

    def add_cell(self, cell: Cell) -> None:
        """
        This method adds a cell to the _cells attribute

        Keyword arguments:
        cell -- the cell to be added (Cell)
        """
        if not isinstance(cell, Cell):
            raise ValueError("The cell must be a Cell.")
        self._cells[cell.identifier] = cell

    def get_cell(self, identifier: CellIdentifier) -> Cell:
        """
        This method returns a cell.

        Keyword arguments:
        identifier -- the identifier of the cell (CellIdentifier)
        return -- the cell (Cell) or None if the cell does not exist
        """
        if not isinstance(identifier, CellIdentifier):
            raise ValueError("The identifier must be a CellIdentifier.")
        if identifier not in self._cells:
            return None
        return self._cells[identifier]
