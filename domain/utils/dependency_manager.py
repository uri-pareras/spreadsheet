"""
This file contains the DependencyManager class.
"""
from domain.entities.content import NumericalContent
from domain.entities.spreadsheet import Spreadsheet
from domain.entities.cell import Cell, CellIdentifier
from domain.entities.function import Function
from domain.entities.range import Range
from domain.entities.value import NumericalValue
from domain.exceptions.exceptions import CircularDependencyException


class DependencyManager:
    """
    This class is responsible for managing the dependencies and detecting circular dependencies.
    """

    def __init__(self, spreadsheet: Spreadsheet):
        """
        This method initializes the dependency manager.

        Keyword arguments:
        spreadsheet -- the spreadsheet (Spreadsheet)

        Attributes:
        _spreadsheet -- the spreadsheet (Spreadsheet)
        """
        self._spreadsheet = spreadsheet

    def get_dependencies(self, expression: list) -> list:
        """
        This method returns the dependencies of an expression.

        Keyword arguments:
        expression -- the expression (list of FormulaComponents)
        return -- the dependencies (list of CellIdentifiers)
        """
        dependencies = []
        for component in expression:
            if isinstance(component, Cell):
                dependencies.append(component.identifier)
            elif isinstance(component, Function):
                for argument in component.arguments:
                    if isinstance(argument, Cell):
                        dependencies.append(argument.identifier)
                    elif isinstance(argument, Range):
                        for cell_id in argument.obtain_all_cell_ids():
                            dependencies.append(cell_id)
        return dependencies

    def remove_old_dependencies(self, cell: Cell):
        """
        This method removes the current cell from the depends_on_me lists of the cells that depend on it.
        """
        for dependency in cell.depends_on:
            dep_cell = self._spreadsheet.get_cell(dependency)
            if dep_cell is not None:
                dep_cell.depends_on_me.remove(cell.identifier)

    def update_depends_on_me_lists(self, new_formula: CellIdentifier, dependencies: list) -> None:
        """
        This method updates the dependencies of the cells that depend on the new_formula.

        Keyword arguments:
        new_formula -- the new formula (CellIdentifier)
        dependencies -- the dependencies of the new formula (list of CellIdentifiers)
        """
        for dep_id in dependencies:
            dep_cell = self._spreadsheet.get_cell(dep_id)
            if dep_cell is not None:
                if new_formula not in dep_cell.depends_on_me:
                    dep_cell.add_dependency(new_formula)
            else:
                self._spreadsheet.add_cell(Cell(dep_id, NumericalContent(NumericalValue(None))))
                self._spreadsheet.get_cell(dep_id).add_dependency(new_formula)

    def detect_circular_dependencies(self, origin_cell: CellIdentifier, cell: Cell) -> bool:
        """
        This method detects circular dependencies.

        Keyword arguments:
        cell -- the cell containing the new Formula to check (Cell)
        return -- True if there are circular dependencies, False otherwise (bool)
        """
        dependencies = cell.depends_on_me
        for dependency in dependencies:
            if dependency == origin_cell:
                return True
            else:
                return self.detect_circular_dependencies(origin_cell, self._spreadsheet.get_cell(dependency))

        return False
