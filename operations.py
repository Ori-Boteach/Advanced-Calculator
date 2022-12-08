from math import *

operators = ['+', '-', '*', '/', '^', '%', '$', '&', '@', '~', '!', '#']
middle_operators = ['+', '-', '*', '/', '^', '%', '$', '&', '@']
valid_digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '(', ')', '.', '-']
valid_near_dot = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


def checkValidForMiddleOperator(MiddleOperator, operator_index, formula):
    if (operator_index - 1 < 0 or operator_index + 1 == len(formula) or formula[
        operator_index - 1] not in valid_digits or formula[operator_index + 1] not in valid_digits) and formula[operator_index - 1] != '!':
        raise ValueError("operator '" + MiddleOperator + "' is not valid in current index: " + str(
            operator_index) + ", formula: " + formula)


class Operator(object):  # the base class for all operators
    def calculate(self, num1, num2):
        pass

    def checkValid(self, index, formula):
        pass


class Addition(Operator):  # +
    def __init__(self):
        pass

    def calculate(self, num1, num2):
        """
        :return: the value of the addition of the two given numbers
        """
        return float(num1) + float(num2)

    def checkValid(self, index, formula):
        checkValidForMiddleOperator('+', index, formula)


class Subtraction(Operator):  # -
    def __init__(self):
        pass

    def calculate(self, num1, num2):
        """
        :return: the value of the subtraction of the two given numbers
        """
        if num2 != 0:
            return float(num1) - float(num2)
        else:
            return float(num1) * -1.0

    def checkValid(self, index, formula):
        if len(formula) == 1 or formula[index + 1] not in valid_digits:
            raise ValueError("operator '-' is not valid in current index: " + str(
                index) + ", formula: " + formula)


class Multiplication(Operator):  # *
    def __init__(self):
        pass

    def calculate(self, num1, num2):
        """
        :return: the value of the multiplication of the two given numbers
        """
        return float(num1) * float(num2)

    def checkValid(self, index, formula):
        checkValidForMiddleOperator('*', index, formula)


class Division(Operator):  # /
    def __init__(self):
        pass

    def calculate(self, num1, num2):
        """
        :return: the value of the division of the two given numbers
        """
        return float(num1) / float(num2)

    def checkValid(self, index, formula):
        checkValidForMiddleOperator('/', index, formula)
        if formula[index + 1] == 0:
            raise ZeroDivisionError("can't divide by zero")


class Pow(Operator):  # ^
    def __init__(self):
        pass

    def calculate(self, num1, num2):
        """
        :return: the value of the pow of the first given number by the second given number
        """
        return pow(float(num1), float(num2))

    def checkValid(self, index, formula):
        checkValidForMiddleOperator('^', index, formula)


class DivisionRemainder(Operator):  # %
    def __init__(self):
        pass

    def calculate(self, num1, num2):
        """
        :return: the value of the reminder as a result of the division of the two given numbers
        """
        return float(num1) % float(num2)

    def checkValid(self, index, formula):
        checkValidForMiddleOperator('%', index, formula)


class Maximum(Operator):  # $
    def __init__(self):
        pass

    def calculate(self, num1, num2):
        """
        :return: the maximum value between the two given numbers
        """
        if float(num1) > float(num2):
            return float(num1)
        else:
            return float(num2)

    def checkValid(self, index, formula):
        checkValidForMiddleOperator('$', index, formula)


class Minimum(Operator):  # &
    def __init__(self):
        pass

    def calculate(self, num1, num2):
        """
        :return: the minimum value between the two given numbers
        """
        if float(num1) < float(num2):
            return float(num1)
        else:
            return float(num2)

    def checkValid(self, index, formula):
        checkValidForMiddleOperator('&', index, formula)


class Average(Operator):  # @
    def __init__(self):
        pass

    def calculate(self, num1, num2):
        """
        calculating the average of both given numbers
        :return: the average of both given numbers
        """
        return (float(num1) + float(num2)) / 2

    def checkValid(self, index, formula):
        """
        checking if '@' char in the given formula is valid
        :return: True if valid, False otherwise
        """
        checkValidForMiddleOperator('@', index, formula)


class Negation(Operator):  # ~
    def __init__(self):
        pass

    def calculate(self, num_not_used, num):
        """
        :return: the value of the negation of given number
        """
        return -float(num)

    def checkValid(self, index, formula):
        """
        checking if '~' char in the given formula is valid
        :return: True if valid, False otherwise
        """
        if index + 1 == len(formula) or formula[index + 1] not in valid_digits:
            raise ValueError("operator '~' is not in a correct place")


class Factorial(Operator):  # !
    def __init__(self):
        pass

    def calculate(self, num, num_not_used):
        """
        calculating the factorial of the given number
        :return: the value of the given number factorial
        """
        dot_index = str(float(num)).find('.')
        if str(float(num))[dot_index+1] != '0':
            raise ValueError("can't calculate factorial of a non integer number")
        if float(num) < 0:
            raise ValueError("can't calculate factorial of negative number")
        if float(num) == 1:
            return 1
        return float(num) * self.calculate(float(num) - 1, num_not_used)

    def checkValid(self, index, formula):
        """
        checking if '!' char in the given formula is valid
        :return: True if valid, False otherwise
        """
        if index + 1 < len(formula):
            if index - 1 < 0 or formula[index - 1] not in valid_digits:
                raise ValueError("operator '!' is not in a correct place")
            if formula[index + 1] in valid_digits:
                raise ValueError("missing operator after '!'")


class SumDigits(Operator):  # #
    def __init__(self):
        pass

    def calculate(self, num, num_not_used):
        """
        calculating the sum of the digits of the given number
        :return: the sum of the digits of the given number
        """
        num = int(num)
        sum_digits = 0
        while num != 0:
            sum_digits += num % 10
            num = num // 10

        while sum_digits >= 10:
            sum_digits = sum_digits // 10 + sum_digits % 10
        return sum_digits

    def checkValid(self, index, formula):
        """
        checking if '#' char in the given formula is valid
        :return: True if valid, False otherwise
        """
        if index + 1 < len(formula):
            if formula[index - 1] not in valid_digits:
                raise ValueError("operator '#' is not in a correct place")
            if index + 1 != len(formula) and formula[index + 1] in valid_digits:
                raise ValueError("missing operator after '#'")
