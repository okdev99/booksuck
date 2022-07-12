import tkinter

class my_window:
    def __init__(self, win):
        self.button = tkinter.Button(window, text="Start", fg='black', bg='white')
        self.button.place(x=200, y=200)

        self.label = tkinter.Label(window, text="GUI Test: Input form", fg="black", font=("Roboto", 20))
        self.label.place(x=150, y=20)

        self.chapter_name = tkinter.Entry(window, text="Chapter name here.", bg="white", fg="black")
        self.chapter_name.place(x=100, y=300)
        self.button.bind("<Button-1>", self.print_entry)

        self.result = tkinter.Entry(bg="white", fg="black")
        self.result.place(x=200, y=500)

    def print_entry(self, event):
        #self.chapter_name.delete(0, 'end')
        txt = self.chapter_name.get()
        self.result.insert(-1, str(txt))

window = tkinter.Tk()
my_win = my_window(window)
window.title("GUI Test")
window.geometry("300x200+10+20") #widthxheight+XPOS+YPOS
window.mainloop()


