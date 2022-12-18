# Advanced-Calculator

Building an advanced calculator that includes the basic operations, in addition to several others:
Addition: +, Subtraction: -, Multiplication: *, Division: /, Pow: ^, Division Remainder: %
Maximum: $, Minimum: &, Average: @, Negation(prefix): ~, Factorial(postfix): !, Sum Digits(postfix): #

The main module calls an initial validation check.
Afterwards, the calculating operation begins -> for each operator,based on it's priority, the function checks it's validity, and calculates it's internal result,
which is later on embedded in the mutated formula string in the correct position.
**I CHOSE TO WORK ACCORDING TO WAY 2 - FULLY CONCATENATING THE MINUS SIGNS**
