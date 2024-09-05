"""
Made By Ryan Kennedy and Chris Cruz
Date: Aug 31, 2024
Period: 6
Class: Embedded Programming

This is the GUI for the small binary board project.
NOTE: if you want to make this work on the binary board then you need to uncomment the comments that start with "FIXME: Pi dependent code".
"""

from time import sleep
from threading import Thread, Lock
import tkinter as tk
from PIL import Image, ImageTk
import tkinter.font as tkfont
from LbBinaryNumber import LbBinaryNumber # this is a wrapper around a binary number


# FIXME: Pi dependent code
#from BinaryBoardGPIO_modified import BinaryBoard # this is the class that allows you to interact with the lights

"""
Modes are represented by their tkinter frames

if you want to add a mode:
    1. add an id for it to the comment below
    2. create a frame for it
    3. add correct functionality to unpack_current_frame()
    4. add a method called [MODE_NAME]_mode()
    5. inside of the newly created method make it call unpack_current_frame() 
    6. inside of the newly created method make it change self.current_mode to its mode id
    7. inside of the newly created method make it pack it's frame
    8. (optional) if you want to be able to access it from the mode select screen then add
       it to the select_mode method and the select mode's ListBox.

if you want to switch modes inside the code call [MODE_NAME]_mode() and it should switch
if you want to display text back to the user then use self.output_text_label
to display a number on the binary board use self.display_number_on_binary_board(num: int, error_led: bool)
self.binary_board is the class that you should use to interact with the lights **this is for special purposes**

MODE IDs:
-2 = no mode
-1 = select mode
 0 = display number mode
 1 = display ascii mode
 2 = byte loop mode
 3 = add mode
 4 = subtract mode
 5 = two's complement mode (twoscomp)
"""

