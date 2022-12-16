# Project's Author: Ori Boteach
from Calculation import *   # Path: Calculation.py
from InitialValidation import *  # Path: InitialValidation.py

if __name__ == '__main__':
    print("WELCOME TO YOUR ADVANCED CALCULATOR! made by Ori")
    print("Addition: +, Subtraction: -, Multiplication: *, Division: /, Pow: ^, Division Remainder: %")
    print("Maximum: $, Minimum: &, Average: @, Negation(prefix): ~, Factorial(postfix): !, Sum Digits(postfix): #")

    wants_again = True
    while wants_again:
        try:
            formula = input("Please enter a formula: ")
        except EOFError:
            print("invalid formula! please restart the program")
            break
        if len(formula) == 0:
            raise EmptyFormula()

        new_formula = InitialCheck(formula)
        formula = new_formula
        print("Your formula is: " + formula)

        formula = CalculateParentheses(formula)  # take care of the parentheses calculations
        print("The result: " + Calculate(formula))  # calculate the result of the formula and print it
        pressed = input("Press 'q' to quit or any other key to continue: ")
        if pressed == 'q':
            wants_again = False

    print("THANK YOU FOR USING MY CALCULATOR! HOPE TO SEE YOU AGAIN SOON :)")
