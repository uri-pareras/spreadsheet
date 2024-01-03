"""
This file contains the Range class.
"""

from argument import Argument
from cell import CellIdentifier, Cell
from spreadsheet import Spreadsheet

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
        columns = self.__generate_column_range(self._start, self._end)
        for column in columns:
            for row in range(self._start.row, self._end.row + 1):
                cells.append(spreadsheet.get_cell(CellIdentifier(column, row)))
        return cells #TODO: revisar
    

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
            result = 0
            for c in s:
                result = result * 26 + ord(c) - ord('A') + 1
            return result - 1  # Subtract 1 for 0-indexing

        # Function to convert an integer to a string in base-26
        def int_to_base26(num):
            result = ''
            while num >= 0:
                result = chr(num % 26 + ord('A')) + result
                num //= 26
                num -= 1  # Subtract 1 for 0-indexing
            return result

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
            values.append(cell.value)
        return values