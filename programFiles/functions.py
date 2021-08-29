# Functions

# Imports
from os import system, name


# Clear screen
def clear_screen():

    # Windows
    if name == "nt":
        _ = system("cls")

    # Linux & Mac
    else:
        _ = system("clear")
