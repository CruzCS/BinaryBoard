"""
Made By Ryan Kennedy and Chris Cruz
Date: Aug 31, 2024
Period: 6
Class: Embedded Programming

This is a class that is used for storing a number as binary
"""


class LbBinaryNumber:
    def __init__(self, number):
        self.number = 0
        self.bits = [False, False, False, False, False, False, False, False]
        self.load_number(number)

    # @brief Use this to change the number. This loads both the self.number and self._# fields.
    # @param number This is the number that you want to store.
    def load_number(self, number):
        self.number = number
        for i in range(0, 8):
            self.bits[i] = bool(number & (1 << i))

    # @brief loads the twos complement of the current number
    def twos_complement(self):
        new_num = 0
        for i in range(0, 8):
            self.bits[i] = not self.bits[i]
            if (self.bits[i] is True):
                new_num += 1 << i
        new_num += 1
        self.load_number(new_num)

    # For Debugging
    # @brief Gets a string in binary representation of the loaded number
    # @return A string which contains a binary encoding of the loaded number
    def get_loaded_number_binary(self) -> str:
        result = ""
        for bit in self.bits[::-1]:
            if (bit is True):
                result += "1"
            else:
                result += "0"
        return result
