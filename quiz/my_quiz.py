#-------------------------HEADER--------------------------------#
# kristofszigeti
# Quiz game
#----------------------Start of the CODE----------------------------#
# imports everything from tkinter
from tkinter import *
# imports ttk themed widgets from tkinter
from tkinter import ttk
# import json module to use json file for data
import json
# import messagebox as mb for reference from tkinter
from tkinter import messagebox as mb
# import datetime and time module to output a result file
from datetime import *
import time
# import random module
import random

# import os and import sys: az összecsomagolt futtatható fájl készítéséhez szükséges modulok
import os
import sys

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        # When running as a bundled executable
        return os.path.join(sys._MEIPASS, relative_path)
    # When running in development mode
    return os.path.join(os.path.abspath("."), relative_path)

# the main class
class Quiz:
    # initial dunder method: __init__
    # initialize values, containers, class methods to display contents and create operations
    def __init__(self):

        self.q_no = 0 # initial number of questions

        # initial (empty) data storage
        self.question = []
        self.choices = []
        self.answer = []
        self.hint = []

        self.display_title() # display title label
        # self.display_question() # display question (korábbi állapot, már nem mutat semmit, mert nincs miből)

        # radiobuttons and their corresponding answer according to current question
        # self.options = self.radio_buttons() # assigns and shows radiobuttons initially # (korábbi állapot)
        self.options = None # initial None storage (de a változót létrehozni szükséges)

        # https://www.linkedin.com/learning/python-gui-development-with-tkinter-2/making-selections-with-the-combobox-and-spinbox?resume=false
        self.selected_option = IntVar() # initial (integer) value type to assign integer to check answer

        # display choices for the current question, displays the buttons # (korábbi állapot, a sorrendiséget tartani kell->indexerror)
        # self.display_options()
        # self.buttons()

        # self.data_size = 0 # (korábbi állapot)
        self.data_size = len(self.question) # number of questions from json
        # print(self.data_size)
        # print(len(self.question))
        # feedback field, showing if the answer is correct or wrong,
        self.feedback = ttk.Label(frame, font=('Franklin Gothic', 15, 'bold'), anchor='center', justify='center') # in this form it does not do anything, must be referred it later and add/customize the response with text and color
        self.feedback.place(x=350, y=330)

        self.correct = 0.0 # initial counter value of correct answers

        # https://www.linkedin.com/learning/python-gui-development-with-tkinter-2/handling-user-events?resume=false
        guitop.bind('<Return>', self.next_btn) # reference of the method, not call it https://stackoverflow.com/questions/54251768/how-do-i-keybind-functions-to-keys-in-the-keyboard-with-tkinter
        guitop.bind('<Escape>', lambda event: guitop.destroy()) # anonym callable/function to handle event, and avoid executing without the user event # https://stackoverflow.com/questions/46626441/bind-lambda-of-function-to-key-event-python

        self.current_topic = StringVar() # initial empty and blank in the main window

        self.player_name = StringVar()
        self.name_entry = ttk.Entry(frame, width=20, textvariable=self.player_name, font=('Franklin Gothic', 10)) # width controls the size of the name_entry field, and specifies the number of characters, not pixels
        self.name_entry.place(x=5, y=395)
        self.name_entry.insert(0, "Type your name")

        self.topic_bonus = None

    # method fo displaying the result, counting, storing the number of correct and wrong answers and then display them at the end in messagebox widet
    def display_result(self):

        # calculates the wrong count
        correct = f"Correct: {self.correct}"
        wrong_count = self.data_size - self.correct
        wrong = f"Missed points: {wrong_count}"

        # calculates the percentage of correct answers
        score = int(self.correct / self.data_size * 100)
        result = f"Your score: {score}%"

        # Shows a message box to display the result
        mb.showinfo("Result", f"{result}\n{correct}\n{wrong}")

        return result

    # checking if the answer after we clicked next button.
    def check_ans(self, q_no):

        # checking if the selected option is correct (else-case=not correct)
        if self.selected_option.get() == self.answer[q_no]:
            # if the option is correct it return true
            self.feedback['foreground'] = "green" # ont color to green
            # self.feedback["bg"] = "light gray"  # set the background color of this label (teszt)
            self.feedback["text"] = f'  Correct!  \u2714' # light check mark: https://www.fileformat.info/info/unicode/char/1f5f8/index.htm
            return True
        else:
            self.feedback['foreground'] = 'darkorange' # it sets the font color to red, indicating the answer is inaccurate
            # self.feedback["bg"] = "light gray"  # set the background color of this label (teszt)
            self.feedback['text'] = f'\u274C  Next time!' # cross mark https://www.fileformat.info/info/unicode/char/274c/index.htm
            return False

    #  a next gomb metódusa
    def next_btn(self, event=None): # https://stackoverflow.com/questions/54251768/how-do-i-keybind-functions-to-keys-in-the-keyboard-with-tkinter

        # increasing points
        if self.check_ans(self.q_no) == True:
            # if the answer is correct (True) it increments the value of variable correct by 1
            self.correct += 1.0

        # update progress bar and its label
        progress_value = (self.correct / self.data_size) * 100
        progressbar['value'] = progress_value
        progress_counter.set(f"Correct: {self.correct}/{self.data_size}")

        self.q_no += 1 # go further to next question by incrementing the q_no counter

        # checks if the q_no size is equal to the data size
        if self.q_no == self.data_size: # if the counter has reached the total number of questions (for this round!): steps-in

            # if it is correct then it displays the score
            # self.display_result()

            with open("result.txt", "a", encoding="UTF-8") as outfile:
                player_name = self.player_name.get() # storing the name_entry field in variable
                line_newscore= f"{date.today()}, {time.strftime('%H:%M:%S')}\n{self.current_topic:20s}\nPlayer name: {player_name:15s}\n{quiz.display_result()}\n" + f"{'-'*(13+self.name_entry['width'])}\n" # https://www.geeksforgeeks.org/get-current-date-and-time-using-python/
                outfile.write(line_newscore)
            # print(self.name_entry['width'])

            if self.correct == self.data_size and topics.entrycget(5, 'state') == 'disabled':
                mb.showinfo("BONUS", "Congratulations!\n\nYou have earned a bonus topic!!\n\nCheck the 'Topics' cascade menu!")
                # unlocking bonus
                topics.entryconfig(5, state='active', label="Topic BONUS - Board Games", image= logo_t06)

            if self.correct == self.data_size and topics.entrycget(6, 'label') == 'T, T-É és SZÉS1':
                mb.showinfo("BONUS", "Szép volt főni! Ezt kimaxoltad.")

            elif self.correct == self.data_size and topics.entrycget(5, 'state') == 'active':
                mb.showinfo("Apologize", "Sorry, but I do not have more bonuses for you.")

            mb.showinfo("Help", "You are at the end of the guiz. \n\nNow you can hit 'OK' and select a new topic from 'Topics' menu to play again!\n\nGood luck!\n")
            self.name_entry.state(['!disabled'])

        else:
            # going further
            self.display_question()
            self.display_options()

    # hint option for the player
    def hint_btn(self):

        self.correct -= 0.5 # each time pushing the hint button earns -0.5 points
        # Shows a message box to display the result
        mb.showinfo("Result", f"You asked me for a hint.\n\nHere it is:\n\n{self.hint[self.q_no]}") # fetching info accordingly

    # X open results
    # def open_rankings(self):
    #     with open("result.txt", "r") as ranking:
    #         exec(ranking.read()) # az exec function nem fog működni és nem is ajánlott

    # showing buttons in quitop/frame
    # https://www.geeksforgeeks.org/python-creating-a-button-in-tkinter/
    def buttons(self):
        # color ref.: https://stackoverflow.com/questions/22408237/named-colors-in-matplotlib
        # next_button itself for checking the answer and moving to the next question
        next_button = Button(frame, text="Next",
                             command=self.next_btn, # call the next_btn method of the Quiz class
                             width=10, bg='lightblue', fg='black', font=('Franklin Gothic', 16, 'bold'),
                             activebackground='dark blue', activeforeground='white')
        # placing next
        next_button.place(x=350, y=380)


        # hint_button itself to show a hint to the user
        hint_button = Button(frame, text="Hint",
                             command=self.hint_btn, # call the hint_btn method of the Quiz class
                             width=10, bg="seashell", fg="black", font=('Franklin Gothic', 12, 'bold'),
                             activebackground='gold', activeforeground='black')
        # placing hint
        hint_button.place(x=680, y=330)


        # quit_button to close the game and the window
        quit_button = Button(frame, text="Quit",
                             command=guitop.destroy, # destroy is built-in therefore belongs to the parent=guitop
                             width=10, bg="light grey", fg="black", font=('Franklin Gothic', 12, 'bold'),
                             activebackground='maroon', activeforeground='white')
        # placing quit
        quit_button.place(x=680, y=380) # it is the bottom-right corner

    def display_options(self):
        val = 0 # starting value

        # deselecting the choices
        self.selected_option.set(0) # avoiding selecting the first

        # looping over the choices to be displayed for the text parameter of the radio buttons.
        for option in self.choices[self.q_no]:
            self.options[val]['text'] = option
            val += 1 # it must be increased to go through the choices and show them

    # this method shows the current question on the screen
    def display_question(self):

        # showing questions inside a Label widget
        # https://www.geeksforgeeks.org/python-tkinter-label/?ref=lbp
        if self.q_no < len(self.question):
            q_no = Label(frame, text=self.question[self.q_no], wraplength= 700, # index
                         font=('Franklin Gothic', 16, 'bold'), anchor='center', # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/img/labelanchor.png
                         justify='center',
                         width=55, height=3)

            # placing of the option in the frame
            q_no.place(x=40, y=80)

    # this method shows a title label in the parent window
    def display_title(self):
        # title of the game
        title = Label(frame, text="Quiz Game",
                             padx=75, width=40, bg='light sky blue', fg="white", font=('Franklin Gothic', 20, "bold"), justify='center') # color ref.: https://i.sstatic.net/lFZum.png
        # placing of the title
        title.place(x=0, y=0)

    # because of the radio buttons, to select the answers from "choices"
    # returns a list of radio button which are later used to add the choices to them.
    def radio_buttons(self):

        # initialize the list with an empty list of choices
        q_list = []
        # print(len(q_list))
        # position of the first option
        y_pos = 160

        # adding the choices to the list # lab_11_hotel.py
        while len(q_list) < 4:
            # setting the radio button properties
            radio_btn = Radiobutton(frame, text="", variable=self.selected_option, value=len(q_list) + 1,
                                    font=('Franklin Gothic', 14),
                                    width= 60, anchor='w',justify="left")
            # print(len(q_list))
            q_list.append(radio_btn) # adding the button to the end of the list one by one

            radio_btn.place(x=100, y=y_pos) # placing the button
            y_pos += 40  # increasing the y-axis position by +40 (downwards)

        # return the lsit of radio buttons
        return q_list # important!

    def call_topic(self, topic_datafile, index, topic_length=10):
        # load topics # https://pynative.com/python-json-exercise/#h-exercise-8-check-whether-following-json-is-valid-or-invalid-if-invalid-correct-it
        with open(topic_datafile, 'r', encoding='utf-8') as datafile:
            data_dict = json.load(datafile)

        # combine data into a list https://www.w3schools.com/python/ref_func_zip.asp
        data_list = list(zip(data_dict['question'], data_dict['choices'], data_dict['answer'], data_dict['hints'])) # https://discovery.cs.illinois.edu/guides/Python-Fundamentals/brackets/ # https://www.geeksforgeeks.org/parentheses-square-brackets-and-curly-braces-in-python/
        # random.shuffle(data_list) # https://www.geeksforgeeks.org/python-random-sample-function/
        data_sample_list = random.sample(data_list, k=topic_length)

        # unpack the shuffled data back into separate lists
        # global question, choices, answer, hint
        # https://geekflare.com/dev/python-unpacking-operators/
        self.question, self.choices, self.answer, self.hint = zip(*data_sample_list) # https://www.w3schools.com/python/ref_func_zip.asp # https://stackoverflow.com/questions/50950690/python-unpacking-operator

        # restore the initial status, it must happen if we have already played one
        self.q_no = 0
        self.correct = 0.0
        # must reload tha data
        self.data_size = len(self.question)
        # print(self.data_size)
        self.options = self.radio_buttons() # after this we get the radiobuttons
        self.display_question() # after this we have the question
        self.display_options() # after this the options
        self.buttons() # after this we have buttons
        # self.selected_option.set(0) # clear the selection

        # restore progress bar and label
        progressbar['value'] = 0
        progress_counter.set(f"Correct: 0/{len(self.question)}")

        self.feedback['text'] = ""  # restore feedback label to 'blank' status
        self.current_topic = topics.entrycget(index, 'label') # declares/fills the label content
        self.name_entry.state(['disabled'])

    def display_topic_label(self, index):
        # referring to parameters
        topic_label = topics.entrycget(index, 'label')
        topic_logo = topics.entrycget(index, 'image')

        # label widget
        topic = Label(frame, text=f"{topic_label}", image=topic_logo, compound='left',
                      width=650, bg='sky blue', fg="black", font=("Franklin Gothic", 16, "bold"), justify='center')
        topic.place(x=90, y=40) # placing the label

