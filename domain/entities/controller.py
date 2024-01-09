"""
This file implements the controller of the application.
"""
from domain.entities.spreadsheet import Spreadsheet
from domain.IO.user_interface import TextualUserInterface
from domain.IO.spreadsheetloader import SpreadsheetLoaderS2V
from domain.IO.spreadsheetsaver import SpreadsheetSaverS2V
from domain.entities.content import Formula
from domain.entities.formula_evaluator import FormulaEvaluatorPostfix


class Controller:
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
        # Todo: avoid changing a cell that is used in a formula for one with text
        cell_added = self._spreadsheet.add_cell(cell_identifier, new_content)
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
        cells_to_load = loader.load_spreadsheet(file_path)
        for cell in cells_to_load:
            try:
                self.edit_cell(cell[0], cell[1])
            except:  # Any exception treated as invalid file
                # raise ValueError("The file is not valid.")
                pass

    def save_spreadsheet_to_file(self, file_path: str) -> None:
        """
        This method saves the spreadsheet to a file.

        Keyword arguments:
        file_path -- the path of the file (str)
        """
        saver = SpreadsheetSaverS2V()
        saver.save_spreadsheet(self._spreadsheet, file_path)
