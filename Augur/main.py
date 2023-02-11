import sys
import tkinter.ttk as ttk
import tkinter as tk





root = tk.Tk()
dark = '#343444'
light= '#ffffff'
root.title('Augur')

wind_var = tk.StringVar()
temp_var = tk.StringVar()
date_var = tk.StringVar()
predict_var = tk.StringVar()

lbl_wind = ttk.Label(root, text='Average Wind Speed:', background=dark, foreground=light).pack(pady=8)
inp_wind = ttk.Entry(root, textvariable = wind_var).pack(padx=16)

lbl_temp = ttk.Label(root, text='Average Temperature:', background=dark, foreground=light).pack(pady=8)
inp_temp = ttk.Entry(root, textvariable = temp_var).pack()

lbl_date = ttk.Label(root, text='Month as Integer:', background=dark, foreground=light).pack(pady=8)
inp_date = ttk.Entry(root, textvariable = date_var).pack()

btn_run  = ttk.Button(root, text='Run').pack(pady=8)

lbl_temp = ttk.Label(root, text='Prediction:',background = dark, foreground=light).pack()
inp_temp = ttk.Label(root, textvariable = predict_var, background = dark, foreground=light).pack(pady=100)

btn_close = ttk.Button(root, text='Close', command=lambda:exit()).pack(pady=8)

if sys.platform in 'win32':  
    root.config(background = dark)
    # lbl_wind.
    style = ttk.Style(root)  
    style.theme_use('clam')

root.mainloop()
