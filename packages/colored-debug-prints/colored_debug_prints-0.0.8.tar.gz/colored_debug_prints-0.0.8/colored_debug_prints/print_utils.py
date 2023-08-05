from colorama import *

init()

__all__ = [
    "debugPrints"
]

class debugPrints():
    def info(self, textToPrint, extraData=None):
        if (extraData != None):
            print(f"{Fore.CYAN}[*] {textToPrint} {Fore.LIGHTBLACK_EX}({extraData}){Fore.RESET}")
        else:
            print(f"{Fore.CYAN}[*] {textToPrint}{Fore.RESET}")

    def warn(self, textToPrint, extraData=None):
        if (extraData != None):
            print(f"{Fore.YELLOW}[*] {textToPrint} {Fore.LIGHTBLACK_EX}({extraData}){Fore.RESET}")
        else:
            print(f"{Fore.YELLOW}[*] {textToPrint}{Fore.RESET}")

    def error(self, textToPrint, extraData=None):
        if (extraData != None):
            print(f"{Fore.RED}[*] {textToPrint} {Fore.LIGHTBLACK_EX}({extraData}){Fore.RESET}")
        else:
            print(f"{Fore.RED}[*] {textToPrint}{Fore.RESET}")

if (__name__ == "__main__"):
    prints = debugPrints()
    prints.info("Hello World!")
    prints.info("Hello World!", "But this is the 2nd print!")
    prints.warn("Hello World, but this is a warning!")
    prints.warn("Hello World, but this is a warning!", "but with extra text")
    prints.error("Hello World, but this is an error!")
    prints.error("Hello World, but this is an error!", "but with extra text")
