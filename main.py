if __name__ == '__main__':
    operators = ['+', '-', '*', '/', '^', '%', '$', '&', '@', '~', '!', '.', ' ']
    middle_operators = ['+', '-', '*', '/', '^', '%', '$', '&', '@']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '(', ')', ' ']

    equation = input("enter an equation: ")

    if equation.count('(') != equation.count(')'):  # in case number of parentheses doesn't add up
        print("invalid number of parentheses")

    for char in equation:
        if char not in operators and char not in numbers:  # in case a char in the input is invalid
            print("char " + char + " is invalid!")

    for char in equation:
        if char == '(' and equation[equation.rfind(char) + 1] == ')':  # in case there is a ')' after a '('
            print("invalid parentheses")

    for char in equation:
        if char in middle_operators:
            indexOfChar = equation.rfind(char)
            if indexOfChar - 1 < 0 or indexOfChar + 1 == len(equation) or equation[indexOfChar - 1] not in numbers or equation[indexOfChar + 1] not in numbers:
                print("operator '" + char + "' is not in a correct place")

