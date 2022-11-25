from operations import *
from CustomExceptions import *


def InitialCheck(given_formula):
    """
    checking if the given formula is valid and making necessary initial changes
    :param given_formula:
    :return: if general check invalid, raises custom exception with the relevant message else returns the new formula
    """
    chars_valid = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '(', ')', ' ', '.', '+', '-', '*', '/', '!', '^',
                   '.', '%', '$', '&', '@', '~']
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

    # check spaces: if valid - delete them, else - raise exception
    index = 0
    for check_character in given_formula:
        if check_character == ' ':
            operator_index = given_formula.rfind(check_character)
            if operator_index - 1 < 0 or operator_index + 1 == len(formula) or (
                    formula[operator_index - 1] in numbers and formula[operator_index + 1] in numbers):  # invalid
                raise InvalidSpaces
            else:  # valid -> remove space and dec index as a result
                given_formula = given_formula[:index] + given_formula[index + 1:]
                index -= 1
        index += 1

    operator_index = 0
    for check_character in given_formula:  # converting ~ signs to - signs
        if check_character == '~' and given_formula[operator_index - 1] not in numbers:
            given_formula = given_formula[:operator_index] + '-' + given_formula[operator_index + 1:]
        elif check_character == '~' and operator_index - 1 < 0:  # TODO: doesnt work for ~3
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

    operator_index = 0  # TODO: what about 2+-3 ???
    for check_character in given_formula:  # only if there were multiple minus signs in a row concatenate the plus signs
        if changed and check_character == '+' and operator_index + 1 < len(given_formula) and given_formula[operator_index + 1] == '+':
            given_formula = given_formula[:operator_index] + given_formula[operator_index + 1:]
            operator_index -= 1  # if there were a concatenation, index stays in place
        operator_index += 1

    return given_formula


def Calculate(formula):
    """
    calculating the result of the given formula
    :param formula: the formula that needs to be calculated
    :return: the result of the given formula
    """
    operations_dict = {'+': Addition(), '-': Subtraction(), '*': Multiplication(), '/': Division(),
                       '^': Pow().checkValid, '@': Average(), '~': Negation(), '%': DivisionRemainder(), '$': Maximum,
                       '&': Minimum, '!': Factorial()}

    priority_dict = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, '%': 4, '$': 5, '&': 5, '@': 5, '~': 6, '!': 6}

    current_priority = 6
    while current_priority > 0:  # scan the formula for each priority
        index = 0
        while index < len(formula):  # go over the formula
            character = formula[index]
            if character in operators:  # if the char is an operator, else inc index
                if priority_dict[character] == current_priority:  # if operator is the right priority
                    # todo: doesn't work for & and $ and what to do with decimal numbers??? 2.1+2 ?
                    operations_dict[character].checkValid(index, formula)  # check if the operator is valid
                    if index + 1 < len(formula):  # if ok, calculate the result
                        # getting the WHOLE number BEFORE the operator
                        prior_number = formula[index - 1]
                        i = 1
                        while formula[index - i - 1] in numbers and index - i - 1 >= 0:
                            prior_number = formula[index - i - 1] + prior_number
                            i += 1
                        # getting the WHOLE number BEFORE the operator
                        after_number = formula[index + 1]
                        i = 1
                        while index + i + 1 < len(formula) and formula[index + i + 1] in numbers:
                            after_number += formula[index + i + 1]
                            i += 1
                        current_result = operations_dict[character].calculate(prior_number, after_number)
                    else:
                        current_result = operations_dict[character].calculate(formula[index - 1], 0)

                    # update the formula:
                    # everything before the num prior to the operator + the result of the calc + everything after the num after the operator
                    formula = formula[:index - len(prior_number)] + str(int(current_result)) + formula[index + len(after_number) + 1:]
                    print("new formula: " + formula)
                    index = -1  # reset index and start over from the beginning

            index += 1  # move to the next char

        current_priority -= 1  # go down a level of priority
    return formula


def CalculateParentheses(formula):  # take care of the parentheses
    index = 0
    for character in formula:  # go over the formula
        if character == '(':  # if a '(' is found
            parentheses_index = formula.rfind(character)  # find the last index of the '('
            parentheses_content = formula[parentheses_index + 1:formula.find(')', parentheses_index)]  # get the content of the most inner parentheses
            ParenthesesValid(formula, parentheses_index)  # check if the position of the parentheses is valid
            parentheses_content = Calculate(parentheses_content)  # calculate the content of the parentheses
            formula = formula[:parentheses_index] + str(parentheses_content) + formula[formula.find(')', parentheses_index) + 1:]  # replace the parentheses with the calculated content
            index -= 1  # if there was a change, index stays in place
        index += 1

    print("after dealing with the parentheses the formula is: " + str(formula))
    return str(formula)


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
    if (parentheses_index - 1 > 0 and formula[parentheses_index -1] not in can_be_before_parentheses) or parentheses_index + 1 >= len(formula):
        raise ValueError("char before parentheses is not valid in current place")


if __name__ == '__main__':
    formula = input("Please enter a formula: ")
    new_formula = InitialCheck(formula)
    formula = new_formula
    print("Your formula is: " + formula)

    formula = CalculateParentheses(formula)  # take care of the parentheses calculations
    print("The result: " + Calculate(formula))  # calculate the result of the formula and print it
