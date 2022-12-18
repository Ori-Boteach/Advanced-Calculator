from Operations import *  # path: Operations.py

chars_valid = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '(', ')', ' ',
               '.', '+', '-', '*', '/', '!', '^', '.', '%', '$', '&', '@', '~', '#']


def InitialCheck(given_formula):
    """
    checking if the given formula is valid and making necessary initial changes
    :param given_formula: the initial formula that needs to be checked
    :return: if general check invalid, raises custom exception with the relevant message, else, returns the new formula
    """
    if len(given_formula) == 0:
        raise EmptyFormula()

    InvalidFirstCharCheck(given_formula)
    given_formula = SpacesAndTabsCheck(given_formula)
    InvalidParenthesesCheck(given_formula)
    InvalidInputtedChars(given_formula)
    given_formula = InvalidDotsAndCorrection(given_formula)
    NegationCheck(given_formula)
    given_formula = CheckForConcatination(given_formula)
    InvalidFirstCharCheck(given_formula)  # check again for invalid first char after concatination
    return given_formula


def InvalidFirstCharCheck(given_formula):
    # if the first char is an operator, raise exception -> later on, if the first char is a plus sign (cause of concatenation), it will be removed
    if given_formula[0] in operators and given_formula[0] != '-' and given_formula[0] != '~':
        raise InvalidFirstChar(given_formula[0])
    if len(given_formula) == 1 and (given_formula[0] == '-' or given_formula[0] == '~'):
        raise InvalidFirstChar(given_formula[0])


def SpacesAndTabsCheck(given_formula):
    for check_character in given_formula:
        # if there are tabs in the formula delete them
        if check_character == '\t':
            given_formula = given_formula.replace('\t', '')

    for check_character in given_formula:
        # if there are spaces in the formula allow it -> delete them
        if check_character == ' ':
            given_formula = given_formula.replace(' ', '')

    # if the formula is empty after deleting spaces
    if len(given_formula) == 0:
        raise EmptyFormula()
    return given_formula


def InvalidParenthesesCheck(given_formula):
    # in case number of parentheses is odd -> doesn't add up
    if given_formula.count('(') != given_formula.count(')'):
        raise OddParentheses
    # if there is a '(' at the end of the formula or a ')' at the beginning
    if given_formula[-1] == '(' or given_formula[0] == ')':
        raise EmptyParentheses
    for check_character in given_formula:
        # in case of parentheses with invalid content
        if check_character == '(' and given_formula[given_formula.rfind(check_character) + 1] == ')':
            raise EmptyParentheses


def InvalidInputtedChars(given_formula):
    for check_character in given_formula:
        # in case a char in the input is invalid
        if check_character not in chars_valid:
            raise InvalidInput(check_character, given_formula)


def InvalidDotsAndCorrection(given_formula):

    if getNextOperator(1, given_formula) is None and given_formula.count('.') > 1:
        raise InvalidDotsUse

    index = 0
    # add '0' after '.' that doesn't have a number after it
    for check_character in given_formula:
        if check_character == '.' and (given_formula[index + 1] not in valid_near_dot or index + 1 >= len(given_formula)):
            given_formula = given_formula[:index + 1] + '0' + given_formula[index + 1:]
        index += 1

    index = 0
    # check for invalid '.' placement
    for check_character in given_formula:
        if check_character == '.' and given_formula[index + 1] not in valid_near_dot:
            raise InvalidDots(index)
        index += 1

    index = 0
    # add '0' before '.' that doesn't have a number in front of it
    for check_character in given_formula:
        if check_character == '.' and (given_formula[index - 1] not in valid_near_dot or index - 1 < 0):
            given_formula = given_formula[:index] + '0.' + given_formula[index + 1:]
        index += 1

    return given_formula


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


def getNumAfter(formula, index):
    """
    getting the WHOLE number AFTER the operator
    :param formula: the current mutation of the formula
    :param index: starting index
    :return: the whole number after the operator
    """
    after_number = ""
    i = 0
    while index + i + 1 < len(formula) and formula[index + i + 1] in valid_digits:
        # if there is a minus sign, recursively call the function to get the whole number, then add the minus sign and break
        if formula[index + 1] == '-':
            after_number = '-' + getNumAfter(formula, index + 1)
            break
        after_number += formula[index + i + 1]
        i += 1
    return after_number


def NegationCheck(given_formula):
    operator_index = 0
    # check for contradiction of '~' before '!'
    for check_character in given_formula:
        if check_character == '~' and getNextOperator(operator_index, given_formula) == '!' and getNumAfter(given_formula, operator_index).count('(') == 0:
            after = '-' + getNumAfter(given_formula, operator_index)
            raise NegativeFactorial(after)
        if check_character == '~' and getNumAfter(given_formula, operator_index).count('(') == 0 and getNumAfter(given_formula, operator_index).count(')') == 0:
            after = getNumAfter(given_formula, operator_index)
            Negation().checkValid(operator_index, given_formula)
            Negation().calculate(0, after)
        operator_index += 1


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
            if check_character == '-' and operator_index + 1 < len(given_formula) and given_formula[operator_index + 1] == '+':
                given_formula = given_formula[:operator_index] + '-' + given_formula[operator_index + 2:]
            if check_character == '+' and operator_index + 1 < len(given_formula) and given_formula[operator_index + 1] == '+':
                given_formula = given_formula[:operator_index] + '+' + given_formula[operator_index + 2:]
            operator_index += 1
    return given_formula


def CheckForConcatination(given_formula):
    # !GOING BY THE SECOND WAY - FULLY CONCATENATING MINUS SIGNS!
    # check for multiple minus signs in a row and concatenate them
    operator_index = 0
    while operator_index < len(given_formula):
        check_character = given_formula[operator_index]
        if check_character == '-' and operator_index + 1 < len(given_formula) and given_formula[operator_index + 1] == '-':
            if given_formula[operator_index - 1] != '~' and given_formula[operator_index + 2] != '(':  # check for a case like "~--2" or --(-1+2)
                given_formula = given_formula[:operator_index] + '+' + given_formula[operator_index + 2:]
            elif given_formula[operator_index - 1] in valid_near_dot:  # check for a case like "2--(5+1) -> + stays"
                given_formula = given_formula[:operator_index] + '+' + given_formula[operator_index + 2:]
            else:
                given_formula = given_formula[:operator_index] + given_formula[operator_index + 2:]
            operator_index = -1
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
    valid_open_parentheses = ['-', '~']
    valid_close_parentheses = ['!', '#']
    # if there is an operator after '(' or before ')'
    if (formula[parentheses_start_index + 1] in operators and formula[parentheses_start_index + 1] not in valid_open_parentheses) or (formula[parentheses_end_index - 1] in operators and formula[parentheses_end_index - 1] not in valid_close_parentheses):
        raise InvalidNextToParentheses

    # if the parentheses are empty or contain only one char
    if len(formula) <= 1:
        raise EmptyParentheses

    can_be_before_parentheses = ['+', '-', '*', '/', '^', '%', '$', '&', '@', '~', '(']
    if (parentheses_start_index - 1 > 0 and formula[parentheses_start_index - 1] not in can_be_before_parentheses) or parentheses_start_index + 1 >= len(formula):
        raise InvalidNextToParentheses