# Tkinter GUI:

# create a top-level parent GUI Window
guitop = Tk() # parent

# dimensions of the GUI Window
guitop_width = 800
guitop_height = 480

# put the window to the center # https://www.youtube.com/watch?v=Z8jdlBNIaDo
# queries the Win screensize setting and store them in a variable
screen_width = guitop.winfo_screenwidth()
screen_height = guitop.winfo_screenheight()
# print(screen_width, screen_height)
# positions the parent window
guitop.geometry(f"{guitop_width}x{guitop_height}+{(screen_width // 2)-(guitop_width // 2)}+{(screen_height // 2)-(guitop_height // 2)}") #("800x480")
guitop.configure(bg='dark gray')
# print((screen_width // 2)-(guitop_width // 2), (screen_height // 2)-(guitop_height // 2))

# set the title of the Window
guitop.title("Quiz Game")
frame = ttk.Frame(guitop)
frame.pack(fill= NONE, expand= True) # https://www.geeksforgeeks.org/difference-between-fill-and-expand-options-for-tkinter-pack-method/
frame.config(height = guitop_height, width = guitop_width)
frame.config(relief = 'sunken')

# set the menubar
guitop.option_add('*tearOff', False) # https://www.geeksforgeeks.org/what-does-the-tearoff-attribute-do-in-a-tkinter-menu/
menubar = Menu(guitop) # https://www.linkedin.com/learning/python-gui-development-with-tkinter-2/building-cascading-menus?resume=false
guitop.config(menu = menubar)
topics = Menu(menubar)
# results = Menu(menubar)
# help_ = Menu(menubar) # underscore is for avoiding shadowing https://www.linjiangxiong.com/2024/08/28/how-to-fix-shadows-name-from-outer-scope-warning-in-pycharm/index.html

