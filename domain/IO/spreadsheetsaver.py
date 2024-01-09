"""
This file contains the spreadsheet saver abstract class.
It also contains the SpreadsheetSaverS2V concrete class.
This class saves a spreadsheet to a file.
"""
import abc
from domain.utils.utils import base26_to_int
from domain.entities.content import Formula, NumericalContent, TextualContent
from domain.entities.spreadsheet import Spreadsheet
from domain.IO.spreadsheetloader import SpreadsheetLoaderS2V  # Only for testing


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

        with open(file_path, 'w') as spreadsheet_file:
            cell_list = spreadsheet.get_cells()
            cell_list = self.sort_cells(cell_list)
            for cell in cell_list:
                while int(cell.identifier.row) != row_counter:
                    row_counter += 1
                    column_counter = 0
                    spreadsheet_file.write("\n")
                while base26_to_int(cell.identifier.column) != column_counter:
                    column_counter += 1
                    spreadsheet_file.write(";")
                else:
                    if isinstance(cell.content, Formula):  # If the content is a formula
                        spreadsheet_file.write("=" + cell.content.textual_representation.replace(";", ","))
                    # If the content is numerical or textual
                    elif isinstance(cell.content, NumericalContent) or isinstance(cell.content, TextualContent):
                        spreadsheet_file.write(cell.content.value.get_value_string())
                    else:
                        raise ValueError("Unexpected content type.")
            spreadsheet_file.close()

    @staticmethod
    def sort_cells(cell_list: list) -> list:
        """
        This method sorts the cells of a spreadsheet by row and column.
        Row and column can be more than one character.

        Keyword arguments:
        cell_list -- the list of cells (list)
        """
        if not isinstance(cell_list, list):
            raise ValueError("The cell list must be a list.")
        return sorted(cell_list, key=lambda cell: (int(cell.identifier.row), base26_to_int(cell.identifier.column)))


if __name__ == "__main__":
    saver = SpreadsheetSaverS2V()
    loader = SpreadsheetLoaderS2V()
    # WARNING: the path of the file IS HARDCODED
    #spreadsheet_test = loader.load_spreadsheet(r"C:\Users\Marc Micolau\PycharmProjects\spreadsheet\tests\spreadsheet_test.s2v")
    #saver.save_spreadsheet(spreadsheet_test, r"C:\Users\Marc Micolau\PycharmProjects\spreadsheet\tests\test_s2v_saved.s2v")
