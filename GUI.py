import tkinter as tk
from tkinter import ttk
import multiprocessing


class SynthGUI(tk.Frame):
    def __init__(self, queue, master=None):
        super().__init__(master)
        self.master = master
        self.queue = queue
        self.create_widgets()

    def create_widgets(self):
        self.key_label = tk.Label(self.master, text="Key: ")
        self.octave_label = tk.Label(self.master, text="Octave")
        self.quality_label = tk.Label(self.master, text="Scale Type: ")
        self.submit = tk.Button(self.master, text="Submit", command=self.submit)
        self.key = ttk.Combobox(self.master, text="Key", width=27)
        self.octave = ttk.Combobox(self.master, text="Octave", width=27)
        self.quality = ttk.Combobox(self.master, width=27)
        self.quality['values'] = ('Major', 'Minor')
        self.quit = tk.Button(self.master, text="QUIT", fg="red",
                              command=self.quit)
        self.key['values'] = ('C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B')
        self.octave['values'] = ('0', '1', '2', '3', '4', '5', '6', '7')

        self.key_label.grid(row="0", column="0")
        self.octave_label.grid(row="1", column="0")
        self.quality_label.grid(row="2", column="0")
        self.key.grid(row='0', column='2')
        self.octave.grid(row='1', column='2')
        self.quality.grid(row='2', column='2')
        self.submit.grid(row='3', column='2')
        self.quit.grid(row='4', column='2')

    def submit(self):
        self.queue.put((self.key.get(), int(self.octave.get()), self.quality.get()))

    def quit(self):
        self.queue.put(-1)
        self.master.destroy()


class GUIProc(multiprocessing.Process):
    def __init__(self, queue):
        super(GUIProc, self).__init__()
        self.queue = queue

    def run(self):
        root = tk.Tk()
        root.geometry('500x250')
        app = SynthGUI(self.queue, master=root)
        app.mainloop()