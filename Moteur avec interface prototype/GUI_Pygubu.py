import tkinter as tk
from tkinter.constants import DISABLED
import tkinter.ttk as ttk
from pygubu.widgets.scrollbarhelper import ScrollbarHelper
from search_engine import search


class NewprojectApp:
    def __init__(self, master=None):
        # build ui
        self.frame2 = ttk.Frame(master)

        self.scrollbar = ScrollbarHelper(self.frame2, scrolltype='both')
        self.scrollbar.configure(usemousewheel=False)
        self.scrollbar.place(anchor='nw', relheight='0.68', relwidth='1.0', rely='0.16', x='0', y='0')
        
        self.label1 = ttk.Label(self.frame2)
        self.label1.configure(text='           Terme :')
        self.label1.place(anchor='nw', relheight='0.08', relwidth='0.22', relx='0.03', rely='0.06', x='0', y='0')

        self.entry2 = ttk.Entry(self.frame2)
        self.entry2.configure(exportselection='true')
        self.entry2.place(anchor='nw', relheight='0.06', relwidth='0.26', relx='0.25', rely='0.07', x='0', y='0')

        self.button2 = ttk.Button(self.frame2)
        self.button2.configure(text='Chercher', command=lambda: func(app))
        self.button2.place(anchor='nw', relheight='0.06', relwidth='0.13', relx='0.57', rely='0.07', x='0', y='0')


        self.text1 = tk.Text(self.frame2)
        self.text1.configure(cursor='arrow', font='TkMenuFont', height='10', width='50', state=DISABLED)
        self.text1.place(anchor='nw', relheight='0.65', relwidth='0.97', relx='0.0', rely='0.16', x='0', y='0')

        self.error = ttk.Label(self.frame2)
        self.error.place(anchor='sw', relheight='0.08', relwidth='1.0', relx='0.05', rely='0.95', x='0', y='0')


        self.frame2.configure(height='600', width='800')
        self.frame2.pack(side='top')


        # Main widget
        self.mainwindow = self.frame2


    def run(self):
        self.mainwindow.mainloop()



def func(app:NewprojectApp):
    app.text1.configure(state='normal')

    app.error.configure(text="")
    app.text1.delete(1.0,"end")
    sucess, result = search(app.entry2.get())
    if not sucess:
        app.error.configure(text=result)
    else:
        app.text1.insert(1.0, '\n'.join(result))
    
    app.text1.configure(state='disabled')


if __name__ == '__main__':
    import tkinter as tk
    root = tk.Tk()
    app = NewprojectApp(root)
    app.run()

