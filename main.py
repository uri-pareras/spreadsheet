"""
Authors: Marc Micolau & Oriol Pareras
Date: 24/11/2020
Description: This is the main file of the spreadsheet project.
"""
from controller.controller import Controller


def main() -> None:
    """
    This method runs the application.
    """
    controller = Controller()
    controller.run()


if __name__ == "__main__":
    main()
