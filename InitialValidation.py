from Calculation import *  # import the calculation file
from CustomExceptions import *  # import custom exceptions
from operations import *  # import all the operations


def InitialCheck(given_formula):
    """
    checking if the given formula is valid and making necessary initial changes
    :param given_formula:
    :return: if general check invalid, raises custom exception with the relevant message else returns the new formula
    """
    chars_valid = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '(', ')', ' ', '.', '+', '-', '*', '/', '!', '^',
                   '.', '%', '$', '&', '@', '~', '#']
    # in case number of parentheses doesn't add up
    if given_formula.count('(') != given_formula.count(')'):
        raise OddParentheses

    for check_character in given_formula:
        # in case there is a ')' after a '('
        if check_character == '(' and given_formula[given_formula.rfind(check_character) + 1] == ')':
            raise EmptyParentheses

    for check_character in given_formula:
        # in case a char in the input is invalid
        if check_character not in chars_valid:
            raise ValueError("char '" + check_character + "' is invalid!")

    index = 0
    for check_character in given_formula:  # check for invalid '.' placement
        if check_character == '.' and given_formula[index + 1] not in valid_near_dot:
            raise ValueError("chars '.' in index " + str(index) + " and after it are invalid!")
        index += 1

    index = 0
    for check_character in given_formula:  # add '0' before '.' that doesn't have a number in front of it
        if check_character == '.' and (given_formula[index - 1] not in valid_near_dot or index - 1 < 0):
            given_formula = given_formula[:index] + '0.' + given_formula[index + 1:]
        index += 1

    index = 0
    for check_character in given_formula:  # check spaces: if valid - delete them, else - raise exception
        if check_character == ' ':
            if index - 1 < 0 or index + 1 == len(formula) or (
                    formula[index - 1] in valid_digits and formula[index + 1] in valid_digits) and formula[index - 1] != '-':  # invalid
                raise InvalidSpaces
            else:  # valid -> remove space and dec index as a result
                given_formula = given_formula[:index] + given_formula[index + 1:]
                index -= 1
        index += 1

    operator_index = 0
    for check_character in given_formula:  # converting ~ signs to - signs
        if check_character == '~' and (given_formula[operator_index - 1] not in valid_digits or operator_index - 1 < 0):
            given_formula = given_formula[:operator_index] + '-' + given_formula[operator_index + 1:]
        else:
            ValueError("operator '~' is not valid in current place")  # in a case like 3+~4 -> invalid
        operator_index += 1

    # check for multiple minus signs in a row
    operator_index = 0
    changed = False
    for check_character in given_formula:
        if check_character == '-' and operator_index + 1 < len(given_formula) and given_formula[operator_index + 1] == '-':
            given_formula = given_formula[:operator_index] + '+' + given_formula[operator_index + 2:]
            changed = True
        operator_index += 1

    operator_index = 0
    for check_character in given_formula:  # only if there were multiple minus signs in a row concatenate the plus signs
        if changed and check_character == '+' and operator_index + 1 < len(given_formula) and given_formula[operator_index + 1] == '+':
            given_formula = given_formula[:operator_index] + given_formula[operator_index + 1:]
            operator_index -= 1  # if there were a concatenation, index stays in place
        operator_index += 1

    return given_formula


def ParenthesesValid(formula, parentheses_index):
    """
    check if the parentheses are valid
    :param formula: the formula that needs to be checked
    :param parentheses_index: the index of the '(' that needs to be checked
    :return: raise exception if invalid
    """
    if len(formula) <= 1:  # if the parentheses are empty or contain only one char
        raise ValueError("parentheses are empty or contain only 1 char")

    can_be_before_parentheses = ['+', '-', '*', '/', '^', '%', '$', '&', '@']
    if (parentheses_index - 1 > 0 and formula[parentheses_index - 1] not in can_be_before_parentheses) or parentheses_index + 1 >= len(formula):
        raise ValueError("char before parentheses is not valid in current place")