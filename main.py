from operations import *
from CustomExceptions import *


def InitialCheck(given_formula):
    """
    checking if the given formula is valid
    :param given_formula:
    :return: if general check invalid, raises custom exception
    """
    chars_valid = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '(', ')', ' ', '.', '+', '-', '*', '/', '!', '^',
                   '.', '%', '$', '&', '@']
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

    # check for multiple minus signs in a row
    operator_index = 0
    changed = False
    for check_character in given_formula:
        if check_character == '-' and operator_index + 1 < len(given_formula) and given_formula[operator_index + 1] == '-':
            given_formula = given_formula[:operator_index] + '+' + given_formula[operator_index + 2:]
            changed = True
        operator_index += 1

    print("before: "+given_formula)
    operator_index = 0  # TODO: 2--3=5 ok ??? and what about 2+-3 ???
    for check_character in given_formula:  # only if there were multiple minus signs in a row concatenate the plus signs
        if changed and check_character == '+' and operator_index + 1 < len(given_formula) and given_formula[operator_index + 1] == '+':
            given_formula = given_formula[:operator_index] + given_formula[operator_index + 1:]
            operator_index -= 1  # if there were a concatenation, index stays in place
        operator_index += 1

    print("after: "+given_formula)
    return given_formula


if __name__ == '__main__':
    formula = input("enter a formula: ")
    new_formula = InitialCheck(formula)
    formula = new_formula
    print("Your formula is: " + formula)

    operations_dict = {'+': Addition(), '-': Subtraction(), '*': Multiplication(), '/': Division(),
                       '^': Pow().checkValid, '@': Average(), '~': Negation(), '%': DivisionRemainder(), '$': Maximum,
                       '&': Minimum, '!': Factorial()}

    priority_dict = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, '%': 4, '$': 5, '&': 5, '@': 5, '~': 6,
                     '!': 6}  # TODO: add parentheses

    current_priority = 6
    current_result = 0
    while current_priority > 0:  # scan the formula for each priority TODO: what about double parentheses?
        index = 0
        for character in formula:  # go over the formula
            # if the char is an operator and at the right priority
            if character in operators and priority_dict[character] == current_priority:
                # todo: doesn't work for & and $ and what to do with decimal numbers???
                operations_dict[character].checkValid(index, formula)  # check if the operator is valid
                if index + 1 < len(formula):  # calculate the result
                    current_result = operations_dict[character].calculate(formula[index - 1], formula[index + 1])
                else:
                    current_result = operations_dict[character].calculate(formula[index - 1], 0)

                formula = formula[:index - 1] + str(int(current_result)) + formula[index + 2:]  # update the formula
                print("new formula: " + formula)
                index = -1  # reset index
            index += 1
        current_priority -= 1  # go down a level of priority

    print("The result: " + str(formula))
