from tkinter import *
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

        self.root.protocol('WM_DELETE_WINDOW', self.doCloseWindow)

        # set font size, family and style for labels
        labelFont = font.Font(family='Helvetica', size=16, weight='bold')
        label2Font = font.Font(family='Helvetica', size=10)
        buttonFont = font.Font(family='Helvetica', size=10, weight='bold')

        # create labels and buttons and assign font layout
        label = Label(self.root, text = "Which step would you like to execute?", fg='DarkOliveGreen2', bg=bg_win)
        label['font'] = labelFont
        step1_button = Button(self.root, text = "Step1: video infos", bg='olive drab',
                                command= lambda: self.finish("step1"))
        label2 = Label(self.root, text="Step2 requires {}_forceAnalysis.csv with footfall frames!", fg='firebrick1', bg=bg_win)
        label2['font'] = label2Font
        step2_button = Button(self.root, text = "Step2: calibration & conversion", bg='olive drab',
                                 command= lambda: self.finish("step2"))

        label3 = Label(self.root, text="Step3 requires {}_forceAnalysis_calib.csv from Step2 and force files in 1 folder!",
                       fg='firebrick1', bg=bg_win)
        label3['font'] = label2Font
        step3_button = Button(self.root, text="Step 3: Align forces & videos & extract Max, Min, Means", bg='olive drab',
                                 command= lambda: self.finish("step3"))

        label4 = Label(self.root,
                       text="Stride Dynamics for hfren geckos, requires force output (matlab), corrected forces, DLC results and morphometrics!",
                       fg='firebrick1', bg=bg_win)
        label4['font'] = label2Font
        step4_button = Button(self.root, text="Step 4: Generate mean force profiles",
                              bg='olive drab',
                              command=lambda: self.finish("step4"))

        step1_button['font'] = buttonFont
        step2_button['font'] = buttonFont
        step3_button['font'] = buttonFont
        step4_button['font'] = buttonFont

        # arrange labels and buttons in window
        label.pack(pady=10, padx=10)
        step1_button.pack(fill=X, padx=50, pady=5)
        label2.pack(pady=5)
        step2_button.pack(fill=X, padx=50, pady=5)
        label3.pack(pady=5)
        step3_button.pack(fill=X, padx=50, pady=5)
        label4.pack(pady=5)
        step4_button.pack(fill=X, padx=50, pady=5)


        # start the loop, and wait for the dialog to be
        # destroyed. Then, return the value:
        self.root.mainloop()

        return self.operation


    def finish(self, operation):
        '''Automatically get's called when pressing a button (command).
        Sets the value (string of step and step number) and closes the window.
        This will cause the show() function to return.
        '''
        self.operation = operation
        self.root.destroy()
        self.root.quit()

    def doCloseWindow(self):
        self.cancel = True
        self.root.destroy()
        self.root.quit()
        return

