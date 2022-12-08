from main import *


def Calculate(formula):
    """
    calculating the result of the given formula
    :param formula: the formula that needs to be calculated
    :return: the result of the given formula
    """
    operations_dict = {'+': Addition(), '-': Subtraction(), '*': Multiplication(), '/': Division(),
                       '^': Pow(), '@': Average(), '~': Negation(), '%': DivisionRemainder(), '$': Maximum(),
                       '&': Minimum(), '!': Factorial(), '#': SumDigits()}

    priority_dict = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, '%': 4, '$': 5, '&': 5, '@': 5, '~': 6, '!': 6, '#': 6}

    current_priority = 6
    while current_priority > 0:  # scan the formula for each priority
        index = 0
        while index < len(formula):  # go over the formula

            flag = False  # a flag to check if there are still operations to be done
            for character in formula:  # go over the formula
                if character in operators and character != '-':
                    flag = True
            if not flag and formula.count(
                    '.') > 1:  # if the final result and there are more than 1 dot, raise exception
                raise ValueError("invalid number - wrong use of '.'")
            if not flag and formula[0] == '-':  # if there are no more operations to be done, result is negative, break
                break

            character = formula[index]
            if character in operators:  # if the char is an operator, else inc index
                if priority_dict[character] == current_priority:  # if operator is the right priority
                    operations_dict[character].checkValid(index, formula)  # check if the operator is valid
                    if index + 1 < len(formula) and index - 1 >= 0:  # if operator is in the middle of the formula
                        # getting the WHOLE number BEFORE the operator
                        prior_number = formula[index - 1]
                        i = 1
                        while formula[index - i - 1] in valid_digits and index - i - 1 >= 0:
                            if formula[
                                index - i - 1] == '-' and index - i - 1 != 0:  # if there is a minus sign in the middle of the formula - break
                                i -= 1
                                break
                            prior_number = formula[index - i - 1] + prior_number
                            i += 1
                        # getting the WHOLE number AFTER the operator
                        after_number = formula[index + 1]
                        i = 1
                        while index + i + 1 < len(formula) and formula[index + i + 1] in valid_digits:
                            if formula[
                                index - i - 1] == '-' and index - i - 1 != 0:  # if there is a minus sign in the middle of the formula - break
                                i -= 1
                                break
                            after_number += formula[index + i + 1]
                            i += 1
                        if after_number.count('.') > 1 or prior_number.count(
                                '.') > 1:  # if there are more than 1 dot in a number
                            raise ValueError("invalid number - wrong use of '.'")
                        current_result = operations_dict[character].calculate(prior_number, after_number)
                    elif index + 1 >= len(formula):  # if the operator is at the end of the formula
                        # getting the WHOLE number BEFORE the operator
                        prior_number = formula[index - 1]
                        i = 1
                        while formula[index - i - 1] in valid_digits and index - i - 1 >= 0:
                            if formula[
                                index - i - 1] == '-' and index - i - 1 != 0:  # if there is a minus sign in the middle of the formula - break
                                i -= 1
                                break
                            prior_number = formula[index - i - 1] + prior_number
                            i += 1
                        after_number = ""
                        if after_number.count('.') > 1 or prior_number.count(
                                '.') > 1:  # if there are more than 1 dot in a number
                            raise ValueError("invalid number - wrong use of '.'")
                        current_result = operations_dict[character].calculate(prior_number, 0)
                    else:  # if the operator is at the beginning of the formula
                        prior_number = ""
                        # getting the WHOLE number BEFORE the operator
                        after_number = formula[index + 1]
                        i = 1
                        while index + i + 1 < len(formula) and formula[index + i + 1] in valid_digits:
                            if formula[
                                index - i - 1] == '-' and index - i - 1 != 0:  # if there is a minus sign in the middle of the formula - break
                                i -= 1
                                break
                            after_number += formula[index + i + 1]
                            i += 1
                        if after_number.count('.') > 1 or prior_number.count(
                                '.') > 1:  # if there are more than 1 dot in a number
                            raise ValueError("invalid number - wrong use of '.'")
                        current_result = operations_dict[character].calculate(after_number, 0)

                    # update the formula:
                    # everything before the num prior to the operator + the result of the calc + everything after the num after the operator
                    formula = formula[:index - len(prior_number)] + str(float(current_result)) + formula[index + len(
                        after_number) + 1:]
                    if character != '-':  # if the operator is not a minus sign
                        index = -1  # reset index and start over from the beginning

            index += 1  # move to the next char

        current_priority -= 1  # go down a level of priority
    return formula


def CalculateParentheses(formula):  # take care of the parentheses
    index = 0
    for character in formula:  # go over the formula
        if character == '(':  # if a '(' is found
            parentheses_index = formula.rfind(character)  # find the last index of the '('
            parentheses_content = formula[parentheses_index + 1:formula.find(')',
                                                                             parentheses_index)]  # get the content of the most inner parentheses
            ParenthesesValid(formula, parentheses_index)  # check if the position of the parentheses is valid
            parentheses_content = Calculate(parentheses_content)  # calculate the content of the parentheses
            formula = formula[:parentheses_index] + str(parentheses_content) + formula[formula.find(')',
                                                                                                    parentheses_index) + 1:]  # replace the parentheses with the calculated content
            index -= 1  # if there was a change, index stays in place
        index += 1

    return str(formula)
