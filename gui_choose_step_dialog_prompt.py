from tkinter import * #imports
from tkinter import Tk
import tkinter.font as font


class choose_step_prompt():
    def __init__(self):
        self.operation = None
        self.cancel = False
        self.root = None

    def show(self):
        '''Show the window, and wait for the user to click a button'''
        self.root = Tk()
        bg_win = 'gray11'
        self.root.configure(bg=bg_win)

        # TODO: somehow exit main loop as well when closing this gui window
        self.root.protocol('WM_DELETE_WINDOW', self.doCloseWindow)

        # set font size, family and style for labels
        labelFont = font.Font(family='Helvetica', size=16, weight='bold')
        label2Font = font.Font(family='Helvetica', size=10)
        buttonFont = font.Font(family='Helvetica', size=10, weight='bold')

        # create labels and buttons and assign font layout
        label = Label(self.root, text = "Which step would you like to execute?", fg='DarkOliveGreen2', bg=bg_win)
        label['font'] = labelFont
        true_button = Button(self.root, text = "Step1: video infos", bg='olive drab',
                                command= lambda: self.finish(True))
        label2 = Label(self.root, text="Step2 requires the footfall frames!", fg='firebrick1', bg=bg_win)
        label2['font'] = label2Font
        false_button = Button(self.root, text = "Step2: calibration & conversion", bg='olive drab',
                                 command= lambda: self.finish(False))
        false_button['font'] = buttonFont
        true_button['font'] = buttonFont

        # arrange labels and buttons in window
        label.pack(pady=10, padx=10)
        true_button.pack(fill=X, padx=50, pady=5)
        label2.pack(pady=5)
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

    def doCloseWindow(self):
        # check if saving
        # if not:
        self.cancel = True
        self.root.destroy()
        self.root.quit()
        return

