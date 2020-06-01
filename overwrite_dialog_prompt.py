from tkinter import * #imports
from tkinter import Tk


class open_prompt():
    def __init__(self):
        self.operation = None
        self.root = None

    def show(self, output_filename):
        '''Show the window, and wait for the user to click a button'''
        print("show")
        self.root = Tk()
        label = Label(self.root, text = "File {} already exists. Overwrite?".format(output_filename))
        true_button = Button(self.root, text = "Yes",
                                command= lambda: self.finish(True))
        false_button = Button(self.root, text = "NO!",
                                 command= lambda: self.finish(False))
        label.pack()
        true_button.pack()
        false_button.pack()

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

