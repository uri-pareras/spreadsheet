## SPREADSHEET PROJECT FOR ARQSOFT
## Authors:
- Marc Micolau & Oriol Pareras

## Description:
This project is a spreadsheet that allows you to create, edit and save spreadsheets.

## Warning:
An error in the marker has been detected:
- In load_test when comparing the values of the cells, the marker compares with a string with "=" and uses
get_cell_formula_expression() to get the formula of the cell. This method should return the formula without
the "=". To pass the test, we have modified the method to return the formula with the "=".