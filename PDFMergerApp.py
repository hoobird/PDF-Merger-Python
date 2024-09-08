from tkinter import filedialog, messagebox, Listbox, END
import tkinter as tk
import PyPDF2
from PIL import Image, ImageTk

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger")
        self.pdf_list = []

        self.create_widgets()

    def create_widgets(self):
        self.image = Image.open("logo.png")
        self.image = self.image.resize((150, 150))
        self.photo = ImageTk.PhotoImage(self.image)
        self.logo = tk.Label(self.root, image=self.photo)
        self.logo.pack(pady=10)

        # Pack the listbox to the left
        self.listbox = Listbox(self.root, selectmode=tk.SINGLE, width=50, height=15)
        self.listbox.pack(side=tk.LEFT, padx=10, pady=10)

        # Create a frame for the buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        # Pack the buttons inside the frame
        self.add_button = tk.Button(self.button_frame, text="Add PDF", command=self.add_pdf)
        self.add_button.pack(side=tk.TOP, pady=5)

        self.remove_button = tk.Button(self.button_frame, text="Remove PDF", command=self.remove_pdf)
        self.remove_button.pack(side=tk.TOP, pady=5)

        self.move_up_button = tk.Button(self.button_frame, text="Move Up", command=self.move_up)
        self.move_up_button.pack(side=tk.TOP, pady=5)

        self.move_down_button = tk.Button(self.button_frame, text="Move Down", command=self.move_down)
        self.move_down_button.pack(side=tk.TOP, pady=5)

        self.merge_button = tk.Button(self.button_frame, text="Merge PDFs", command=self.merge_pdfs)
        self.merge_button.pack(side=tk.TOP, pady=5)

    def add_pdf(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        for file_path in file_paths:
            if file_path not in self.pdf_list:
                self.pdf_list.append(file_path)
                self.listbox.insert(END, file_path)

    def remove_pdf(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "No PDF selected")
            return
        index = selected[0]
        self.listbox.delete(index)
        del self.pdf_list[index]

    def move_up(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "No PDF selected")
            return
        index = selected[0]
        if index == 0:
            return
        self.pdf_list[index], self.pdf_list[index - 1] = self.pdf_list[index - 1], self.pdf_list[index]
        self.update_listbox(index - 1)

    def move_down(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "No PDF selected")
            return
        index = selected[0]
        if index == len(self.pdf_list) - 1:
            return
        self.pdf_list[index], self.pdf_list[index + 1] = self.pdf_list[index + 1], self.pdf_list[index]
        self.update_listbox(index + 1)

    def update_listbox(self, selected_index=None):
        self.listbox.delete(0, END)
        for pdf in self.pdf_list:
            self.listbox.insert(END, pdf)
        if selected_index is not None:
            self.listbox.select_set(selected_index)
            self.listbox.activate(selected_index)

    def merge_pdfs(self):
        if not self.pdf_list:
            messagebox.showwarning("Warning", "No PDFs to merge")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not save_path:
            return

        pdf_merger = PyPDF2.PdfMerger()

        for pdf in self.pdf_list:
            pdf_merger.append(pdf)

        with open(save_path, 'wb') as output_pdf:
            pdf_merger.write(output_pdf)

        messagebox.showinfo("Success", "PDFs merged successfully")