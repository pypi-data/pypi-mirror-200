
"""A calculator module."""

# versioning
__version__ = "0.1.0"

import math

class Calculator:

    def __init__(self, accum=math.inf):
        """default state of the accumulator is +infinity
        """
        self.__accum = accum

    def add(self, num: int):
        """add num to accumulator,
           if accumulator in default state then use num as starting value.

           For example:
               >>> cal = Calculator()
               >>> cal.add(2)
               >>> print(cal.accum_state)
               2
               >>> cal.add(2)
               >>> print(cal.accum_state)
               4
        """
        if self.is_accum_inf():
            self.__accum = num
        else:
            self.__accum += num

    def subtract(self, num: int):
        """subtract num from accumulator,
           if accumulator in defualt state then use num as starting value.

           For example:
               >>> cal = Calculator()
               >>> cal.subtract(2)
               >>> print(cal.accum_state)
               2
               >>> cal.subtract(2)
               >>> print(cal.accum_state)
               0
        """
        if self.is_accum_inf():
            self.__accum = num
        else:
            self.__accum -= num

    def multiply(self, num: int):
        """multipy accumulator by num,
           if default value in accumulator then use num as starting value.

           For example:
               >>> cal = Calculator()
               >>> cal.add(2)
               >>> print(cal.accum_state)
               2
               >>> cal.add(2)
               >>> print(cal.accum_state)
               4
        """
        if self.is_accum_inf():
            self.__accum = num
        else:
            self.__accum *= num

    def divide(self, num: int):
        """divide accumulator by num,
           if default value in accumulator then use num as starting value.

           For example:
               >>> cal = Calculator()
               >>> cal.divide(2)
               >>> print(cal.accum_state)
               2
               >>> cal.divide(2)
               >>> print(cal.accum_state)
               1.0
        """
        if self.is_accum_inf():
            self.__accum = num
        else:
            self.__accum /= num

    def root(self, num: int):
        """find root of number.
           
           For example:
               >>> cal = Calculator()
               >>> cal.root(4)
               >>> print(cal.accum_state)
               2.0
        """
        self.__accum = math.sqrt(num)

    def reset(self, state=math.inf):
        """reset accumulator to defualt value of +infinity
           
           For example:
               >>> cal = Calculator()
               >>> cal.reset(2)
               >>> print(cal.accum_state)
               2
        """
        self.__accum = state

    @property
    def accum_state(self):
        """get current state/value of accumulator
           
           For example:
               >>> cal = Calculator()
               >>> print(cal.accum_state)
               inf
        """
        return self.__accum

    def is_accum_inf(self):
        """check accumulator is set to default of +infinity
           
           For example:
               >>> cal = Calculator()
               >>> print(cal.is_accum_inf())
               True
        """
        return True if self.__accum == math.inf else False
