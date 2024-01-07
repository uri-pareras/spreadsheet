"""
This file contains the spreadsheet loader abstract class.
It also contains the SpreadsheetLoaderS2V concrete class.
This class loads a spreadsheet from a file.
"""
import abc
from domain.entities.spreadsheet import Spreadsheet
from domain.utils.utils import base26_to_int, int_to_base26


class SpreadsheetLoader(abc.ABC):
    """
    This class represents a spreadsheet loader.
    """

    @abc.abstractmethod
    def load_spreadsheet(self, file_path: str) -> Spreadsheet:
        """
        This method loads the spreadsheet from a file.

        Keyword arguments:
        file_path -- the path of the file (str)
        return -- the spreadsheet (Spreadsheet)
        """
        pass


class SpreadsheetLoaderS2V(SpreadsheetLoader):
    """
    This class represents a spreadsheet loader.
    """
    def load_spreadsheet(self, file_path: str) -> Spreadsheet:
        """
        This method loads the spreadsheet from a S2V file.

        Keyword arguments:
        file_path -- the path of the file (str)
        return -- the spreadsheet (Spreadsheet)
        """
        spreadsheet = Spreadsheet()
        with open(file_path) as spreadsheet_file:
            row_number = 1
            for line in spreadsheet_file:
                line = line.strip()
                if line != "":
                    row_cells = line.split(";")
                    for column in range(len(row_cells)):
                        spreadsheet.add_cell(int_to_base26(column) + str(row_number), row_cells[column])
                row_number += 1
        return spreadsheet
