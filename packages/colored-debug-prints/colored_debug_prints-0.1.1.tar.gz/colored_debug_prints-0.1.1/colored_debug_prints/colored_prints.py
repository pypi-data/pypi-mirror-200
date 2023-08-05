from colorama import *

__all__ = [
    "colors",
    "coloredPrint"
]

colors = Fore

class coloredPrint():
    def print(self, textToPrint, color=None):
        if (color == None):
            raise ValueError("Color can't be None")
        print(f"{color}{textToPrint}{colors.RESET}")
