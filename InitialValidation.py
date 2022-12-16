from CustomExceptions import *  # path: CustomExceptions.py
from Operations import *  # path: Operations.py


def getNumAfter(formula, index):
    """
    getting the WHOLE number AFTER the operator
    :param formula: the current mutation of the formula
    :param index: starting index
    :return: the whole number after the operator
    """
    after_number = formula[index + 1]
    i = 1
    while index + i + 1 < len(formula) and formula[index + i + 1] in valid_digits:
        if formula[index - i - 1] == '-' and index - i - 1 != 0:  # if there is a minus sign in the middle of the formula - break
            i -= 1
            break
        after_number += formula[index + i + 1]
        i += 1
    return after_number


def getNextOperator(operator_index, given_formula):
    """
    get the next operator in the formula after the given index
    :param operator_index: starts checking for an operator from this index
    :param given_formula: the inputted formula from the user
    :return: the found operator
    """
    for check_character in given_formula[operator_index + 1:]:
        if check_character in operators:
            return check_character
    return None


def ConcatSigns(given_formula):
    """
    concatenating '+' sign and then '-' sign to a single '-' sign or double '+' sign to a single '+' sign
    :param given_formula: the reformatted formula
    :return: corrected formula
    """
    while given_formula.count('+-') > 0 or given_formula.count('++') > 0:
        operator_index = 0
        for check_character in given_formula:
            if check_character == '+' and operator_index + 1 < len(given_formula) and given_formula[operator_index + 1] == '-':
                given_formula = given_formula[:operator_index] + '-' + given_formula[operator_index + 2:]
            if check_character == '+' and operator_index + 1 < len(given_formula) and given_formula[operator_index + 1] == '+':
                given_formula = given_formula[:operator_index] + '+' + given_formula[operator_index + 2:]
            operator_index += 1
    return given_formula


def InitialCheck(given_formula):
    """
    checking if the given formula is valid and making necessary initial changes
    :param given_formula: the initial formula that needs to be checked
    :return: if general check invalid, raises custom exception with the relevant message else returns the new formula
    """
    chars_valid = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '(', ')', ' ', '.', '+', '-', '*', '/', '!', '^',
                   '.', '%', '$', '&', '@', '~', '#']

    if given_formula.count('(') != given_formula.count(')'):  # in case number of parentheses doesn't add up
        raise OddParentheses

    # if the first char is an operator, raise exception -> later on, if the first char is a plus sign (cause of concatenation), it will be removed
    if given_formula[0] in operators and given_formula[0] != '-' and given_formula[0] != '~':
        raise InvalidFirstChar(given_formula[0])

    for check_character in given_formula:
        if check_character == '\t':  # if there are tabs in the formula delete them
            given_formula = given_formula.replace('\t', '')

    for check_character in given_formula:
        if check_character == ' ':  # if there are spaces in the formula allow it -> delete them
            given_formula = given_formula.replace(' ', '')

    if len(given_formula) == 0:  # if the formula is empty after deleting spaces
        raise EmptyFormula()

    if given_formula[-1] == '(' or given_formula[0] == ')':  # if there is a '(' at the end of the formula or a ')' at the beginning
        raise EmptyParentheses
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

    # check for contradiction of ~ before !
    operator_index = 0
    for check_character in given_formula:
        if check_character == '~' and getNextOperator(operator_index, given_formula) == '!':
            raise ValueError("can't perform a factorial on a negative number!")
        if check_character == '~':
            Negation().checkValid(operator_index, given_formula)
            after = getNumAfter(given_formula, operator_index)
            Negation().calculate(0, after)
        operator_index += 1

    index = 0
    for check_character in given_formula:  # add '0' before '.' that doesn't have a number in front of it
        if check_character == '.' and (given_formula[index - 1] not in valid_near_dot or index - 1 < 0):
            given_formula = given_formula[:index] + '0.' + given_formula[index + 1:]
        index += 1

    # !GOING BY THE SECOND WAY - FULLY CONCATENATING MINUS SIGNS!
    # check for multiple minus signs in a row until there is no more than 1 minus sign in the formula (per a set of parentheses)
    operator_index = 0
    for check_character in given_formula:
        if check_character == '-' and operator_index + 1 < len(given_formula) and given_formula[
            operator_index + 1] == '-':
            given_formula = given_formula[:operator_index] + '+' + given_formula[operator_index + 2:]
        operator_index += 1
    given_formula = ConcatSigns(given_formula)

    return given_formula


def ParenthesesValid(formula, parentheses_start_index, parentheses_end_index):
    """
    check if the parentheses are valid
    :param formula: the formula that needs to be checked
    :param parentheses_start_index: the index of the '(' that needs to be checked
    :param parentheses_end_index: the index of the ')' that it's positioning needs to be checked
    :return: raise exception if invalid
    """
    if formula[parentheses_start_index + 1] in operators or formula[parentheses_end_index - 1] in operators:  # if there is an operator after '(' or before ')'
        raise ValueError("invalid positioning of operators near parentheses!")

    if len(formula) <= 1:  # if the parentheses are empty or contain only one char
        raise ValueError("parentheses are empty or contain only 1 char")

    can_be_before_parentheses = ['+', '-', '*', '/', '^', '%', '$', '&', '@']
    if (parentheses_start_index - 1 > 0 and formula[parentheses_start_index - 1] not in can_be_before_parentheses) or parentheses_start_index + 1 >= len(formula):
        raise ValueError("char before parentheses is not valid in current place")
