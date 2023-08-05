from colorama import *

__all__ = [
    "colors",
    "coloredPrint"
]

colors = Fore

class coloredPrint():
    def print(textToPrint, color=None):
        if (color == None or not color in colors):
            raise ValueError("Invalid Color")
        print(f"{color}{textToPrint}{colors.RESET}")
