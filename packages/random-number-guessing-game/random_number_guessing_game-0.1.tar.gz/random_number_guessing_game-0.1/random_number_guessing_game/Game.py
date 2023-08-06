from .Number import Number
from .Hints import HintDescription, HintType
from .Utils import Options

class Game:
    ''' Class for playing a number guessing game
    
    Attributes:
        rangeMin (int) representing minimum value of the interval in which the number will be generated
		rangeMax (int) representing maximum value of the interval in which the number will be generated
        score (int) representing the score of the game
    '''
    def __init__(self, rangeMin, rangeMax):
        if not isinstance(rangeMin, int):
            raise Exception("rangeMin must be an integer")
        if not isinstance(rangeMax, int):
            raise Exception("rangeMax must be an integer")
        if rangeMin >= rangeMax:
            raise Exception("rangeMin must be lower than rangeMax")
        if rangeMax > 100:
            raise Exception("rangeMax must be lower than 100")
        self.rangeMin = rangeMin
        self.rangeMax = rangeMax
        self.score = 150

    def start(self):
        print()
        print("Starting the game...")

        number = Number(self.rangeMin, self.rangeMax)

        while True:
            print(number.hints_summary())
            print("Select an option:")
            print("1. Guess a number (-5p)")
            print("2. Get a hint (-10p)")
            print("3. Exit")
            print("Your score is {}\n".format(self.score))
            option = input(">> ")

            if option == Options.GUESS_NUMBER.value:
                data = input(">> Guess a number in [{}, {}] interval: ".format(self.rangeMin, self.rangeMax))
                self.score = self.score - 5

                if not data.isnumeric():
                    print("\"{}\" is not a number".format(data))

                if (int(data) == number.generatedNumber):
                    print(">> Congratulations, you guessed! The generated number was {}".format(data))
                    print(">> Your score is {}".format(self.score))
                    break
                else:
                    print(">> Wrong number\n")
            elif option == Options.GET_HINT.value:
                print()
                print("Select a hint type:")
                self.score = self.score - 10

                for hint in HintType:
                    print("{}. {}".format(hint.value, HintDescription[hint.name].value))
                hintType = input(">> Type the number of the hint type [1-3]: ")
                hint = number.hint(hintType)

                print()
                print(hint)
                print()
            elif option == Options.EXIT.value:
                break

        print("Done")