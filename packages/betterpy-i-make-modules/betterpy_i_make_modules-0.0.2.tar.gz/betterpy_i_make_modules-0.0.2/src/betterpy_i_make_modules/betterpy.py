def reverse_and_print(a):
    reversedstr = a[::-1]
    print(reversedstr)


def print_lowercase(a):
    print(a.lower())


def print_uppercase(a):
    print(a.upper())



def remove_spaces_and_print(a):
    spacesremoved = a.replace(" ", "")
    print(spacesremoved)

def find_gap_generate(num1=10, num2=50):
    default_compare = input(
        "Continue with default compare? (number 1: 10, number 2: 50) (y/n) ")
    if default_compare.lower() == "y":
        print(
            f"The gap between number 1 and number 2 (number 1 - number 2) are: {num1 - num2}")
        print(
            f"The gap between number 2 and number 1 (number 2 - number 1) are: {num2 - num1}")
    elif default_compare.lower() == "n":
        num1 = input("Number 1: ")
        num2 = input("Number 2: ")
        combine1 = num1 - num2
        combine2 = num2 - num1
        print(
            f"The gap between number 1 and number 2 (number 1 - number 2) are: {combine1}")
        print(
            f"The gap between number 2 and number 1 (number 2 - number 1 ) are: {combine2}")


def find_gap_and_print(a, b):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        print(
            f"The gap between variable 1 and variable 2 (variable 1 - variable 2) is: {a - b}")
        print(
            f"The gap between variable 2 and variable 1 (variable 2 - variable 1) is: {b - a}")
    else:
        print("Variable is not an integer or float")
def print_in_yellow(a):
    print(f"\u001b[33m{a}")
def print_in_blue(a):
    print(f"\u001b[34m{a}")
def print_in_magenta(a):
    print(f"\u001b[35m{a}")
def print_in_cyan(a):
    print(f"\u001b[36m{a}")
def print_in_black(a):
    print(f"\u001b[40m{a}")
def print_in_red(a):
    print(f"\u001b[41m{a}")
def print_in_green(a):
    print(f"\u001b[42m{a}")


if __name__ == "__main__":    
    print('It looks like you tried to run this, next time use "from usefultools import *" OR "import usefultools" to use this.')
    exit()