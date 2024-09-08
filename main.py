import tkinter as tk
from PDFMergerApp import PDFMergerApp

def main():
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
