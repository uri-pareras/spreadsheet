"""
This file implements the controller of the application.
"""
from domain.entities.spreadsheet import Spreadsheet
from domain.IO.user_interface import TextualUserInterface
from domain.IO.spreadsheetloader import SpreadsheetLoaderS2V
from domain.IO.spreadsheetsaver import SpreadsheetSaverS2V
from domain.entities.content import Formula, TextualContent
from domain.entities.formula_evaluator import FormulaEvaluatorPostfix
from domain.entities.cell import CellIdentifier, Cell
from domain.exceptions.exceptions import NoNumberException, ReadingSpreadSheetException, SavingSpreadSheetException, BadCoordinateException
from usecasesmarker.spreadsheet_controller_for_checker import ISpreadsheetControllerForChecker


class Controller(ISpreadsheetControllerForChecker):
    def __init__(self):
        """
        This method initializes the controller of the spreadsheet application.
        """
        self._spreadsheet = Spreadsheet()
        self._user_interface = TextualUserInterface()
        self._formula_evaluator = FormulaEvaluatorPostfix(self._spreadsheet)
        self.exit = False

    def run(self) -> None:
        """
        This method runs the controller.
        """
        while not self.exit:
            command_list = self._user_interface.get_command()  # Wait for the user to enter a command
            self.process_command(command_list)  # Process the command

    def process_command(self, command: list) -> None:
        """
        This method processes a command and calls the corresponding method.
        """

        match command[0]:
            case "RF":
                pass  # If the command is RF, wait for the next command
            case "C":
                self.create_new_spreadsheet()
                self.render_spreadsheet()
                self._user_interface.command_run_successfully("C")
            case "E":
                self.edit_cell(command[1], command[2])
                self.render_spreadsheet()
                self._user_interface.command_run_successfully("E")
            case "L":
                self.load_spreadsheet_from_file(command[1])
                self.render_spreadsheet()
                self._user_interface.command_run_successfully("L")
            case "S":
                self.save_spreadsheet_to_file(command[1])
                self.render_spreadsheet()
                self._user_interface.command_run_successfully("S")
            case "Q":
                self.quit()
            case _:
                raise ValueError("The command is not valid.")

    def render_spreadsheet(self) -> None:
        """
        This method renders the spreadsheet.
        """
        self._user_interface.render_spreadsheet(self._spreadsheet)

    def quit(self) -> None:
        """
        This method quits the application.
        """
        self.exit = True
        print("Goodbye!")
        print("Created by: Marc Micolau & Oriol Pareras.")

    def create_new_spreadsheet(self) -> None:
        """
        This method creates a new spreadsheet.
        """
        self._spreadsheet = Spreadsheet()
        self._formula_evaluator = FormulaEvaluatorPostfix(self._spreadsheet)

    def edit_cell(self, cell_identifier: str, new_content: str) -> None:
        """
        This method edits a cell.

        Keyword arguments:
        cell_identifier -- the identifier of the cell (str)
        new_content -- the new content of the cell (str)
        """
        cell_added = self._spreadsheet.add_cell(cell_identifier, str(new_content))  # Castejat a str crec que hi ha un fallo al marker
        self._formula_evaluator = FormulaEvaluatorPostfix(self._spreadsheet)  # TODO: Modificar formula evaluator perque no es crei un altre cada cop que s'edita una cel·la
        if isinstance(cell_added.content, Formula):
            self._formula_evaluator.generate_expression(cell_added)
            self._formula_evaluator.evaluate_expression(cell_added)

    def load_spreadsheet_from_file(self, file_path: str) -> None:
        """
        This method loads a spreadsheet from a file.

        Keyword arguments:
        file_path -- the path of the file (str)
        """
        self._spreadsheet = Spreadsheet()  # create new spreadsheet
        loader = SpreadsheetLoaderS2V()  # create loader
        try:
            cells_to_load = loader.load_spreadsheet(file_path)
            for cell in cells_to_load:
                self.edit_cell(cell[0], cell[1])
        except ValueError:  # Any exception treated as invalid file
            raise ReadingSpreadSheetException("The file is not valid.")
        except FileNotFoundError:
            raise ReadingSpreadSheetException("The file does not exist.")

    def save_spreadsheet_to_file(self, file_path: str) -> None:
        """
        This method saves the spreadsheet to a file.

        Keyword arguments:
        file_path -- the path of the file (str)
        """
        saver = SpreadsheetSaverS2V()
        try:
            saver.save_spreadsheet(self._spreadsheet, file_path)
        except ValueError:
            raise SavingSpreadSheetException("The file is not valid.")
        except:
            raise SavingSpreadSheetException("The file could not be saved.")

    def get_cell_content_as_float(self, coord: str) -> float:
        """
        This method returns the content of a cell as a float.

        Keyword arguments:
        coord -- the coordinate of the cell (str)
        """
        cell = self._spreadsheet.get_cell(CellIdentifier(coord))
        try:
            float(cell.content.value.value)
        except ValueError:
            raise NoNumberException("The cell does not contain a number.")

    def get_cell_content_as_string(self, coord: str) -> str:
        """
        Parameters
        coord	a string representing a coordinate in spreadsheet ('A10', for instance).

        Returns
        a string version of the content of a cell. If the cell contains a textual
        content it directly shall return its string value. If the cell contains a
        numerical content, it returns the textual representation of the number.
        If the cell content is a formula, it returns the string representing the
        number resulting of evaluating such formula.
        """
        cell = self._spreadsheet.get_cell(CellIdentifier(coord))  # This must raise the BadCoordinateException
        return str(cell.content.value.value)

    def get_cell_formula_expression(self, coord: str) -> str:
        """
        Parameters
        coord	a string representing a coordinate in spreadsheet ('A10', for instance).

        Returns
        a string representing the formula expression of a cell. If the cell does not
        contain a formula, it returns None.
        """
        cell: Cell = self._spreadsheet.get_cell(CellIdentifier(coord))  # This must raise the BadCoordinateException
        if isinstance(cell.content, Formula):
            return cell.content.textual_representation
        else:
            raise BadCoordinateException("The cell does not contain a formula.")

    def set_cell_content(self, coord: str, str_content: str):
        self.edit_cell(coord, str_content)
