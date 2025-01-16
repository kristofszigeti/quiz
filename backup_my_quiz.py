# Setting up the script for a quiz game with GUI

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

# Quiz content from exterior files
# get the data from the json file
# with open('.\\data\\quiz_sport.json', 'r') as datafile:
#     data_dict = json.load(datafile)

# set the question, choices, and answer
# question = (data_dict['question'])
# choices = (data_dict['choices'])
# answer = (data_dict['answer'])
# hint = (data_dict['hints'])

# combine data into a list
# data_list = list(zip(data_dict['question'], data_dict['choices'], data_dict['answer'], data_dict['hints']))

# random.shuffle(data_list)
# question, choices, answer, hint = zip(*data_list) # unpack the shuffled data back into separate lists

# Convert back to lists (optional, depending on how you use them)
# question = list(question)
# choices = list(choices)
# answer = list(answer)
# hint = list(hint)

# question = []
# choices = []
# answer = []
# hint = []

# our main class
class Quiz:
    # dunder method: __init__
    # initialize all the methods to display contents and create the functions available
    def __init__(self):

        # set question number to 0
        self.q_no = 0

        # initialization of a counter of correct answers
        self.correct = 0

        # initial data content
        self.question = []
        self.options = []
        self.answer = []
        self.hint = []
        # self.data_size = []

        # assigns ques to the display_question function to update later.
        self.display_title()
        # self.display_question()

        # opt_selected holds an integer value which is used for selected option in a question.
        self.opt_selected = IntVar()

        # displaying radio button for the current question and used to
        # display choices for the current question
        # self.opts = self.radio_buttons()
        self.opts = None

        # display choices for the current question
        # self.display_options()

        # displays the button for next_btn, hint_btn, quit_btn
        self.buttons()

        # number of questions
        self.data_size = len(self.question)

        # showing if the answer is correct or wrong, # in this form it does not do anything, must be referred it later and add/customize the response with text and color
        self.feedback = ttk.Label(frame, font=('Franklin Gothic', 15, 'bold'), anchor='center', justify='center')
        self.feedback.place(x=370, y=320)

        guitop.bind('<Return>', self.next_btn) # https://stackoverflow.com/questions/54251768/how-do-i-keybind-functions-to-keys-in-the-keyboard-with-tkinter
        guitop.bind('<Escape>', lambda event: guitop.destroy()) # unnamed callable/function to handle event

    # This method is used to display the result
    # It counts the number of correct and wrong answers
    # and then display them at the end as a message Box
    def display_result(self):

        # calculates the wrong count
        wrong_count = self.data_size - self.correct
        correct = f"Correct: {self.correct}"
        wrong = f"Wrong: {wrong_count}"

        # calcultaes the percentage of correct answers
        score = int(self.correct / self.data_size * 100)
        result = f"Your score: {score}%"

        # Shows a message box to display the result
        mb.showinfo("Result", f"{result}\n{correct}\n{wrong}")

        return result

    # This method checks the Answer after we click on Next.
    def check_ans(self, q_no):

        # checking if the selected option is correct (else-case=not correct)
        if self.opt_selected.get() == self.answer[q_no]:
            # # my little bonus
            # with open("turtle_Race.py", "r") as bonus:
            #     exec(bonus.read())
            # if the option is correct it return true
            self.feedback['foreground'] = "green" # it sets the font color to green
            # self.feedback["bg"] = "light gray"  # set the background color
            self.feedback["text"] = 'Correct! \U0001F5F8' # light check mark: https://www.fileformat.info/info/unicode/char/1f5f8/index.htm
            return True
        else:
            self.feedback['foreground'] = 'red' # it sets the font color to red, indicating the answer is not correct
            # self.feedback["bg"] = "light gray"  # set the background color
            self.feedback['text'] = f'\u274C Oops!\nNext time!' # cross mark https://www.fileformat.info/info/unicode/char/274c/index.htm
            return False

    # This method is used to check the answer of the
    # current question by calling the check_ans and question no.
    # if the question is correct it increases the count by 1
    # and then increase the question number by 1. If it is last
    # question then it calls display result to show the message box.
    # otherwise shows next question.
    def next_btn(self, event=None):

        # Check if the answer is correct
        if self.check_ans(self.q_no) == True:
            # if the answer is correct (True) it increments the value of variable correct by 1
            self.correct += 1

        # Update progress bar and label
        progress_value = (self.correct / self.data_size) * 100
        progress["value"] = progress_value
        progress_label_var.set(f"Correct: {self.correct}/{self.data_size}")

        # Moves to next Question by incrementing the q_no counter
        self.q_no += 1

        # checks if the q_no size is equal to the data size
        if self.q_no == self.data_size:

            # if it is correct then it displays the score
            self.display_result()

            with open("result.txt", "a", encoding="UTF-8") as outfile:
                line_newscore= f"{quiz.display_result()}, {date.today()} {time.strftime("%H:%M:%S")}\n"  # +name # https://www.geeksforgeeks.org/get-current-date-and-time-using-python/
                outfile.write(line_newscore)

            # closes (destroys) the GUI
            guitop.destroy()

        else:
            # shows the next question
            self.display_question()
            self.display_options()

    # This method is used to provide a hint to help the user in answering
    # the current question by calling a pop-up window.
    def hint_btn(self):
        # Shows a message box to display the result
        mb.showinfo("Result", f"You asked me for a hint.\nHere it is:\n{self.hint[self.q_no]}")

    def open_rankings(self):
        with open("result.txt", "r") as ranking:
            exec(ranking.read())

    # This method shows the two buttons on the screen.
    # The first one is the next_button which moves to next question
    # It has properties like what text it shows the functionality,
    # size, color, and property of text displayed on button. Then it
    # mentions where to place the button on the screen. The second
    # button is the exit button which is used to close the GUI without
    # completing the quiz.
    def buttons(self):

        # next_button itself for checking the answer and moving to the next question
        next_button = Button(frame, text="Next",
                             command=self.next_btn, # call the next_btn method of the class Quiz
                             width=10, bg='lightblue', fg='black', font=('Franklin Gothic', 16, 'bold'), activebackground='darkblue', activeforeground='white')

        # placing the next_button on the screen
        next_button.place(x=350, y=380)

        # hint_button itself to show a hint to the user
        hint_button = Button(frame, text="Hint",
                             command=self.hint_btn, # call the hint_btn method of the class Quiz
                             width=10, bg="seashell", fg="black", font=('Franklin Gothic', 12, 'bold'), activebackground='gold', activeforeground='black')

        # placing the button on the screen
        hint_button.place(x=600, y=300)

        # quit_button to close the game and the window
        quit_button = Button(frame, text="Quit",
                             command=guitop.destroy, # destroy is built-in therefore belongs to the parent=guitop
                             width=5, bg="light grey", fg="black", font=('Franklin Gothic', 12, 'bold'), activebackground='maroon', activeforeground='white')

        # placing the Quit button on the screen
        quit_button.place(x=700, y=400) # it is the bottom-right corner

    # This method deselect the radio button on the screen
    # Then it is used to display the choices available for the current
    # question which we obtain through the question number and Updates
    # each of the choices for the current question of the radio button.
    def display_options(self):
        val = 0

        # deselecting the choices
        self.opt_selected.set(0)

        # looping over the choices to be displayed for the
        # text of the radio buttons.
        for option in self.options[self.q_no]:
            self.opts[val]['text'] = option
            val += 1

    # This method shows the current Question on the screen
    def display_question(self):

        # showing questions inside a Label widget
        # https://www.geeksforgeeks.org/python-tkinter-label/?ref=lbp
        if self.q_no < len(self.question):
            q_no = Label(frame, text=self.question[self.q_no], wraplength= 700,
                         font=('Franklin Gothic', 16, 'bold'), anchor='n', justify='center',
                         width=55, height=3, border= 10)

            # placing the option on the screen
            q_no.place(x=40, y=80)

    # This method is used to Display Title
    def display_title(self):

        # The title to be shown
        title = Label(frame, text="Quiz Game",
                      width=50, bg="green", fg="white", font=('Franklin Gothic', 20, "bold"))

        # place of the title
        title.place(x=0, y=0)

        # # The title to be shown
        # topic = Label(frame, text=f"{topics.entrycget(0, "label")}",
        #               width=50, fg="black", font=("Franklin Gothic", 16, "bold"), justify='center')
        #
        # # place of the title
        # topic.place(x=90, y=50)

    # This method shows the radio buttons to select the Question
    # on the screen at the specified position. It also returns a
    # list of radio button which are later used to add the choices to
    # them.
    def radio_buttons(self):

        # initialize the list with an empty list of choices
        q_list = []

        # position of the first option
        y_pos = 170

        # adding the choices to the list
        while len(q_list) < 4:
            # setting the radio button properties
            radio_btn = Radiobutton(frame, text="", variable=self.opt_selected,
                                    value=len(q_list) + 1, font=('Franklin Gothic', 14), width= 40, anchor='w',justify="left")

            # adding the button to the list
            q_list.append(radio_btn)

            # placing the button
            radio_btn.place(x=100, y=y_pos)

            # incrementing the y-axis position by 40
            y_pos += 40

        # return the radio buttons
        return q_list

    def call_topic(self, topic_datafile, topic_length=2):
        # load quiz topic files
        with open(topic_datafile, 'r', encoding='utf-8') as datafile:
            data_dict = json.load(datafile)

        # combine data into a list
        data_list = list(zip(data_dict['question'], data_dict['choices'], data_dict['answer'], data_dict['hints']))
        # random.shuffle(data_list)
        data_sample_list = random.sample(data_list, k=topic_length)

        # Unpack the shuffled data back into separate lists
        # global question, choices, answer, hint
        self.question, self.options, self.answer, self.hint = zip(*data_sample_list)

        # restore the initial status
        self.q_no = 0
        self.correct = 0
        self.data_size = len(self.question)
        self.opts = self.radio_buttons()
        self.display_question()
        self.display_options()

        # restore progress bar and label
        progress["value"] = 0
        progress_label_var.set(f"Correct: 0/{len(self.question)}")

        # restore feedback label
        self.feedback["text"] = "" # 'blank' status
        # print("Questions:", self.question)
        # print("Options:", self.choices)
        # print("Answers:", self.answer)
        # print("Hints:", self.hint)

