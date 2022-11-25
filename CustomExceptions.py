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


class InvalidSpaces(Exception):
    """
    in case there are blank spaces between two numbers
    """

    def __init__(self):
        pass

    def __str__(self):
        return "invalid use of blank spaces"
