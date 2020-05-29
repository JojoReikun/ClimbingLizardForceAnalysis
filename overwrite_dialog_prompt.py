from tkinter import * #imports
from tkinter import Tk


class open_prompt(object):
    def __init__(self):
        self.operation = None
        self.root = None

    def show(self, output_filename):
        '''Show the window, and wait for the user to click a button'''

        self.root = Tk()
        label = Label(self.root, text = "File {} already exists. Overwrite?".format(output_filename))
        true_button = Button(self.root, text = "True",
                                command= lambda: self.finish(True))
        false_button = Button(self.root, text = "False",
                                 command= lambda: self.finish(False))

        true_button.pack()
        false_button.pack()

        # start the loop, and wait for the dialog to be
        # destroyed. Then, return the value:
        self.root.mainloop()
        return self.operation

    def finish(self, operation):
        '''Set the value and close the window

        This will cause the show() function to return.
        '''
        self.operation = operation
        self.root.destroy()
