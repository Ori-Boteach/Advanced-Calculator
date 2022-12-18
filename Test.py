from main import *


def test_syntax_exceptions():
    assert callFunctionsByOrder("12.12.12") == "invalid use of '.'"
    assert callFunctionsByOrder("1/1000000") == "WOW! the calculator can't handle the result of the operator /'s calculation!"
    assert callFunctionsByOrder("2-+3") == "operator '-' is not valid in current index: 1, formula: 2-+3"
    assert callFunctionsByOrder("2+3-") == "operator '-' is not valid in current index: 3, formula: 5.0-"
    assert callFunctionsByOrder("~2~3!") == "can't perform a factorial on a negative number: -3"


def test_odd_and_empty_inputs():
    assert callFunctionsByOrder("abcdefg") == "char 'a' is invalid in index 0 of the formula!"
    assert callFunctionsByOrder("ori's calculator is the best") == "char 'o' is invalid in index 0 of the formula!"
    assert callFunctionsByOrder("") == "EMPTY formula!"
    assert callFunctionsByOrder(" -  ") == "Invalid first character: -"
    assert callFunctionsByOrder("\t") == "EMPTY formula!"
    assert callFunctionsByOrder("\t   \t      \t      ") == "EMPTY formula!"


def test_simple_formulas():
    assert callFunctionsByOrder("1+2") == "3.0"
    assert callFunctionsByOrder("1-2") == "-1.0"
    assert callFunctionsByOrder("2*3") == "6.0"
    assert callFunctionsByOrder("2/3") == str(2 / 3)
    assert callFunctionsByOrder("2%3") == "2.0"
    assert callFunctionsByOrder("-2^3") == "-8.0"
    assert callFunctionsByOrder("2$3") == "3.0"
    assert callFunctionsByOrder("2&3") == "2.0"
    assert callFunctionsByOrder("2@3") == str((2 + 3) / 2)
    assert callFunctionsByOrder("~3") == "-3.0"
    assert callFunctionsByOrder("3!") == "6.0"
    assert callFunctionsByOrder("3!!") == "720.0"
    assert callFunctionsByOrder("123#") == "6.0"
    assert callFunctionsByOrder("99##") == "9.0"


def test_minuses_and_negation():
    assert callFunctionsByOrder("2--3") == "5.0"
    assert callFunctionsByOrder("2-~3!") == "can't perform a factorial on a negative number: -3"
    assert callFunctionsByOrder("2--3!") == "8.0"
    assert callFunctionsByOrder("2---3#") == "-1.0"
    assert callFunctionsByOrder("---3") == "-3"
    assert callFunctionsByOrder("2---3!") == "-4.0"
    assert callFunctionsByOrder("-3!") == "can't perform a factorial on a negative number: -3"
    assert callFunctionsByOrder("2--~3") == "-1.0"
    assert callFunctionsByOrder("--~---~3") == "can't negate operator: ---"


def test_complex_formulas():
    assert callFunctionsByOrder("((~(4^   3!$9-8 @33)  )&9*  21 #-   93218#)@42  069") == "-372162.25"
    assert callFunctionsByOrder("(122+33*(   4^3! $ (9- 8@33 ) ) )$ ( 9*  3! - 93218# )") == "135290.0"
    assert callFunctionsByOrder("(4! - (5.5^3)#)$ (1 231 23@6! )@(~5 43)") == "30689.25"
    assert callFunctionsByOrder("(~-23  4*5  43)#-(543  43^0.1)@69 420$(133 7)") == "-34693.4875938195"
    assert callFunctionsByOrder("(420-69+1337)# -~((-2)^3)!$(2.5^2@3)  ----82366") == "42069.0"
    assert callFunctionsByOrder("5318008 +(69 -42*10 )/1&7 ^5%42 @9%2  - (9-0 9090 909. 9 )^1") == "14408557.9"
    assert callFunctionsByOrder("(24$3!)@   1.69+7!   *(0.01^2)#    /12*7  -(.1)") == "2952.745"
    assert callFunctionsByOrder("(458%34)-((65-(9!)^0.2)*7%2#-9/7^5)-------(2@2%2$2*2^2)") == "-36.058918339460206"
    assert callFunctionsByOrder("((  (  123#)@6  7312  -381#-~-(5!))*0   .1+2^5@69420%2)") == "33636.41421356237"
    assert callFunctionsByOrder("(1!  -2@3#   +4$- 5%6^ 7&8* 9) -- 10- ~(11!*-12) ") == "-478854135.5"
    assert callFunctionsByOrder("54&2--(542*7^4%34#*2!$2-0.98/76%43)----- -- - (897-(4!)^0.69)") == "2603574.0095242294"
    assert callFunctionsByOrder("1!+2!   -33#+4  4$55&77  ^0-88*9  9--~(1  @2@3#-4%3)^2") == "-8715.5625"
    assert callFunctionsByOrder("731+~(31321)*2 *-321 --- (3!$89@321321$312^0.5)") == "20108412.11971862"
    assert callFunctionsByOrder("((--(-1-  (-2%6  ^7&6)- -0.89)+3  #/2)--1) @1@1@1@2--8$7") == "-246.41312499999998"
    assert callFunctionsByOrder("--(54  3*0.69  )#/123--(9!-~3@  9$  2^  3) ---(365^(55-(32+23)))") == "362853.0650406504"
