# Project's Author: Ori Boteach
from Calculation import *   # Path: Calculation.py
from InitialValidation import *  # Path: InitialValidation.py


def OpeningMessage():
    """
    printing the opening message
    """
    print("WELCOME TO YOUR ADVANCED CALCULATOR! made by @Ori_Boteach")
    print("Addition: +, Subtraction: -, Multiplication: *, Division: /, Pow: ^, Division Remainder: %")
    print("Maximum: $, Minimum: &, Average: @, Negation(prefix): ~, Factorial(postfix): !, Sum Digits(postfix): #")


def callFunctionsByOrder(input_formula):
    try:
        new_formula = InitialCheck(input_formula)
        if new_formula != input_formula:
            input_formula = new_formula
            print("More elegantly, your formula is: " + input_formula)
    except SyntaxError as e:
        print(e)
        return str(e)
    except ValueError as e:
        print(e)
        return str(e)

    try:
        input_formula = CalculateParentheses(input_formula)  # take care of the parentheses calculations
        input_formula = CheckForConcatination(input_formula)  # after the parentheses calculations, check for AGAIN for concatination
        print("it's RESULT: " + Calculate(input_formula))  # calculate the result of the formula and print it
        return Calculate(input_formula)
    except SyntaxError as e:
        print(e)
        return str(e)
    except ValueError as e:
        print(e)
        return str(e)
    except ZeroDivisionError as e:
        print(e)
        return str(e)
    except OverflowError as e:
        print(e)
        return str(e)


def try_again():
    try:
        pressed = input("Press 'q' to quit or any other key (except ctrl+d) to continue: ")
        if pressed == 'q':
            return False
        return True

    except EOFError:  # if the user pressed ctrl+d when trying to enter a key
        print("Invalid key! Please restart the program")
        exit(1)


if __name__ == '__main__':

    OpeningMessage()
    wants_again = True
    while wants_again:
        try:
            formula = input("Please enter a formula: ")
        except EOFError:
            print("Invalid formula! Please restart the program")
            break

        callFunctionsByOrder(formula)

        wants_again = try_again()

    print("THANK YOU FOR USING MY CALCULATOR! HOPE TO SEE YOU AGAIN SOON :)")
