import sys
from colorama import init, Fore
init(convert=True)

class Logger:
    render = True
    
    @classmethod
    def _basicLog(cls, prefix: str, message: str, color: str, printArgs: dict={ 'end': '\n' }) -> None:
        if not cls.render: return
        print(f'{color}{prefix}{Fore.RESET}{message}', **printArgs)

    @classmethod
    def warning(cls, message: str, printArgs: dict={ 'end': '\n' }) -> None:
        return cls._basicLog('Warning ', message, Fore.LIGHTRED_EX, printArgs)

    @classmethod
    def info(cls, message: str, printArgs: dict={ 'end': '\n' }) -> None:
        return cls._basicLog('Info ', message, Fore.LIGHTBLUE_EX, printArgs)

    @classmethod
    def error(cls, message: str, exitCode: bool=True, printArgs: dict={ 'end': '\n' }) -> None:
        cls._basicLog('Error ', message, Fore.RED, printArgs)
        if exitCode: sys.exit(1)

    @classmethod
    def debug(cls, message: str, printArgs: dict={ 'end': '\n' }) -> None:
        return cls._basicLog('Debug ', message, Fore.LIGHTGREEN_EX, printArgs)

    @classmethod
    def success(cls, message: str, printArgs: dict={ 'end': '\n' }) -> None:
        return cls._basicLog('Success ', message, Fore.GREEN, printArgs)