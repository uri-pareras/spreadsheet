"""
This file implements the controller of the application.
"""
from domain.entities.cell import CellIdentifier
from domain.entities.cell import Cell
from domain.entities.spreadsheet import Spreadsheet
from domain.IO.user_interface import TextualUserInterface
from domain.IO.spreadsheetloader import SpreadsheetLoaderS2V
from domain.IO.spreadsheetsaver import SpreadsheetSaverS2V
from domain.entities.content import Formula, Content, TextualContent, NumericalContent
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
        content = Content.create_content(new_content)
        if content is None:
            raise ValueError("The content is not valid.")
        cell = self._spreadsheet.get_cell(CellIdentifier(cell_identifier))
        if cell is None:
            cell = Cell(CellIdentifier(cell_identifier), content)
            self._spreadsheet.add_cell(cell)
            if isinstance(content, Formula):
                self._formula_evaluator.generate_expression(cell)
                self._formula_evaluator.evaluate_expression(cell)
        else:
            if cell.depends_on_me:
                if isinstance(content, TextualContent):
                    raise ValueError("The content can not be text because it is used in a formula.")
                elif isinstance(content, NumericalContent):
                    cell.content = content
                elif isinstance(content, Formula):
                    cell.content = content
                    self._formula_evaluator.generate_expression(cell)
                    self._formula_evaluator.evaluate_expression(cell)
                for dependency in cell.depends_on_me:
                    dependency_cell = self._spreadsheet.get_cell(dependency)
                    self._formula_evaluator.evaluate_expression(dependency_cell)
            else:
                cell.content = content
                if isinstance(content, Formula):
                    self._formula_evaluator.generate_expression(cell)
                    self._formula_evaluator.evaluate_expression(cell)


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
