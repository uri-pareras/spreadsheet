"""
This file contains the spreadsheet loader abstract class.
It also contains the SpreadsheetLoaderS2V concrete class.
This class loads a spreadsheet from a file.
"""
import abc
from domain.entities.spreadsheet import Spreadsheet
from domain.utils.utils import int_to_base26
from domain.entities.content import Formula


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

    def load_spreadsheet(self, file_path: str) -> list:
        """
        This method parses the file and returns the list of cells to be loaded to the spreadsheet.

        Keyword arguments:
        file_path -- the path of the file (str)
        return -- the spreadsheet_to_load (lis)
        """
        cells_to_load = []
        file_path = file_path.strip()
        if not isinstance(file_path, str):
            raise ValueError("The file path must be a string.")
        if not file_path.endswith(".s2v"):
            raise ValueError("The file must be a .s2v file.")
        spreadsheet_to_load = Spreadsheet()
        with open(file_path) as spreadsheet_file:
            row_number = 1
            for line in spreadsheet_file:
                line = line.strip()
                if line != "":
                    row_cells = line.split(";")
                    for column in range(len(row_cells)):
                        string_value = row_cells[column]
                        if row_cells[column] == "":
                            pass
                        elif row_cells[column][0] == "=" and "," in row_cells[column]:
                            # If there is a comma in a formula, replace it with a semicolon
                            row_cells[column] = row_cells[column].replace(",", ";")
                        elif "," in row_cells[column]:
                            raise ValueError("The file is not valid.")
                        cells_to_load.append((int_to_base26(column) + str(row_number), row_cells[column]))
                row_number += 1
        return cells_to_load


if __name__ == "__main__":
    loader = SpreadsheetLoaderS2V()
    # WARNING: the path of the file IS HARDCODED
    spreadsheet = loader.load_spreadsheet("/home/marc/PycharmProjects/spreadsheet/tests/spreadsheet_test.s2v")
    for cell_id in spreadsheet:
        cell = spreadsheet.get_cell(cell_id)
        if isinstance(cell.content, Formula):
            print(cell.identifier.coordinate, cell.content.textual_representation)
        else:
            print(cell.identifier.coordinate, cell.content.value.value)
