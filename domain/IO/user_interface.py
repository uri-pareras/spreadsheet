"""
This file contains the implementation of the user interface.
"""
import abc
from domain.entities.spreadsheet import Spreadsheet
from domain.entities.content import Formula
from collections import deque


class UserInterface(abc.ABC):
    """
    This class represents an abstract user interface.
    """
    @abc.abstractmethod
    def get_command(self) -> list:
        """
        This method prints the available commands and gets the command from the user.
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def render_spreadsheet(spreadsheet: Spreadsheet) -> None:
        """
        This method prints the spreadsheet.
        """
        pass

    @abc.abstractmethod
    def render_available_commands(self) -> None:
        """
        This method prints the available commands.
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def command_run_successfully(command: str) -> None:
        """
        This method prints a message if the command was run successfully.
        """
        pass


class TextualUserInterface(UserInterface):
    """
    This class represents a concrete implementation of the user interface.
    It represents a textual user interface.
    """
    def __init__(self):
        """
        This method initializes the user interface.
        """
        self._available_commands = ["RF", "C", "E", "L", "S", "Q"]
        self._command_list = []
        self._command_buffer = deque([])

    def get_command(self) -> list:
        """
        This method prints the available commands and gets the command from the user.
        """
        if self._command_buffer:
            command = self._command_buffer.popleft()  # Get the first command in the queue
        else:
            self.render_available_commands()
            command = input("Enter a command: ")  # Get the command from keyboard input
        command = command.strip()
        self._command_list = command.split(" ")
        self._command_list[0] = self._command_list[0].upper()
        if self.is_command_valid(list(self._command_list)):
            return self._command_list
        else:
            return self.get_command()  # If the command is not valid, get another one

    def is_command_valid(self, command: list) -> bool:
        """
        This method checks if a command is valid.
        It also parses file paths with spaces.

        Keyword arguments:
        command -- the command (str)
        return -- True if the command is valid, False otherwise (bool)
        """
        if command[0] in self._available_commands:
            if command[0].upper() in ["RF", "L", "S"]:
                if len(command) == 2:
                    if command[0].upper() == "RF":
                        self.process_commands_form_file()
                    return True
                elif len(command) > 2:  # This is to be able to process file paths with spaces
                    for c in command[2:]:
                        command[1] += " " + c
                    self._command_list = command[:2]
                    if command[0].upper() == "RF":
                        self.process_commands_form_file()
                    return True
                else:
                    print("Expected 1 argument ", len(command) - 1, " given")
                    return False
            elif command[0].upper() in ["C", "Q"]:
                if len(command) == 1:
                    return True
                else:
                    print("Expected 0 arguments ", len(command) - 1, " given")
                    return False
            elif command[0].upper() == "E":
                if len(command) == 3:
                    return True
                else:
                    print("Expected 2 arguments ", len(command) - 1, " given")
                    return False
        else:
            print("Invalid command.")
            return False

    def process_commands_form_file(self) -> None:
        """
        This method gets the commands from a file and puts it in the command buffer.

        Keyword arguments:
        command -- the command (list)
        """
        file_path = self._command_list[1]
        with open(file_path) as command_file:
            for line in command_file:
                self._command_buffer.append(line)  # Put the command in the end of the queue

    @staticmethod
    def render_spreadsheet(spreadsheet: Spreadsheet) -> None:
        """
        This method prints the spreadsheet.
        """
        print("-------------------------------------------------------------------------------------------------------")
        for cell_id in spreadsheet:
            cell = spreadsheet.get_cell(cell_id)
            if isinstance(cell.content, Formula):
                print(cell.identifier.coordinate, cell.content.textual_representation, cell.content.value.value)
            else:
                print(cell.identifier.coordinate, cell.content.value.value)
        print("-------------------------------------------------------------------------------------------------------")

    @staticmethod
    def command_run_successfully(command: str) -> None:
        """
        This method prints a message if the command was run successfully.
        """
        match command:
            case "RF":
                pass
            case "C":
                print("Spreadsheet created successfully.")
            case "E":
                print("Cell edited successfully.")
            case "L":
                print("Spreadsheet loaded successfully.")
            case "S":
                print("Spreadsheet saved successfully.")
            case "Q":
                pass
            case _:
                raise ValueError("The command is not valid.")

    def render_available_commands(self) -> None:
        """
        This method prints the available commands.
        """
        print("-------------------------------------------------------------------------------------------------------")
        print("Available commands: ")
        print("RF - Read file: This command shall have one argument: the text file pathname.")
        print("C - Create new spreadsheet")
        print("E - Edit cell: The first argument shall be a cell coordinate. The second one shall be the content.")
        print("L - Load spreadsheet from file")
        print("S - Save spreadsheet to file")
        print("Q - Quit")
        print("IMPORTANT: COMMANDS AND ARGUMENTS MUST BE SEPARATED BY A SPACE.")
        print("-------------------------------------------------------------------------------------------------------")