# Tkinter GUI:
# create a top-level GUI Window
guitop = Tk()

# set the size of the GUI Window
guitop_width = 800
guitop_height = 480

# put the window to the center # https://www.youtube.com/watch?v=Z8jdlBNIaDo
# queries the screensize setting and store them in a variable
screen_width = guitop.winfo_screenwidth()
screen_height = guitop.winfo_screenheight()
# print(screen_width, screen_height)
# positions the parent window
guitop.geometry(f"{guitop_width}x{guitop_height}+{(screen_width // 2)-(guitop_width // 2)}+{(screen_height // 2)-(guitop_height // 2)}")
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
results = Menu(menubar)
# help_ = Menu(menubar)

menubar.add_cascade(menu = topics, label ='Topics')
menubar.add_cascade(menu = results, label ='Results')
# menubar.add_cascade(menu = help_, label = 'Help')

results.add_command(label ='Ranking', command = lambda: quiz.open_rankings())
results.add_separator()

# results.entryconfig('New', accelerator ='Ctrl+N')
logo_t01 = PhotoImage(file ='.\\logo\\python_logo.gif').subsample(10, 10) # Change path as needed
# logo_t02 = PhotoImage(file = 'python_logo.gif').subsample(10, 10) # Change path as needed
# logo_t03 = PhotoImage(file = 'python_logo.gif').subsample(10, 10) # Change path as needed
# logo_t04 = PhotoImage(file = 'python_logo.gif').subsample(10, 10) # Change path as needed

