"""
This file contains the implementation of the user interface.
"""
import abc


class UserInterface(abc.ABC):
    """
    This class represents an abstract user interface.
    """
    @abc.abstractmethod
    def run(self) -> None:
        """
        This method runs the user interface.
        """
        pass

    def read_commands_from_file(self, file_path: str) -> None:
        """
        This method reads the commands from a file.

        Keyword arguments:
        file_path -- the path of the file (str)
        """
        pass

    def create_new_spreadsheet(self) -> None:
        """
        This method creates a new spreadsheet.
        """
        pass

    def edit_cell(self, cell_identifier: str, new_content: str) -> None:
        """
        This method edits a cell.

        Keyword arguments:
        cell_identifier -- the identifier of the cell (str)
        new_content -- the new content of the cell (str)
        """
        pass

    def load_spreadsheet_from_file(self, file_path: str) -> None:
        """
        This method loads a spreadsheet from a file.

        Keyword arguments:
        file_path -- the path of the file (str)
        """
        pass

    def save_spreadsheet_to_file(self, file_path: str) -> None:
        """
        This method saves the spreadsheet to a file.

        Keyword arguments:
        file_path -- the path of the file (str)
        """
        pass


class TextualUserInterface(UserInterface):
    """
    This class represents a concrete implementation of the user interface.
    It represents a textual user interface.
    """
    def run(self) -> None:
        """
        This method runs the user interface.
        """
        pass
