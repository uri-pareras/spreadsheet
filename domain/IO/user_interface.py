"""
This file contains the implementation of the user interface.
"""
import abc


class UserInterface(abc.ABC):
    """
    This class represents an abstract user interface.
    """
    @abc.abstractmethod
    def get_command(self) -> str:
        """
        This method prints the available commands and gets the command from the user.
        """
        pass

    @abc.abstractmethod
    def render_spreadsheet(self) -> None:
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

    def get_command(self) -> list:
        """
        This method prints the available commands and gets the command from the user.
        """
        self.render_available_commands()
        command = input("Enter a command: ")
        command = command.strip()
        command = command.upper()
        command_list = command.split(" ")
        if self.is_command_valid(command_list):
            return command_list

    def is_command_valid(self, command: list) -> bool:
        """
        This method checks if a command is valid.

        Keyword arguments:
        command -- the command (str)
        return -- True if the command is valid, False otherwise (bool)
        """
        if command[0].upper() in self._available_commands:
            if command[0].upper() in ["RF", "L", "S"]:
                if len(command) == 2:
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

    def render_spreadsheet(self) -> None:
        """
        This method prints the spreadsheet.
        """
        pass

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
