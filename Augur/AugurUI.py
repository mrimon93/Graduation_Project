import sys
from AugurLogic import  AugurLogic
import tkinter.ttk as ttk

class AugurUI:

    def __init__(self, root) -> None:
        '''
        Parameters:
        -----------
            root : parent (tk.Tk())
        Example: root = tk.Tk()     '''

        self.root  = root

        ## Pretty systems does not need custom colors.
        self.dark  = ''
        self.light = ''

        ## Instansiate logic
        self.a_logic = AugurLogic()

        ## Windows always needs special attention...
        if sys.platform in 'win32': 

            print('o-oh, sensing Windows OS...') 

            ## Yes, we NEED these for Windows!
            self.dark  = '#343444'
            self.light = '#ffffff'

            ## Set background on main window
            self.root.config(background = self.dark)

            ## Set theme...
            self.style = ttk.Style(self.root)  
            self.style.theme_use('clam')
        


    def set_ui(self, wind_var, temp_var, date_var, hour_var, day_var, predict_var):
        '''Initialize UI elements.              \n
        For prettier UI, tk.StringVar() is used.\n
        Parameter:
        ----------
            wind_var : tk.StringVar()
            temp_var : tk.StringVar()
            date_var : tk.StringVar()
            predict_var : tk.StringVar()        '''

        ttk.Label(self.root,
            text = 'Hour of the day:',
            background = self.dark,
            foreground = self.light
        ).pack(pady = 8)
        ttk.Entry(self.root, textvariable = hour_var, justify = 'center').pack()

        ttk.Label(self.root,
            text = 'Month as Integer:',
            background = self.dark,
            foreground = self.light
        ).pack(pady = 8)
        ttk.Entry(self.root, textvariable = date_var, justify = 'center').pack()

        ttk.Label(self.root,
            text = 'Day as Integer:',
            background = self.dark,
            foreground = self.light
        ).pack(pady = 8)
        ttk.Entry(self.root, textvariable = day_var, justify = 'center').pack()

        ttk.Label(self.root,
            text='Average Wind Speed:',
            background = self.dark,
            foreground = self.light
        ).pack(pady = 8)
        ttk.Entry(self.root, textvariable = wind_var, justify = 'center').pack(padx = 16)

        ttk.Label(self.root,
            text = 'Average Temperature:',
            background = self.dark,
            foreground = self.light
        ).pack(pady = 8)
        ttk.Entry(self.root, textvariable = temp_var, justify = 'center').pack()

        ttk.Button(
            self.root,                # lambda: Used on command below,
            text    = 'Run',          # or will trigger on initiation
            command = lambda: self.a_logic.get_input_and_predict( # <- This line
                wind_var, temp_var, date_var, hour_var, day_var, predict_var
            )
        ).pack(pady = 8)

        ttk.Label(self.root,
            text = 'Prediction:',
            background = self.dark,
            foreground = self.light
        ).pack()

        ttk.Label(      # Empty on start, uses all
            self.root,  # entries for printing message
            textvariable = predict_var,
            background   = self.dark,
            foreground   = self.light,
            justify      = 'center',
        ).pack(pady = 18)

        btn_close = ttk.Button(self.root,
            text = 'Close',
            command = lambda: exit()).pack(pady = 8) # <- another lambda: