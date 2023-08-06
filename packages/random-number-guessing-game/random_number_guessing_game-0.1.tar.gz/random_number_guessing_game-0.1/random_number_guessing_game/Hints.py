from enum import Enum

class HintType(Enum):
    LOWER_THAN = '1'
    GREATER_THAN = '2'
    PARITY = '3'
    PRIME = '4'
    PERFECT_SQUARE = '5'
    FIBONACCI = '6'
    DIVIDED_BY_3 = '7'
    DIVIDED_BY_5 = '8'

class HintDescription(Enum):
    LOWER_THAN = 'Lower than'
    GREATER_THAN = 'Higher than'
    PARITY = 'Parity'
    PRIME = 'Prime number'
    PERFECT_SQUARE = 'Perfect square'
    FIBONACCI = 'Fibonacci number'
    DIVIDED_BY_3 = 'Divided by 3'
    DIVIDED_BY_5 = 'Divided by 5'