class ParenthesesException(Exception):
    """
    the base class exception for all parentheses exceptions
    """
    def __init__(self):
        pass

    def __str__(self):
        pass


class EmptyParentheses(ParenthesesException):
    """
    in case the user inputted an empty parentheses or a parentheses with invalid content
    """
    def __init__(self):
        pass

    def __str__(self):
        return "the content of the parentheses is invalid"


class InvalidNextToParentheses(ParenthesesException):
    """
    in case there is an operator after '(' or before ')'
    """
    def __init__(self):
        pass

    def __str__(self):
        return "invalid positioning of operators near opening/closing parentheses"


class OddParentheses(ParenthesesException):
    """
    in case number of parentheses doesn't add up
    """
    def __init__(self):
        pass

    def __str__(self):
        return "invalid number of parentheses!"


class InvalidFirstChar(Exception):
    """
    in case the first char in the formula is an operator
    """
    def __init__(self, char):
        self.char = char

    def __str__(self):
        return "invalid first character: " + self.char


class EmptyFormula(Exception):
    """
    in case the formula is empty after deleting spaces
    """
    def __init__(self):
        pass

    def __str__(self):
        return "empty formula!"


class InvalidInput(Exception):
    """
    in case a char in the input is invalid
    """
    def __init__(self, check_character, given_formula):
        self.check_character = check_character
        self.given_formula = given_formula

    def __str__(self):
        return "char '" + self.check_character + "' is invalid in index " + str(self.given_formula.index(self.check_character)) + " of the formula!"


class InvalidDots(Exception):
    """
    in case a char in the input is invalid
    """
    def __init__(self, index):
        self.index = index

    def __str__(self):
        return "chars '.' in indexes " + str(self.index) + " and " + str(self.index + 1) + " are invalid!"


class InvalidDotsUse(Exception):
    """
    in case there was a misuse of the '.' operator
    """
    def __init__(self):
        pass

    def __str__(self):
        return "invalid use of '.'"


class NegativeFactorial(Exception):
    """
    in case a char in the input is invalid
    """
    def __init__(self, number):
        self.number = number

    def __str__(self):
        return "can't perform a factorial on a negative number: " + self.number
