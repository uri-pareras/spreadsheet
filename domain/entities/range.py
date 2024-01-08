"""
This file contains the Range class.
"""

from domain.entities.argument import Argument
from domain.entities.cell import CellIdentifier
from domain.entities.spreadsheet import Spreadsheet
from domain.utils.utils import base26_to_int, int_to_base26


class Range(Argument):
    """
    This class represents a range.
    It inherits from the Argument interface to obtain the
    get_values_as_argument method.
    """
    def __init__(self, start: CellIdentifier, end: CellIdentifier, spreadsheet: Spreadsheet):
        """
        This method initializes the range.

        Keyword arguments:
        start -- the start of the range (CellIdentifier)
        end -- the end of the range (CellIdentifier)
        spreadsheet -- the spreadsheet (Spreadsheet)
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

        Keyword arguments:
        spreadsheet -- the spreadsheet (Spreadsheet)
        return -- the cells of the range (list)
        """
        cells = []
        columns = self.__generate_column_range(self._start.column, self._end.column)
        for column in columns:
            for row in range(self._start.row, self._end.row + 1):
                cells.append(spreadsheet.get_cell(CellIdentifier(str(column) + str(row))))
        return cells  # TODO: revisar

    @staticmethod
    def __generate_column_range(start_column, end_column):
        """
        This function returns a list of the columns in between the start and end columns.

        Keyword arguments:
        start_column -- the start column (str)
        end_column -- the end column (str)
        return -- the list of columns (list)
        """
        # Convert the start and end strings to integers
        start_num = base26_to_int(start_column)
        end_num = base26_to_int(end_column)

        # Generate strings between the start and end integers
        result = []
        for i in range(start_num, end_num + 1):
            result.append(int_to_base26(i))
        
        return result
    
    def get_values_as_argument(self):
        """
        This method returns the values of the cells.
        return -- the values of the cells (list)
        """
        values = []
        for cell in self._cells:
            values.append(cell.content.value)
        return values
