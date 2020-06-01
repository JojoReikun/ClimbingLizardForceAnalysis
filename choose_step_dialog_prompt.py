from tkinter import * #imports
from tkinter import Tk


class choose_step_prompt():
    def __init__(self):
        self.operation = None
        self.cancel = False
        self.root = None

    def show(self):
        '''Show the window, and wait for the user to click a button'''
        self.root = Tk()

        # TODO: somehow exit main loop as well when closing this gui window
        self.root.protocol('WM_DELETE_WINDOW', self.doCloseWindow)

        label = Label(self.root, text = "Which step would you like to execute?")
        true_button = Button(self.root, text = "Step1: video infos",
                                command= lambda: self.finish(True))
        label2 = Label(self.root, text="Step2 requires the footfall frames!")
        false_button = Button(self.root, text = "Step2: calibration & conversion",
                                 command= lambda: self.finish(False))
        label.pack()
        true_button.pack()
        label2.pack()
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

    def doCloseWindow(self):
        # check if saving
        # if not:
        self.cancel = True
        self.root.destroy()
        self.root.quit()
        return

