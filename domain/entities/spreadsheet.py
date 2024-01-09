"""
This file contains the spreadsheet class.
"""

from domain.entities.cell import Cell, CellIdentifier
from domain.entities.content import Content, NumericalContent, TextualContent, Formula
from domain.entities.value import NumericalValue, TextualValue


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

    def __iter__(self):
        """
        This method returns an iterator of the spreadsheet.
        """
        return iter(self._cells)

    @property
    def cells(self):  # TODO: is necessary?
        """
        Getter for the cells.
        """
        return self._cells

    def add_cell(self, cell_id: str, content_str: str) -> None:
        """
        This method adds a cell to the spreadsheet.
        If the cell is already in the spreadsheet, it is overwritten.

        Keyword arguments:
        cell_id -- the identifier of the cell (str)
        content -- the content of the cell (str)
        """
        content_str = content_str.strip()

        if cell_id in self._cells:  # If the cell is already in the spreadsheet, it is overwritten
            self._cells.pop(cell_id)

        if content_str.startswith("="):  # Check if it is a formula
            formula_str = content_str[1:]
            formula = Formula(formula_str)
            cell = Cell(CellIdentifier(cell_id), formula)
        else:
            try:  # Check if it is a number
                value_number = float(content_str)
            except ValueError:  # If it is not a formula or a number, it is text
                value = TextualValue(content_str)
                content = TextualContent(value)
                cell = Cell(CellIdentifier(cell_id), content)
            else:
                value = NumericalValue(value_number)
                content = NumericalContent(value)
                cell = Cell(CellIdentifier(cell_id), content)
        self.__store_cell(cell)

    def __store_cell(self, cell: Cell) -> None:
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

    def get_cells(self) -> list:
        """
        This method returns the cells of the spreadsheet.

        return -- the cells of the spreadsheet (list)
        """
        return list(self._cells.values())
