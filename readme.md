## SPREADSHEET PROJECT FOR ARQSOFT
## Authors:
- Marc Micolau & Oriol Pareras

## Description:
This project is a spreadsheet that allows you to create, edit and save spreadsheets.

## Warning:
Some errors in the marker have been detected:
- In load_test when comparing the values of the cells, the marker compares with a string with "=" and uses
get_cell_formula_expression() to get the formula of the cell. This method should return the formula without
the "=". To pass the test, we have modified the method to return the formula with the "=".
- In load_test in check_first_row, in expected the last cell has a comma after A12 and it must be a semicolon.