# Class that handles GUI and all of it's associated functionality
class GUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("900x600")
        self.root.title("Binary Board")
        self.root.configure(bg="#1e1e1e")
       

        ico = Image.open("resources/bulb.ico")
        self.root.wm_iconphoto(False, ImageTk.PhotoImage(ico))
        self.one = ImageTk.PhotoImage(file = "resources/1.png")# use ur own path
        self.zero = ImageTk.PhotoImage(file = "resources/0.png")# use ur own path
        self.error = ImageTk.PhotoImage(file = "resources/error.png")# use ur own path

        # Main colors for UI
        self.background = "#1e1e1e"
        self.foreground = "white"
        self.green_color = "#00bf63"

        # FIXME: Pi Dependent Code
        #self.binary_board = BinaryBoard()

        # The id of the active mode
        self.current_mode = -2

        self.titleImage = Image.open("resources/binaryBoard.png")# use ur own path
        self.title = ImageTk.PhotoImage(self.titleImage)
        self.title_label = tk.Label(self.root, image=self.title, bg= self.background)
        self.title_label.pack()
        
        # A label that will be used to output messages to the user
        self.output_text_label = tk.Label(self.root, text="", bg=self.background, fg=self.green_color, font=("bold"))
        self.output_text_label.pack()

        # Costum fonts for the UI
        self.heading_font = tk.font.Font(family = "OCR A Extended", size = 18, weight = "bold")
        self.sub_font = tk.font.Font(family = "OCR A Extended", size = 15)
        self.button_font = tk.font.Font(family = "OCR A Extended", size = 12, weight = "bold")

        # Visual representation of the binary board (on screen)
        # Creating and packing the labels in reverse order (to match binary board)
        self.bit128 = tk.Label(self.root, bd = 0, image= self.zero) 
        self.bit64 = tk.Label(self.root, bd = 0, image= self.zero)
        self.bit32 = tk.Label(self.root, bd = 0, image= self.zero)
        self.bit16 = tk.Label(self.root, bd = 0, image= self.zero)
        self.bit8 = tk.Label(self.root, bd = 0, image= self.zero)
        self.bit4 = tk.Label(self.root, bd = 0, image= self.zero)
        self.bit2 = tk.Label(self.root, bd = 0, image= self.zero)
        self.bit1 = tk.Label(self.root, bd = 0, image= self.zero) 
        self.bit128.pack(side=tk.RIGHT, padx = (1, 30)) # padding to the left of the board
        self.bit64.pack(side=tk.RIGHT, padx = 1)
        self.bit32.pack(side=tk.RIGHT, padx = 1)
        self.bit16.pack(side=tk.RIGHT, padx = 1)
        self.bit8.pack(side=tk.RIGHT, padx = 1)
        self.bit4.pack(side=tk.RIGHT, padx = 1)
        self.bit2.pack(side=tk.RIGHT, padx = 1)
        self.bit1.pack(side=tk.RIGHT, padx = (30, 1)) # padding to the right of the board

        # ==== Mode Select ====
        self.mode_select_frame = tk.Frame(self.root, bg = self.background, width=40) # frame

        self.select_label = tk.Label(self.mode_select_frame, bd = 0, text="Select The Mode", font = self.heading_font, bg = self.background, fg = self.green_color) # title label
        self.mode_list_box = tk.Listbox(self.mode_select_frame, bg = self.background, bd = 0, fg = self.foreground, font = self.sub_font) # mode options that you can choose from
        

        # self.mode_list_box.insert([MODE_ID], [MODE_NAME])
        self.mode_list_box.insert(0, "Display Number")
        self.mode_list_box.insert(1, "Display Ascii")
        self.mode_list_box.insert(2, "Byte Loop")
        self.mode_list_box.insert(3, "Add")
        self.mode_list_box.insert(4, "Subtract")
        self.mode_list_box.insert(5, "Two's Complement")

        self.mode_select_button = tk.Button(self.mode_select_frame, text="Select", command=lambda: self.select_mode(), font = self.button_font, bg = self.green_color, fg = "black" , width = 15)
        
        self.select_label.pack()
        self.mode_list_box.pack()
        self.mode_select_button.pack()

        # ==== Display Number ====
        self.display_number_frame = tk.Frame(self.root, bg = self.background) # frame
        
        # UI
        self.display_number_label = tk.Label(self.display_number_frame, text="Display Number", font= self.heading_font, bg = self.background, fg = self.green_color) # title label
        self.display_number_text_box = tk.Text(self.display_number_frame, height=1, width=10, bg = self.foreground, font = 12) # text box for entering number (maybe make this Entry instead of Text)
        self.display_number_select_button = tk.Button(self.display_number_frame, text="Display", font = self.button_font, command=self.display_number , bg = self.green_color, fg = "black") # button for submitting number
        

        self.display_number_label.pack()
        self.display_number_text_box.pack()
        self.display_number_select_button.pack()
        

        # ==== Display Ascii ====
        self.display_ascii_frame = tk.Frame(self.root, bg = self.background) # frame
        
        # UI
        self.display_ascii_label = tk.Label(self.display_ascii_frame, text="Display Ascii", font= self.heading_font, bg = self.background, fg = self.green_color) # title label
        self.display_ascii_text_box = tk.Text(self.display_ascii_frame, bg = self.foreground, font = 12, height = 1, width =10) # entry for entering character
        self.display_ascii_select_button = tk.Button(self.display_ascii_frame, text="Display", command=self.display_ascii, font = self.button_font, bg = self.green_color, fg= "black") # button for submitting character

        self.display_ascii_label.pack()
        self.display_ascii_text_box.pack()
        self.display_ascii_select_button.pack()

        # ==== Byte Loop ====
        self.byte_loop_frame = tk.Frame(self.root, bg = self.background) # frame

        # flag for if the byte loop animation is still running and a lock for multithread support
        self.byte_loop_running_lock = Lock()
        self.byte_loop_running = False

        # UI
        self.byte_loop_label = tk.Label(self.byte_loop_frame, text="Byte Loop", font= self.heading_font, bg = self.background, fg = self.green_color) # title label
        self.byte_loop_output_stringvar = tk.StringVar(self.byte_loop_frame) # stringvar that contains the content of the display label
        self.byte_loop_output_label = tk.Label(self.byte_loop_frame, textvariable=self.byte_loop_output_stringvar,font = self.sub_font, bg = self.background, fg = "white") # label that displays the output
        self.byte_loop_exit_button = tk.Button(self.byte_loop_frame, text="Exit", command=self.exit_byte_loop, font = self.button_font, bg = self.green_color, fg= "black") # button for exiting/stopping the animation

        self.byte_loop_label.pack()
        self.byte_loop_output_label.pack()
        self.byte_loop_exit_button.pack()

        # ==== Add ====
        self.add_frame = tk.Frame(self.root, bg = self.background) # frame

        # Stores the numbers that are inputted
        self.add_first_number = 0
        self.add_second_number = 0

        # UI
        self.add_label = tk.Label(self.add_frame, text="Add", font= self.heading_font, bg = self.background, fg = self.green_color) # title label
        self.add_entry_contents = tk.StringVar(self.add_frame, "") # stringvar that contains the contents of the entry
        self.add_entry = tk.Entry(self.add_frame, textvariable=self.add_entry_contents, font = 12) # entry for inputting numbers
        self.add_button = tk.Button(self.add_frame, text="Submit First Number", command=self.add_submit_first_number, font = self.button_font, bg = self.green_color, fg= "black") # button that serves multiple purposes

        self.add_label.pack()
        self.add_entry.pack()
        self.add_button.pack()

        # ==== Subtract ====
        self.subtract_frame = tk.Frame(self.root, bg = self.background) # frame

        # Stores the numbers that are inputted
        self.subtract_first_number = 0
        self.subtract_second_number = 0

        # UI
        self.subtract_label = tk.Label(self.subtract_frame, text="Subtract", font= self.heading_font, bg = self.background, fg = self.green_color) # title label
        self.subtract_entry_contents = tk.StringVar(self.subtract_frame, "") # stringvar that contains the contents of the entry
        self.subtract_entry = tk.Entry(self.subtract_frame, textvariable=self.subtract_entry_contents, font = 12) # entry for inputting numbers
        self.subtract_button = tk.Button(self.subtract_frame, text="Submit First Number", command=self.subtract_submit_first_number, font = self.button_font, bg = self.green_color, fg= "black") # button that serves multiple purposes

        self.subtract_label.pack()
        self.subtract_entry.pack()
        self.subtract_button.pack()

        # Twos Complement
        self.twoscomp_frame = tk.Frame(self.root, bg = self.background) # frame

        # UI
        self.twoscomp_label = tk.Label(self.twoscomp_frame, text="Two's Complement", font= self.heading_font, bg = self.background, fg = self.green_color) # title label
        self.twoscomp_entry_contents = tk.StringVar(self.twoscomp_frame, "") # stringvar that contains the contents of the entry
        self.twoscomp_entry = tk.Entry(self.twoscomp_frame, textvariable=self.twoscomp_entry_contents, font = 12) # entry for inputting a number
        self.twoscomp_button = tk.Button(self.twoscomp_frame, text="Display Two's Complement", command=self.twoscomp_show, font = self.button_font, bg = self.green_color, fg= "black") # button for displaying the two's complement

        self.twoscomp_label.pack()
        self.twoscomp_entry.pack()
        self.twoscomp_button.pack()

        # ==== Starting ====
        self.select_mode_mode()

        self.root.mainloop()

    def display_number_on_binary_board_and_gui(self, num, error_bool):
        self.display_number_on_binary_board(num, error_bool)
        self.display_number_on_gui(num, error_bool)

    # displays the inputted number on the binary board
    def display_number_on_binary_board(self, num, error_bool):
        # FIXME: Pi dependent code
        # self.binary_board.setErrorLED(error_bool)
        # for i in range(1, 8):
        #     self.binary_board.setMainLED(2 ** i, number.bits[i])
        pass

    def display_number_on_gui(self, num, error_bool):
        number = LbBinaryNumber(num)

        # sets the board to all zeros if the number is zero
        if num == 0:
            self.bit1.config(image=self.zero)
            self.bit2.config(image=self.zero)
            self.bit4.config(image=self.zero)
            self.bit8.config(image=self.zero)
            self.bit16.config(image=self.zero)
            self.bit32.config(image=self.zero)
            self.bit64.config(image=self.zero)
            self.bit128.config(image=self.zero)

        # sets the board to the number if it is within range of binary
        elif num > 0 and num < 256:

            # lists of all of the labels
            self.board = [self.bit1, self.bit2, self.bit4, self.bit8, self.bit16, self.bit32, self.bit64, self.bit128] 

            # gets text comprised of 1's and 0's to display on the GUI binary board
            binary_text = number.get_loaded_number_binary()

            # goes through each digit and sets the image of the label to the corresponding image
            for i in range(0, 8):
                if binary_text[i] == "1":
                    self.board[i].config(image=self.one)
                else:
                    self.board[i].config(image=self.zero)

        # sets the board to all red if the number is out of range / On physical board, the error LED will light up, not all LEDs
        if error_bool:
            self.output_text_label.config(text="Number out of range.", fg="red")
            for i in range(0, 8):
                self.board[i].config(image=self.error)



    # calls pack_forget() on the frame associated with the current mode (self.current_mode)
    def unpack_current_frame(self):
        if (self.current_mode == -2):
            pass
        elif (self.current_mode == -1):
            self.mode_select_frame.pack_forget()
        elif (self.current_mode == 0):
            self.display_number_frame.pack_forget()
        elif (self.current_mode == 1):
            self.display_ascii_frame.pack_forget()
        elif (self.current_mode == 2):
            self.byte_loop_frame.pack_forget()
        elif (self.current_mode == 3):
            self.add_frame.pack_forget()
        elif (self.current_mode == 4):
            self.subtract_frame.pack_forget()
        elif (self.current_mode == 5):
            self.twoscomp_frame.pack_forget()

    # ==== Select Mode Mode ====

    # starts select mode
    def select_mode_mode(self):
        self.unpack_current_frame()

        self.current_mode = -1
        self.mode_select_frame.pack(expand=True, padx = 30)
        self.mode_list_box.selection_clear(0, tk.END)
        


    # switches modes based on the selected element in the ListBox
    def select_mode(self):

        # gets selected mode
        mode = 0
        try:
            mode = int(self.mode_list_box.curselection()[0])
        except:
            self.output_text_label.config(text="You don't have a mode selected.", fg="red")
            return

        # calls the associated mode's method to switch modes
        if (mode == 0):
            self.display_number_mode()
        elif (mode == 1):
            self.display_ascii_mode()
        elif (mode == 2):
            self.byte_loop_mode()
        elif (mode == 3):
            self.add_mode()
        elif (mode == 4):
            self.subtract_mode()
        elif (mode == 5):
            self.twoscomp_mode()

    # ==== Display Number Mode ====

    # starts display number mode
    def display_number_mode(self):
        self.unpack_current_frame()
        self.current_mode = 0
        self.display_number_frame.pack(expand=True, padx = 30)
    

    # displays the inputted number on the binary board
    def display_number(self):
        
        # gets the number to display with error checking
        num = 0
        try:
            num = int(self.display_number_text_box.get("1.0", "end-1c"))
        except:
            self.output_text_label.config(text="Please enter a valid number.", fg="red")
            return

        # clears the text box
        self.display_number_text_box.delete("1.0", "end")

        # Display on lightboard
        error_led = (num < 0 or num > 255)
        self.display_number_on_binary_board_and_gui(num, error_led)

        # output success information to the user
        self.output_text_label.config(text="Displayed Number", fg="green")

        self.select_mode_mode()

    # ==== Display Ascii Mode ====

    # starts display ascii mode
    def display_ascii_mode(self):
        self.unpack_current_frame()
        self.current_mode = 1
        self.display_ascii_frame.pack(expand=True, padx = 30)
    
    # displays the inputted ascii character on the binary board
    def display_ascii(self):

        # gets the inputted character with error checking
        char = 'a'
        try:
            text = ""
            text = self.display_ascii_text_box.get("1.0", "end-1c")
            char = text[0]
        except:
            self.output_text_label.config(text="Please enter in a character.", fg="red")            
            return

        # clears the text box
        self.display_ascii_text_box.delete("1.0", "end")

        # Display on lightboard
        num = ord(char)
        error_led = (num < 0 or num > 255)
        self.display_number_on_binary_board_and_gui(num, error_led)

        # outputs success information
        self.output_text_label.config(text="Displayed Ascii Number", fg="green")

        self.select_mode_mode()

    # ==== Byte Loop Mode ====

    # starts byte loop mode
    def byte_loop_mode(self):
        self.unpack_current_frame()
        self.current_mode = 2
        self.byte_loop_frame.pack(expand=True, padx = 30)

        self.start_byte_loop()


    # starts the byte loop animation in a seperate thread
    def start_byte_loop(self):
        self.byte_loop_running_lock.acquire()
        self.byte_loop_running = True
        self.byte_loop_running_lock.release()

        self.byte_loop_thread = Thread(target=self.do_byte_loop, daemon=True)
        self.byte_loop_thread.start()

    # does the byte loop animation, meant to be started with start_byte_loop()
    def do_byte_loop(self):
        displayed_number = 0

        while (displayed_number < 256):

            self.byte_loop_running_lock.acquire()
            if (self.byte_loop_running is False):
                self.byte_loop_running_lock.release()
                break

            self.byte_loop_running_lock.release()

            # display number on binary board and output on GUI
            bin_num = LbBinaryNumber(displayed_number)
            self.byte_loop_output_stringvar.set(bin_num.get_loaded_number_binary() + " - " + str(displayed_number))
            self.display_number_on_binary_board_and_gui(displayed_number, False)

            sleep(0.4)
            displayed_number += 1

    # stops the byte loop animation and exits back to the select mode
    def exit_byte_loop(self):
        if (self.byte_loop_thread.is_alive() is True):
            self.byte_loop_running_lock.acquire()
            self.byte_loop_running = False
            self.byte_loop_running_lock.release()
            self.byte_loop_thread.join()

        self.select_mode_mode()

    # ==== Add Mode ====

    # starts the add mode
    def add_mode(self):
        self.unpack_current_frame()
        self.current_mode = 3
        self.add_frame.pack(expand=True, padx = 30)
        self.add_entry.config(state='normal')


    # submits the input in the entry as the first number
    def add_submit_first_number(self):
        
        # gets inputted number from entry with error checking
        num = 0
        try:
            num = int(self.add_entry_contents.get())
        except:
            self.output_text_label.config(text="Please enter a valid number.", fg="red")
            return

        self.add_entry_contents.set("") # clears entry

        self.add_first_number = num # loads number

        # displays first number on the binary board
        error_led = (self.add_first_number < 0 or self.add_first_number > 255)
        self.display_number_on_binary_board_and_gui(self.add_first_number, error_led)

        # output success information
        self.output_text_label.config(text="Submitted and displayed first number.", fg="green")

        # changes the behavior of the button for submitting the second number
        self.add_button.config(text="Submit Second Number", command=self.add_submit_second_number)

    # submits the input in the entry as the second number
    def add_submit_second_number(self):

        # gets inputted number from entry with error checking
        num = 0
        try:
            num = int(self.add_entry_contents.get())
        except:
            self.output_text_label.config(text="Please enter a valid number.", fg="red")
            return

        self.add_entry_contents.set("") # clears entry

        self.add_second_number = num # loads number

        # displays first number on the binary board
        error_led = (self.add_second_number < 0 or self.add_second_number > 255)
        self.display_number_on_binary_board_and_gui(self.add_second_number, error_led)

        # output success information
        self.output_text_label.config(text="Submitted and displayed second number.", fg="green")

        # changes functionalitiy of the button and the entry for showing the sum
        self.add_button.config(text="Display Sum", command=self.add_display_sum)
        self.add_entry.config(state='disabled') # disables entry

    # displays the summed number and exits add mode
    def add_display_sum(self):
        # sums the numbers
        num = self.add_first_number + self.add_second_number

        # displays the sum on the binary board
        error_led = (num < 0 or num > 255)
        self.display_number_on_binary_board_and_gui(num, error_led)

        # output success information
        self.output_text_label.config(text="Submitted and displayed sum.", fg="green")

        # change functionality of the button for submitting the first number
        self.add_button.config(text="Submit First Number", command=self.add_submit_first_number)

        # goes back to select mode
        self.select_mode_mode()

    # ==== Subtract Mode ====

    # starts subtract mode
    def subtract_mode(self):
        self.unpack_current_frame()
        self.current_mode = 4
        self.subtract_frame.pack(expand=True, padx = 30)
        self.subtract_entry.config(state='normal')


    # gets the inputted number from the entry and submits it as the first number
    def subtract_submit_first_number(self):

        # gets inputted number from entry with error checking
        num = 0
        try:
            num = int(self.subtract_entry_contents.get())
        except:
            self.output_text_label.config(text="Please enter a valid number.", fg="red")
            return

        self.subtract_entry_contents.set("") # clears the entry
        self.subtract_first_number = num # loads the inputted number to first number

        # displays first number on binary board
        error_led = (self.subtract_first_number < 0 or self.subtract_first_number > 255)
        self.display_number_on_binary_board_and_gui(self.subtract_first_number, error_led)

        # output success information
        self.output_text_label.config(text="Submitted and displayed first number.", fg="green")

        # changes the functionality of the button for submitting the second number
        self.subtract_button.config(text="Submit Second Number", command=self.subtract_submit_second_number)

    # gets the inputted number from the entry and submits it as the second number
    def subtract_submit_second_number(self):

        # gets inputted number from entry with error checking
        num = 0
        try:
            num = int(self.subtract_entry_contents.get())
        except:
            self.output_text_label.config(text="Please enter a valid number.", fg="red")
            return

        self.subtract_entry_contents.set("") # clears the entry
        self.subtract_second_number = num # loads the number into second number

        # displays first number on binary board
        error_led = (self.subtract_second_number < 0 or self.subtract_second_number > 255)
        self.display_number_on_binary_board_and_gui(self.subtract_second_number, error_led)

        # output success information
        self.output_text_label.config(text="Submitted and displayed second number.", fg="green")

        # changes functionality of the button and entry for displaying the two's complement of the second number
        self.subtract_button.config(text="Display Two's Complement of Second Number", command=self.subtract_display_twos_complement)
        self.subtract_entry.config(state='disabled')

    # displays the two's complement of the second number
    def subtract_display_twos_complement(self):

        # get the twos complement of the second number
        num = LbBinaryNumber(self.subtract_second_number)
        num.twos_complement()

        # display two's complement on binary board
        self.display_number_on_binary_board_and_gui(num.number, False)

        # output success information
        self.output_text_label.config(text="Displayed two's complement.", fg="green")

        # change the functionality of the button for displaying the result of the subtraction
        self.subtract_button.config(text="Display Result", command = self.subtract_display_result)
        

    # display the result of the subtraction
    def subtract_display_result(self):
        
        # find the result of the subtraction
        num = self.subtract_first_number - self.subtract_second_number

        # display result on binary board
        error_led = (num < 0 or num > 255)
        self.display_number_on_binary_board_and_gui(num, error_led)

        # output success information
        self.output_text_label.config(text="Submitted and displayed result.", fg="green")

        # change functionality of the button for submitting the first number
        self.subtract_button.config(text="Submit First Number", command=self.subtract_submit_first_number)

        # exits subract mode and goes to select mode mode
        self.select_mode_mode()

    # ==== Two's Complement Mode

    # starts two's complement mode
    def twoscomp_mode(self):
        self.unpack_current_frame()
        self.current_mode = 5
        self.twoscomp_frame.pack(expand=True, padx = 30)

    # displays the two's complement of the inputted number
    def twoscomp_show(self):

        # gets inputted number from entry with error checking
        num = 0
        try:
            num = int(self.twoscomp_entry_contents.get())
        except:
            self.output_text_label.config(text="Please enter a valid number.", fg="red")
            return

        self.twoscomp_entry_contents.set("") # clears the entry

        # gets the two's complement
        bin_num = LbBinaryNumber(num)
        bin_num.twos_complement()

        # display two's complement on the binary board
        self.display_number_on_binary_board_and_gui(bin_num.number, False)

        # output success information
        self.output_text_label.config(text="Displayed two's complement.", fg="green")

        # exits two's complement mode and goes to select mode mode
        self.select_mode_mode()
