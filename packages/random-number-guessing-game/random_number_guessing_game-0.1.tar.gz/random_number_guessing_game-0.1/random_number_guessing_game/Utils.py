from enum import Enum

class Options(Enum):
    GUESS_NUMBER = '1'
    GET_HINT = '2'
    EXIT = '3'

class Parity(Enum):
    EVEN = 1
    ODD = 2

PrimeNumbersList = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
FibonacciList = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987]