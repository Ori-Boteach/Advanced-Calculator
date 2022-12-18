from InitialValidation import ParenthesesValid, CheckForConcatination  # path: InitialValidation.py
from Operations import *  # path: Operations.py


def getNumBefore(formula, index):
    """
    getting the WHOLE number BEFORE the operator
    :param formula: the current mutation of the formula
    :param index: starting index
    :return: the whole number before the operator
    """
    prior_number = formula[index - 1]
    i = 1
    while formula[index - i - 1] in valid_digits and index - i - 1 >= 0:
        # if there is a minus sign in the middle of the formula - break
        if formula[index - i - 1] == '-' and index - i - 1 != 0:
            # catch edge case such as -> 9-~3@9 == 9-(-3)@9
            if formula[index - i - 2] == '-':
                prior_number = '-' + prior_number
            break
        prior_number = formula[index - i - 1] + prior_number
        i += 1
    return prior_number


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
        # if there is an operator in the middle of the formula - break
        if formula[index + i+1] in operators:
            break
        after_number += formula[index + i + 1]
        i += 1
    return after_number


def Calculate(formula):
    """
    calculating the result of the given formula
    :param formula: the formula that needs to be calculated
    :return: the result of the given formula
    """
    operations_dict = {'+': Addition(), '-': Subtraction(), '*': Multiplication(), '/': Division(), '^': Pow(), '@': Average(),
                       '~': Negation(), '%': DivisionRemainder(), '$': Maximum(), '&': Minimum(), '!': Factorial(), '#': SumDigits()}

    priority_dict = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, '%': 4, '$': 5, '&': 5, '@': 5, '~': 6, '!': 6, '#': 6}

    current_priority = 6
    while current_priority > 0:  # scan the formula for each priority
        index = 0
        while index < len(formula):  # go over the formula
            check = False  # boolean flag -> not changing the formula if it starts with a minus sign

            flag = False  # a flag to check if there are still operations to be done
            for character in formula:  # go over the formula
                if character in operators and character != '-':
                    flag = True

            # if the final result and there are more than 1 dot, raise exception
            if not flag and formula.count('.') > 1 and formula[0] == '-' and formula.count("-") == 1:
                raise InvalidDotsUse()

            # if there are no more operations to be done, result is negative, break
            if not flag and formula[0] == '-' and formula.count("-") == 1:
                break

            # if the first character is '+', remove it (knowing that it's a result of concatenation of minus signs)
            if formula[0] == '+':
                formula = formula.replace('+', '')

            character = formula[index]
            # if the char is an operator, else inc index
            if character in operators:

                if priority_dict[character] == current_priority:  # if operator is the right priority
                    operations_dict[character].checkValid(index, formula)  # check if the operator is valid

                    if index + 1 < len(formula) and index - 1 >= 0:  # if operator is in the middle of the formula
                        prior_number = getNumBefore(formula, index)
                        prior_number = CheckForConcatination(prior_number)  # concatenate signs if needed
                        after_number = getNumAfter(formula, index)
                        after_number = CheckForConcatination(after_number)  # concatenate signs if needed
                        if after_number.count('.') > 1 or prior_number.count('.') > 1:  # if there are more than 1 dot in a number
                            raise InvalidDotsUse()
                        if character == '~':  # if the operator is negation
                            prior_number = ""
                        if character == '!' or character == '#':  # if the operator is factorial or sum digits
                            after_number = ""
                        current_result = operations_dict[character].calculate(prior_number, after_number)

                    elif index + 1 >= len(formula):  # if the operator is at the end of the formula
                        prior_number = getNumBefore(formula, index)
                        after_number = ""
                        if after_number.count('.') > 1 or prior_number.count('.') > 1:  # if there are more than 1 dot in a number
                            raise InvalidDotsUse()
                        current_result = operations_dict[character].calculate(prior_number, "")

                    # if the operator is at the beginning of the formula
                    else:
                        prior_number = ""
                        after_number = getNumAfter(formula, index)
                        if after_number.count('.') > 1 or prior_number.count('.') > 1:  # if there are more than 1 dot in a number
                            raise InvalidDotsUse()
                        if formula[0] != '-':  # if the formula starts with a minus sign
                            current_result = operations_dict[character].calculate("", after_number)
                        else:  # if the formula starts with a minus sign
                            current_result = ""
                            check = True

                    # update the formula:
                    # everything before the num prior to the operator + the result of the calc + everything after the num after the operator
                    if str(current_result).count('e') > 0:  # if the result is in scientific notation
                        raise InvalidScientificNotation(character)
                    if not check:
                        formula = formula[:index - len(prior_number)] + str(float(current_result)) + formula[index + len(after_number) + 1:]

                    if character != '-':  # if the operator is not a minus sign
                        index = -1  # reset index and start over from the beginning
            index += 1  # move to the next char
        current_priority -= 1  # go down a level of priority
    return formula


def CalculateParentheses(formula):
    """
    taking care of the calculation of the parentheses
    :param formula: the formula that needs to be calculated
    :return: the formula after the calculation of the parentheses
    """
    index = 0
    found = False
    for character in formula:  # go over the formula
        if character == ')' and not found:  # if there is a closing parenthesis without an opening one
            raise ParenthesesException()

        if character == '(':  # if a '(' is found
            parentheses_index = formula.rfind(character)  # find the last index of the '('
            parentheses_content = formula[parentheses_index + 1:formula.find(')', parentheses_index)]  # get the content of the most inner parentheses
            ParenthesesValid(formula, parentheses_index, formula.find(')'))  # check if the position of the parentheses is valid
            parentheses_content = Calculate(parentheses_content)  # calculate the content of the parentheses
            formula = formula[:parentheses_index] + str(parentheses_content) + formula[formula.find(')', parentheses_index) + 1:]  # replace the parentheses with the calculated content
            index -= 1  # if there was a change, index stays in place
            found = True
        index += 1

    return str(formula)
