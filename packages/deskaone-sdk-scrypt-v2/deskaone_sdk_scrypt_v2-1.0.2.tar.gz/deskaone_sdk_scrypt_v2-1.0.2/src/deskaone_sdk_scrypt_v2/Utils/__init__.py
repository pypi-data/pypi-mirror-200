from os import urandom
import random
import string
from .Timer import Timer, Color, Typer
from .Reset import Reset
from .Crypto import Crypto
from .ProgressBar import ProgressBar
from .AWSRequestsAuth import AWSRequestsAuth

class Random:
    
    def __init__(self, __size: int, __mode = 'hex') -> None:self.__size, self.__mode = __size, __mode
    
    def __bytes__(self) -> bytes:return urandom(self.__size)
            
    def __str__(self) -> str:
        if self.__mode == 'letters':return ''.join(random.choice(string.ascii_letters) for _ in range(self.__size))
        elif self.__mode == 'lower':return ''.join(random.choice(string.ascii_lowercase) for _ in range(self.__size))
        elif self.__mode == 'upper':return ''.join(random.choice(string.ascii_uppercase) for _ in range(self.__size))
        elif self.__mode == 'digits':return ''.join(random.choice(string.digits) for _ in range(self.__size))
        elif self.__mode == 'all':return ''.join(random.choice(string.digits + string.ascii_letters) for _ in range(self.__size))
        elif self.__mode == 'hex':return urandom(self.__size).hex()

__all__ = [
    'Timer', 
    'Color',
    'Typer',
    'Reset',
    'Crypto',
    'ProgressBar',
    'AWSRequestsAuth',
    'Random',
]