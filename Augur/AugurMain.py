''' Idiosyncratic Augur.
Run this file from project root folder.
Example from terminal:
python.exe .\Augur\AugurMain.py
'''
from AugurUI import AugurUI
import tkinter as tk

root = tk.Tk()
root.title('Augur')
root.geometry('220x600')

wind_var = tk.IntVar()
temp_var = tk.IntVar()
day_var  = tk.IntVar()
date_var = tk.IntVar()
hour_var = tk.IntVar()
predict_var = tk.StringVar()

## Set StringVars for faster testing 
# wind_var.set(2)
# temp_var.set(4)
# date_var.set(7)

## This is a hack to keep UI consistent from start to finish
predict_var.set('Use average values\nas input for\nwind and temeprature.\n\n\n\n\n\n')          # Don't touch it!

AugurUI(root).set_ui(wind_var, temp_var, date_var, hour_var, day_var, predict_var)

## Center window
# Gets the requested values of the height and widht.
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
print("Width",windowWidth,"Height",windowHeight)
 
# Gets both half the screen width/height and window width/height
positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
positionDown  = int(root.winfo_screenheight()/2 - windowHeight/2) - 160
 
# Positions the window in the center of the page.
root.geometry("+{}+{}".format(positionRight, positionDown))

# Start program
root.mainloop()
