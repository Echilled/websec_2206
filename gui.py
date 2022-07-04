

import tkinter as tk


def main():
    parent_window = tk.Tk()  # landing page
    txt = tk.Label(parent_window, text="Web Mon")
    txt.pack()
    parent_window.mainloop()


if __name__ == '__main__':
    main()