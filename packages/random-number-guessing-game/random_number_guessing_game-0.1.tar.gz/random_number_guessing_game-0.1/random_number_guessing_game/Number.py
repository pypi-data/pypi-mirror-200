import random
import math
from .Hints import HintType
from .Utils import Parity, PrimeNumbersList, FibonacciList

class Number:
    """ Class used for generating a random number and offering
	hints for guessing that number
	
	Attributes:
		rangeMin (int) representing minimum value of the interval in which the number will be generated
		rangeMax (int) representing maximum value of the interval in which the number will be generated
		generatedNumber (int) representing the randomly generated number
        higherHint (int) representing a number lower than the generated number
        lowerHint (int) representing a number higher than the generated number
        parity (boolean) true if the generated number is even, false otherwise 
        prime (boolean) true if the generated number is prime, false otherwise 
		perfectSquare (boolean) true if the generated number is perfectSquare, false otherwise 
        fibonacci (boolean) true if the generated number is fibonacci, false otherwise 
        dividedBy3 (boolean) true if the generated number can be divided by 3, false otherwise 
        dividedBy5 (boolean) true if the generated number can be divided by 5, false otherwise 
	"""
        
    def __init__(self, rangeMin, rangeMax):
        self.rangeMin = rangeMin
        self.rangeMax = rangeMax
        self.generatedNumber = random.randint(rangeMin, rangeMax)
        self.higherHint = rangeMin
        self.lowerHint = rangeMax
        self.parity = None
        self.prime = None
        self.perfectSquare = None
        self.fibonacci = None
        self.dividedBy3 = None
        self.dividedBy5 = None

    def guess(self, number):
        """Function to guess the generated number
		
		Args: 
			number (integer): The number entered for guessing the generated number
		
		Returns: 
			bool: is the entered number equal with the generated number
		"""
        return number == self.generatedNumber
    
    def hints_summary(self):
        """Function to display the summary of the hints
		
		Args: 
			None
		
		Returns: 
			string: a text containing all the important hints
		"""
        lowerThan = "- The number is lower than {}\n".format(self.lowerHint)
        higherThan = "- The number is higher than {}\n".format(self.higherHint)
        summary = "What you know by now:\n" + higherThan + lowerThan

        if (self.parity != None):
            if self.parity == Parity.EVEN:
                summary = summary + "- The number is even\n"
            else:
                summary = summary + "- The number is odd\n"

        if (self.prime != None):
            if self.prime:
                summary = summary + "- The number is prime\n"
            else:
                summary = summary + "- The number is not prime\n"

        if (self.perfectSquare != None):
            if self.perfectSquare:
                summary = summary + "- The number is a perfect square\n"
            else:
                summary = summary + "- The number is not a perfect square\n"
        
        if (self.fibonacci != None):
            if self.perfectSquare:
                summary = summary + "- The number is a Fibonacci number\n"
            else:
                summary = summary + "- The number is not a Fibonacci number\n"

        if (self.dividedBy3 != None):
            if self.dividedBy3:
                summary = summary + "- The number can be divided by 3\n"
            else:
                summary = summary + "- The number can not be divided by 3\n"
        
        if (self.dividedBy5 != None):
            if self.dividedBy5:
                summary = summary + "- The number can be divided by 5\n"
            else:
                summary = summary + "- The number can not be divided by 5\n"
        return summary
    
    def hint(self, hintType):
        """Function that returns a hint for guessing the generated number
		
		Args: 
			hintType: 
		
		Returns: 
			string: a hint for guessing the generated number
		"""
        if (hintType == HintType.LOWER_THAN.value):
            if (self.rangeMin == self.generatedNumber):
                return "Hint: The number is the lowest in [{}, {}] interval".format(self.rangeMin, self.rangeMax)
            else:
                generatedHintNumber = random.randint(self.generatedNumber + 1, self.lowerHint - 1)
                self.lowerHint = generatedHintNumber
                return "Hint: The number is lower than {}".format(generatedHintNumber)
        elif (hintType == HintType.GREATER_THAN.value):
            if (self.rangeMax == self.generatedNumber):
                return "Hint: The number is the highest in [{}, {}] interval".format(self.rangeMin, self.rangeMax)
            else:
                generatedHintNumber = random.randint(self.higherHint + 1, self.generatedNumber - 1)
                self.higherHint = generatedHintNumber
                return "Hint: The number is higher than {}".format(generatedHintNumber)
        elif (hintType == HintType.PARITY.value):
            if (self.generatedNumber % 2 == 0):
                self.parity = Parity.EVEN
                return "Hint: The number is even"
            else:
                self.parity = Parity.ODD
                return "Hint: The number is odd"
        elif (hintType == HintType.PRIME.value):
            if (self.generatedNumber in PrimeNumbersList):
                self.prime = True
                return "Hint: The number is prime"
            else:
                self.prime = False
                return "Hint: The number is not prime"
        elif (hintType == HintType.FIBONACCI.value):
            if (self.generatedNumber in FibonacciList):
                self.fibonacci = True
                return "Hint: The number is prime"
            else:
                self.fibonacci = False
                return "Hint: The number is not prime"
        elif (hintType == HintType.PERFECT_SQUARE.value):
            if (math.sqrt(self.generatedNumber).is_integer()):
                self.perfectSquare = True
                return "Hint: The number is a perfect square"
            else:
                self.perfectSquare = False
                return "Hint: The number is not a perfect square"
        elif (hintType == HintType.DIVIDED_BY_3.value):
            if ((self.generatedNumber / 3).is_integer()):
                self.dividedBy3 = True
                return "Hint: The number can be divided by 3"
            else:
                self.dividedBy3 = False
                return "Hint: The number can not be divided by 3"
        elif (hintType == HintType.DIVIDED_BY_5.value):
            if ((self.generatedNumber / 5).is_integer()):
                self.dividedBy5 = True
                return "Hint: The number can be divided by 5"
            else:
                self.dividedBy5 = False
                return "Hint: The number can not be divided by 5"
        else:
            return "Invalid hint type"