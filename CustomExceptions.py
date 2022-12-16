class EmptyParentheses(Exception):
    """
    in case there is a ')' after a '('
    """
    def __init__(self):
        pass

    def __str__(self):
        return "invalid use of parentheses!"


class OddParentheses(Exception):
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
