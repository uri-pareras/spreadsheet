"""
This file contains the Range class.
"""

from domain.entities.argument import Argument
from domain.entities.cell import CellIdentifier
from domain.entities.spreadsheet import Spreadsheet
from domain.entities.cell import Cell
from domain.entities.content import NumericalContent
from domain.entities.value import NumericalValue

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
        cell_ids = self.obtain_all_cell_ids()
        for cell_id in cell_ids:
            if spreadsheet.get_cell(cell_id) is not None:
                cells.append(spreadsheet.get_cell(cell_id))
            else:
                cells.append(Cell(cell_id, NumericalContent(NumericalValue(0))))
        return cells  # TODO: revisar

    def obtain_all_cell_ids(self) -> list:
        """
        This method returns the cell identifiers of the cells in the range.

        Keyword arguments:
        return -- the cell identifiers (list)
        """
        cell_ids = []
        columns = self.__generate_column_range(self._start.column, self._end.column)
        for column in columns:
            for row in range(int(self._start.row), int(self._end.row) + 1):
                cell_ids.append(CellIdentifier(str(column) + str(row)))
        return cell_ids

    @staticmethod
    def __generate_column_range(start_column, end_column):
        """
        This function returns a list of the columns in between the start and end columns.

        Keyword arguments:
        start_column -- the start column (str)
        end_column -- the end column (str)
        return -- the list of columns (list)
        """
        # Function to convert a string to an integer in base-26
        def base26_to_int(s):
            result_int = 0
            for c in s:
                result_int = result_int * 26 + ord(c) - ord('A') + 1
            return result_int - 1  # Subtract 1 for 0-indexing

        # Function to convert an integer to a string in base-26
        def int_to_base26(num):
            result_b26 = ''
            while num >= 0:
                result_b26 = chr(num % 26 + ord('A')) + result_b26
                num //= 26
                num -= 1  # Subtract 1 for 0-indexing
            return result_b26

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
            values.append(cell.content.value.value)
        return values
