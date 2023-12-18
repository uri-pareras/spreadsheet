"""
This file contains the Range class.
"""

from argument import Argument
from cell import CellIdentifier, Cell
from spreadsheet import Spreadsheet

class Range(Argument): #TODO Heredar d'argument
    def __init__(self, start: CellIdentifier, end: CellIdentifier, spreadsheet: Spreadsheet):
        """
        This method initializes the range.
        """
        if not isinstance(start, CellIdentifier):
            raise ValueError("The start must be a CellIdentifier.")
        if not isinstance(end, CellIdentifier):
            raise ValueError("The end must be a CellIdentifier.")
        self._start = start
        self._end = end
        self._cells = self.obtain_cells(spreadsheet)
        

    def obtain_cells(self, spreadsheet: Spreadsheet):
        """
        This method obtains the cells of the range from the spreadsheet.
        """
        cells = []
        for column in range(self._start.column, self._end.column + 1):
            for row in range(self._start.row, self._end.row + 1):
                cells.append(spreadsheet.get_cell(CellIdentifier(column, row)))
        return cells #TODO: revisar


    def __iter__(self):
        """
        This method returns the iterator.
        """
        return iter(self._cells)