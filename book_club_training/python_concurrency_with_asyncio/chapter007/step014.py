import tkinter as tk
from tkinter import ttk

window = tk.Tk()
window.title("Hello world app")
window.geometry("200x100")


def say_hello():
    print("Привет!")


hello_button = ttk.Button(window, text="Say hello", command=say_hello)
hello_button.pack()
window.mainloop()
