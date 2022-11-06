
from colorama import Fore


class Log:
    '''
        Handles all print statements to the terminal
        The 'verboseness' variable controls how verbose the log messages should be:
            * 0 = Default, show only results and error messages
            * 1 = Developer, include info messages
    '''
    verboseness = 0

    @staticmethod
    def info(message: str) -> None:
        if Log.verboseness > 0:
            print(Fore.LIGHTCYAN_EX + "[INFO]: " + message)

    @staticmethod
    def success(message: str) -> None:
        if Log.verboseness > 0:
            print(Fore.GREEN + "[SUCCESS]: " + message)

    @staticmethod
    def error(message: str) -> None:
        if Log.verboseness > 0:
            print(Fore.RED + "[ERROR]: " + message)

    @staticmethod
    def print(message: str) -> None:
        print(Fore.WHITE + message)