# results.entryconfig('Open...', state ='disabled')

save = Menu(results)
results.add_cascade(menu = save, label ='Save')
save.add_command(label = 'Save As',command = lambda: print('Saving As...'))
save.add_command(label = 'Save All', command = lambda: print('Saving All...'))

choice = IntVar()
topics.add_radiobutton(label = 'Topic One - Sport', variable = choice, value = 1,
                       command= lambda: quiz.call_topic('.\\data\\quiz_sport.json'))
topics.add_radiobutton(label = 'Topic Two - Movies', variable = choice, value = 2,
                       command= lambda: quiz.call_topic('.\\data\\quiz_movie.json',))
topics.add_radiobutton(label = 'Topic Three - ***', variable = choice, value = 3,
                       command= lambda: quiz.call_topic('.\\data\\quiz_sport.json'))
topics.add_radiobutton(label = 'Topic Four - ***', variable = choice, value = 4,
                       command= lambda: quiz.call_topic('.\\data\\quiz_sport.json'))

# customize the menubar
topics.entryconfig('Topic One - Sport', image= logo_t01, compound ='left')
topics.entryconfig('Topic Two - Movies')
topics.entryconfig('Topic Three - ***')
topics.entryconfig('Topic Four - ***', state ='disabled')

# PROGRESS BAR: # https://www.linkedin.com/learning/python-gui-development-with-tkinter-2/inputting-values-and-displaying-status-with-the-scale-and-progressbar?resume=false
# Create a bar
progress = ttk.Progressbar(frame, orient='horizontal', length=200, mode="determinate", maximum=100)
progress.place(x=5, y=420)

# Create a StringVar to hold the progress text
progress_label_var = StringVar()
progress_label_var.set("Correct: 0/0")

# Overlay a Label for progress display
progress_label = ttk.Label(frame, textvariable=progress_label_var, font=('Franklin Gothic', 12))
progress_label.place(x=60, y=450)  # Position near the progress bar
# print(progress_label.config())

# Function to update progress without exceeding maximum
def update_progress(value):
    if value > progress["maximum"]:
        value = progress["maximum"]  # Clamp to maximum
    progress["value"] = value
# :PROGRESS BAR
# :Tkinter GUI

# create an instance of "Quiz" class.
quiz = Quiz()

# Start the GUI
guitop.mainloop()

# END OF THE PROGRAM
