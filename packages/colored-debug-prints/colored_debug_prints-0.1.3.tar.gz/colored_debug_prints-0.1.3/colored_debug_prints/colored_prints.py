from colorama import *

__all__ = [
    "colors",
    "coloredPrint"
]

colors = Fore

class coloredPrint():
    def print(self, textToPrint, color=None):
        if (color == None):
            print(f"{colors.RED}")
            raise ValueError(f"Color can't be None{colors.RESET}")
        print(f"{color}{textToPrint}{colors.RESET}")
