"""
This file contains the spreadsheet saver abstract class.
It also contains the SpreadsheetSaverS2V concrete class.
This class saves a spreadsheet to a file.
"""
import abc
from domain.entities.spreadsheet import Spreadsheet


class SpreadsheetSaver(abc.ABC):
    """
    This class represents a spreadsheet saver.
    """
    @abc.abstractmethod
    def save_spreadsheet(self, spreadsheet: Spreadsheet, file_path: str) -> None:
        """
        This method saves the spreadsheet to a file.

        Keyword arguments:
        spreadsheet -- the spreadsheet (Spreadsheet)
        file_path -- the path of the file (str)
        """
        pass


class SpreadsheetSaverS2V(SpreadsheetSaver):
    """
    This class represents a spreadsheet saver.
    """
    def save_spreadsheet(self, spreadsheet: Spreadsheet, file_path: str) -> None:
        """
        This method saves the spreadsheet to a S2V file.

        Keyword arguments:
        spreadsheet -- the spreadsheet (Spreadsheet)
        file_path -- the path of the file (str)
        """
        column_counter = 0
        row_counter = 1
        if not isinstance(spreadsheet, Spreadsheet):
            raise ValueError("The spreadsheet must be a Spreadsheet.")
        if not isinstance(file_path, str):
            raise ValueError("The file path must be a string.")
        if not file_path.endswith(".s2v"):
            raise ValueError("The file must be a .s2v file.")
        with open(file_path, "w") as spreadsheet_file:
            cell_list = spreadsheet.get_cells()
            for cell in cell_list:
                if cell.identifier.row != row_counter:
                    row_counter += 1
                    column_counter = 0
                    spreadsheet_file.write("\n")
                elif cell.identifier.column != column_counter:
                    column_counter += 1
                    spreadsheet_file.write(";")
                else:
                    spreadsheet_file.write(cell.content.value.get_value_string() + ";")
                    column_counter += 1
