__author__ = 'Grace Rarer'


"""
THIS IS A MODIFIED VERSION WITH ALTERNATE GPIO NUMBERING USED IN THE PROTOTYPE
"""


# GPIO Library
import RPi.GPIO as GPIO

class BinaryBoard:
    """Instantiate this object to manage the binary board LED outputs on raspberry pi zero.

    This should also be compatible with raspberry pi models A+,B+,2, and 3."""

    def __init__(self):
        # Main LEDs pins in dictionary
        # This uses BOARD numbering, not BCM numbering (e.g. BOARD pin 11 is BCM GPIO # 
        #self.mainPins = {1: 3, 2: 5, 4: 7, 8: 11, 16: 13, 32: 15, 64: 19, 128: 21} # this was the original numbering
        self.mainPins = {1: 21, 2: 3, 4: 5, 8: 15, 16: 11, 32: 13, 64: 19, 128: 23}
        # Red LEDs pins in dictionary
        self.redPins = {1: 8, 2: 10, 4: 12, 8: 16, 16: 18, 32: 22, 64: 24, 128: 26}
        # Error light LED
        self.error_pin = 32

        # set board numbering system
        GPIO.setmode(GPIO.BOARD)

        # setup pins as outputs
        for key, value in self.mainPins.items():
            GPIO.setup(value, GPIO.OUT)
            GPIO.output(value, False)
        for key, value in self.redPins.items():
            GPIO.setup(value, GPIO.OUT)
            GPIO.output(value, False)
        GPIO.setup(self.error_pin, GPIO.OUT)
        GPIO.output(self.error_pin, False)
        

    def setMainLED(self, int_number, bool_state):
        """
        Sets the Main-color LED of a given number to ON or OFF
        """
        # checks whether number is a binary base
        if int_number in [1,2,4,8,16,32,64,128]:

            if bool_state:
                GPIO.output(self.mainPins[int_number], GPIO.HIGH)
                pass
            else:
                GPIO.output(self.mainPins[int_number], GPIO.LOW)
                pass
        else:
            print("int_number must be 2^N and between 1 and 128 inclusive")


    def setRedLED(self, int_number, bool_state):
        """
        Sets the red-color LED of a given number to ON or OFF
        """
        # checks whether number is a binary base
        if int_number in [1,2,4,8,16,32,64,128]:

            if bool_state:
                GPIO.output(self.redPins[int_number], GPIO.HIGH)
                pass
            else:
                GPIO.output(self.redPins[int_number], GPIO.LOW)
                pass
        else:
            print("int_number must be 2^N and between 1 and 128 inclusive")

    def setErrorLED(self, bool_state):
        if bool_state:
            GPIO.output(self.error_pin, GPIO.HIGH)
            pass
        else:
            GPIO.output(self.error_pin, GPIO.LOW)
            pass

    def reconfigurePins(self, new_main_color_dictionary, new_red_color_dictionary, new_error_pin):
        """ DO NOT USE THIS UNLESS YOU UNDERSTAND WHAT YOU ARE DOING, AND KNOW HOW THE RASPBERRY PI GPIO works.
        Changes pin numbers from their default values if hardware has been rearranged.
        Use numbering of BOARD mode, not BCM mode."""
        self.mainPins = new_main_color_dictionary
        self.redPins = new_red_color_dictionary
        self.error_pin = new_error_pin;




