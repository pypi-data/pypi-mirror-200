from colorama import *

__all__ = [
    "colors",
    "coloredPrint"
]

colors = Fore

class coloredPrint():
    def print(self, textToPrint, color=None):
        if (color == None):
            raise ValueError(f"{colors.RED}Color can't be None{colors.RESET}")
        print(f"{color}{textToPrint}{colors.RESET}")
