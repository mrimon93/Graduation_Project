from AugurUI import AugurUI
import tkinter as tk

root = tk.Tk()
root.title('Augur')

wind_var = tk.IntVar()
temp_var = tk.IntVar()
date_var = tk.IntVar()
hour_var = tk.IntVar()
predict_var = tk.StringVar()

## Set StringVars for faster testing 
# wind_var.set(2)
# temp_var.set(4)
# date_var.set(7)

## This is a hack to keep UI consistent from start to finish
predict_var.set('\n\n\n\n\n\n\n\n')          # Don't touch it!

AugurUI(root).set_ui(wind_var, temp_var, date_var, hour_var, predict_var)

root.mainloop()
