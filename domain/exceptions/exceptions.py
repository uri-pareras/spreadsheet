"""
This file contains the exceptions of the application.
"""


class BadCoordinateException(Exception):
    """
    This class represents an exception that is raised when the coordinate is not valid.
    """
    def __init__(self, message="The coordinate is not valid."):
        """
        This method initializes the exception.

        Keyword arguments:
        message -- the message of the exception (str)

        Attributes:
        _message -- the message of the exception (str)
        """
        self._message = message


class NoNumberException(Exception):
    """
    This class represents an exception that is raised when the cell does not contain a number.
    """
    def __init__(self, message="The cell does not contain a number."):
        """
        This method initializes the exception.

        Keyword arguments:
        message -- the message of the exception (str)

        Attributes:
        _message -- the message of the exception (str)
        """
        self._message = message


class ReadingSpreadSheetException(Exception):
    """
    This class represents an exception that is raised when the spreadsheet cannot be read.
    """
    def __init__(self, message="The file is not valid."):
        """
        This method initializes the exception.

        Keyword arguments:
        message -- the message of the exception (str)

        Attributes:
        _message -- the message of the exception (str)
        """
        self._message = message


class SavingSpreadSheetException(Exception):
    """
    This class represents an exception that is raised when the spreadsheet cannot be saved.
    """
    def __init__(self, message="The file cannot be saved."):
        """
        This method initializes the exception.

        Keyword arguments:
        message -- the message of the exception (str)

        Attributes:
        _message -- the message of the exception (str)
        """
        self._message = message

class ContentException(Exception):
    """
    This class represents an exception that is raised when the content is not valid.
    """
    def __init__(self, message="The content is not valid."):
        """
        This method initializes the exception.

        Keyword arguments:
        message -- the message of the exception (str)

        Attributes:
        _message -- the message of the exception (str)
        """
        self._message = message


class CircularDependencyException(Exception):
    """
    This class represents an exception that is raised when there is a circular dependency.
    """
    def __init__(self, message="There is a circular dependency."):
        """
        This method initializes the exception.

        Keyword arguments:
        message -- the message of the exception (str)

        Attributes:
        _message -- the message of the exception (str)
        """
        self._message = message