menubar.add_cascade(menu = topics, label ='Topics')
# menubar.add_cascade(menu = results, label ='Results', state='disabled')
# menubar.add_cascade(menu = help_, label = 'Help', state='disabled')

# results.add_command(label ='Ranking', state='disabled', command = lambda: quiz.open_rankings())

# icons to show for the topics
logo_t01 = PhotoImage(file = resource_path('./logo/logo_sport.png')).subsample(14, 14)
logo_t02 = PhotoImage(file = resource_path('./logo/logo_movie.png')).subsample(7, 7)
logo_t03 = PhotoImage(file = resource_path('./logo/logo_geography.png')).subsample(14, 14)
logo_t04 = PhotoImage(file = resource_path('./logo/logo_football.png')).subsample(14, 14)
logo_t05 = PhotoImage(file = resource_path('./logo/logo_darts.png')).subsample(14, 14)
logo_t06 = PhotoImage(file = resource_path('./logo/logo_boardgames.png')).subsample(14, 14)
logo_t07 = PhotoImage(file = resource_path('./logo/logo_structural engineering.png')).subsample(14, 14)
logo_t08 = PhotoImage(file = resource_path('./logo/logo_electrical_systems_in_buildings.png')).subsample(14,14)
logo_t09 = PhotoImage(file = resource_path('./logo/logo_electrical_systems_in_buildings.png')).subsample(14,14)
logo_t10 = PhotoImage(file = resource_path('./logo/logo_electrical_systems_in_buildings.png')).subsample(14,14)

