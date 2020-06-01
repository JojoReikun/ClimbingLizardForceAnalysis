from tkinter import * #imports
from tkinter import Tk
import tkinter.font as font


class open_prompt():
    def __init__(self):
        self.operation = None
        self.root = None

    def show(self, output_filename):
        '''Show the window, and wait for the user to click a button'''
        self.root = Tk()
        bg_win = 'gray11'
        self.root.configure(bg=bg_win)

        # set font size, family and style for labels
        labelFont = font.Font(family='Helvetica', size=10, weight='bold')
        buttonFont = font.Font(family='Helvetica', size=10, weight='bold')

        # create labels and buttons and assign font layout
        label = Label(self.root, text = "File >>{}<< already exists. Overwrite?".format(output_filename),
                      fg='firebrick1', bg=bg_win)
        label['font'] = labelFont
        true_button = Button(self.root, text = "Yes",
                                command= lambda: self.finish(True), bg='olive drab')
        false_button = Button(self.root, text = "NO!",
                                 command= lambda: self.finish(False), bg='orange red')
        true_button['font'] = buttonFont
        false_button['font'] = buttonFont

        # arrange labels and buttons in window
        label.pack(pady=10, padx=10)
        true_button.pack(fill=X, padx=50, pady=5)
        false_button.pack(fill=X, padx=50, pady=5)

        # start the loop, and wait for the dialog to be
        # destroyed. Then, return the value:
        self.root.mainloop()
        return self.operation

    def finish(self, operation):
        '''Automatically get's called when pressing a button (command).
        Sets the value and close the window.
        This will cause the show() function to return.
        '''
        self.operation = operation
        self.root.destroy()
        self.root.quit()