# https://www.linkedin.com/learning/python-gui-development-with-tkinter-2/presenting-choices-with-check-buttons-and-radio-buttons?resume=false
# https://stackoverflow.com/questions/63871376/tkinter-widget-cgetvariable
# https://www.geeksforgeeks.org/python-setting-and-retrieving-values-of-tkinter-variable/
choice = IntVar()
topics.add_radiobutton(label = 'Topic One - Sport', variable = choice, value = 1,
                       command= lambda: (quiz.call_topic(resource_path('./data/quiz_sport.json'), 0), quiz.display_topic_label(0)))
topics.add_radiobutton(label = 'Topic Two - Movies', variable = choice, value = 2,
                       command= lambda: (quiz.call_topic(resource_path('./data/quiz_movie.json'), 1), quiz.display_topic_label(1)))
topics.add_radiobutton(label = 'Topic Three - Geography', variable = choice, value = 3,
                       command= lambda: (quiz.call_topic(resource_path('./data/quiz_geography.json'), 2), quiz.display_topic_label(2)))
topics.add_radiobutton(label = 'Topic Four - Football', variable = choice, value = 4,
                       command= lambda: (quiz.call_topic(resource_path('./data/quiz_football.json'), 3), quiz.display_topic_label(3)))
topics.add_radiobutton(label = 'Topic Five - Darts', variable = choice, value = 5,
                       command= lambda: (quiz.call_topic(resource_path('./data/quiz_darts.json'), 4), quiz.display_topic_label(4)))
topics.add_radiobutton(label = 'Topic BONUS', variable = choice, value = 6,
                       command= lambda: (quiz.call_topic(resource_path('./data/quiz_boardgames.json'), 5), quiz.display_topic_label(5)))
topics.add_radiobutton(label = 'T, T-É és SZÉS1', variable = choice, value = 7,
                       command= lambda: (quiz.call_topic(resource_path('./data/quiz_structural_engineering_numbered.json'), 6), quiz.display_topic_label(6)))
topics.add_radiobutton(label = 'Electrical Systems', variable = choice, value = 8,
                       command= lambda: (quiz.call_topic(resource_path('./data/quiz_electrical_systems.json'), 7), quiz.display_topic_label(7)))
topics.add_radiobutton(label = 'Electrical Systems - Earthing', variable = choice, value = 9,
                       command= lambda: (quiz.call_topic(resource_path('./data/quiz_electrical_systems_in_buildings_p02_earthing.json'), 8), quiz.display_topic_label(8)))
topics.add_radiobutton(label = 'Electrical Systems - Part 03', variable = choice, value = 10,
                       command= lambda: (quiz.call_topic(resource_path('./data/quiz_electrical_systems_in_buildings_p03.json'), 9), quiz.display_topic_label(9)))



# customizing the menubar
topics.entryconfig(0, image= logo_t01, compound ='left') # adding icon and position it
topics.entryconfig(1, image= logo_t02, compound ='left') # adding icon and position it
topics.entryconfig(2, image= logo_t03, compound ='left')
topics.entryconfig(3, image= logo_t04, compound = 'left')
topics.entryconfig(4, image= logo_t05, compound = 'left')
topics.entryconfig(5, compound= 'left', state ='disabled') # bonusz topic, initially locked
topics.entryconfig(6, image= logo_t07, compound= 'left') # T, T-É és SZÉS1
topics.entryconfig(7, image= logo_t08, compound= 'left') # bme - electrical systems
topics.entryconfig(8, image= logo_t09, compound= 'left') # bme - electrical systems
topics.entryconfig(9, image= logo_t10, compound= 'left') # bme - electrical systems

# # PROGRESS BAR: # https://www.linkedin.com/learning/python-gui-development-with-tkinter-2/inputting-values-and-displaying-status-with-the-scale-and-progressbar?resume=false
# the bar
progressbar = ttk.Progressbar(frame, orient='horizontal', length=200, mode='determinate', maximum=100)
progressbar.place(x=5, y=450)
progressbar_label = ttk.Label(frame, text="Your progress", font=('Franklin Gothic', 10)) # text label
progressbar_label.place(x=5, y=425)
# progress counter initial
# https://www.geeksforgeeks.org/python-setting-and-retrieving-values-of-tkinter-variable/
progress_counter = StringVar()
progress_counter.set("Correct: 0/0") # initial text string

progress_label = ttk.Label(frame, textvariable=progress_counter, font=('Franklin Gothic', 10))
progress_label.place(x=110, y=425)
progress_label['relief'] = 'groove'

# # :PROGRESS BAR
# :Tkinter GUI

# an instance of class "Quiz"
quiz = Quiz()

# https://stackoverflow.com/questions/29158220/tkinter-understanding-mainloop
# https://stackoverflow.com/questions/43442858/why-my-code-doesnt-open-tkinter-window
guitop.mainloop() #

