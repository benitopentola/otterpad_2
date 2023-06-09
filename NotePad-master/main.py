import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import os
from PIL import Image, ImageTk
import tkinter.simpledialog as simpledialog
import subprocess
import sqlite3
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
import sqlite3
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class Notepad:
    def __init__(self, root):
        self.root = root
        self.root.title("Otterpad")
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')
        self.first_time = True
        self.new_file()
        self.current_file_path = None
        self.text = tk.Text(self.root, font=("Arial", 12), undo=True, wrap='word')
        self.autosave()

        scrollbar = tk.Scrollbar(self.root, command=self.text.yview)
        scrollbar.pack(side='right', fill='y')
        self.text['yscrollcommand'] = scrollbar.set

        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save", command=self.save)
        file_menu.add_command(label="Open", command=self.open)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open containing folder", command=self.open_containing_folder)
        file_menu.add_command(label="Open in Notepad", command=self.open_in_notepad)
        file_menu.add_command(label="Save As", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Close", command=self.root.destroy)
        file_menu.add_command(label="Exit", command=self.root.quit)

        edit_menu = tk.Menu(menubar)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.text.edit_undo)
        edit_menu.add_command(label="Redo", command=self.text.edit_redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.cut)
        edit_menu.add_command(label="Copy", command=self.copy)
        edit_menu.add_command(label="Paste", command=self.paste)
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", command=self.select_all)
        edit_menu.add_command(label="Deselect All", command=self.deselect_all)
        edit_menu.add_separator()
        edit_menu.add_command(label="Go to Line", command=self.goto_line)
        edit_menu.add_command(label="Word Count", command=self.word_count)
        edit_menu.add_command(label="Character Count", command=self.character_count)
        edit_menu.add_separator()
        edit_menu.add_command(label="Search", command=self.search)
        edit_menu.add_command(label="Replace", command=self.replace)
        edit_menu.add_separator()
        edit_menu.add_command(label="Convert to Uppercase", command=self.convert_to_uppercase)
        edit_menu.add_command(label="Convert to Lowercase", command=self.convert_to_lowercase)
        edit_menu.add_command(label="Invert Case", command=self.invert_case)
        edit_menu.add_command(label="Title Case", command=self.title_case)
        edit_menu.add_command(label="Sentence Case", command=self.sentence_case)

    def new_file(self, _=None):
        if not self.first_time:
            open_in_new_tab = messagebox.askyesno("New File", "Do you want to create a new tab?")
        else:
            open_in_new_tab = False
            self.first_time = False

        if open_in_new_tab:
            # Crea una nueva pestaña en la ventana actual
            file_frame = ttk.Frame(self.notebook)
            self.notebook.add(file_frame, text='Untitled')
            text_widget = tk.Text(file_frame, font=("Arial", 12), undo=True, wrap='word')
            text_widget.pack(expand=True, fill='both')
            self.notebook.select(file_frame)
        else:
            # Cierra el archivo actual y abre uno nuevo en la misma pestaña
            current_tab = self.notebook.select()
            if current_tab:
                self.notebook.forget(current_tab)

            file_frame = ttk.Frame(self.notebook)
            self.notebook.add(file_frame, text='Untitled')
            text_widget = tk.Text(file_frame, font=("Arial", 12), undo=True, wrap='word')
            text_widget.pack(expand=True, fill='both')
            self.notebook.select(file_frame)

        self.notebook.bind("<Control-n>", self.new_file)

    def autosave_file(self, text_widget):
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        file_name = "file"
        file_number = 0

        while True:
            if file_number == 0:
                file_path = os.path.join(downloads_folder, f"{file_name}.txt")
            else:
                file_path = os.path.join(downloads_folder, f"{file_name}_{file_number}.txt")

            if not os.path.exists(file_path):
                with open(file_path, "w") as file:
                    file.write(text_widget.get(1.0, tk.END))
                break
            else:
                file_number += 1

    def autosave(self, interval=60000):  # Intervalo en milisegundos, 60000 ms = 1 minuto
        current_tab = self.notebook.index(self.notebook.select())
        text_widget = self.notebook.nametowidget(self.notebook.select())

        self.autosave_file(text_widget)
        self.root.after(interval, self.autosave, interval)

    def sentence_case(self):
        content = self.text.get("1.0", "end-1c")
        sentence_content = '. '.join([i.capitalize() for i in content.split('. ')])
        self.text.delete("1.0", "end")
        self.text.insert("1.0", sentence_content)

    def select_all(self):
        self.text.tag_add("sel", "1.0", "end")

    def save(self):
        if self.current_file_path:
            current_tab = self.notebook.index(self.notebook.select())
            file_frame = self.notebook.nametowidget(self.notebook.tabs()[current_tab])
            text_widget = file_frame.winfo_children()[0]

            contents = text_widget.get("1.0", "end-1c")
            with open(self.current_file_path, 'w') as file:
                file.write(contents)

        else:
            self.save_as()

    def open(self):
        file_dialog = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_dialog:
            self.current_file_path = file_dialog
            with open(file_dialog, 'r') as file:
                contents = file.read()
            current_tab = self.notebook.index(self.notebook.select())
            file_frame = self.notebook.nametowidget(self.notebook.tabs()[current_tab])
            text_widget = file_frame.winfo_children()[0]

            text_widget.delete("1.0", "end")
            text_widget.insert("1.0", contents)
            self.notebook.tab(file_frame, text=os.path.basename(self.current_file_path))

    def create_new_file(self):
        self.current_file_path = None
        self.text.delete("1.0", "end")
        self.root.title("Otterpad")

    def autosave(self, interval=60000):
        current_tab = self.notebook.index(self.notebook.select())
        file_frame = self.notebook.nametowidget(self.notebook.tabs()[current_tab])
        text_widget = file_frame.winfo_children()[0]
        self.autosave_file(text_widget)
        self.root.after(interval, self.autosave, interval)

    def open_containing_folder(self):
        if self.current_file_path:
            folder = os.path.dirname(self.current_file_path)
            subprocess.run(['explorer', folder])

    def open_in_notepad(self):
        if self.current_file_path:
            subprocess.run(['notepad', self.current_file_path])

    def save_as(self):
        file_dialog = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_dialog:
            self.current_file_path = file_dialog
            self.save()
            self.root.title(f"Otterpad - {os.path.basename(self.current_file_path)}")

    def cut(self):
        self.text.event_generate("<<Cut>>")

    def copy(self):
        self.text.event_generate("<<Copy>>")

    def paste(self):
        self.text.event_generate("<<Paste>>")

    def deselect_all(self):
        self.text.tag_remove("sel", "1.0", "end")

    def goto_line(self):
        line_number = simpledialog.askinteger("Goto Line", "Enter line number:", parent=self.root, minvalue=1)
        if line_number:
            self.text.mark_set("insert", f"{line_number}.0")

    def word_count(self):
        content = self.text.get("1.0", "end-1c")
        words = len(content.split())
        messagebox.showinfo("Word Count", f"Words: {words}")

    def character_count(self):
        content = self.text.get("1.0", "end-1c")
        characters = len(content)
        messagebox.showinfo("Character Count", f"Characters: {characters}")

    def search(self):
        pass

    def replace(self):
        pass

    def convert_to_uppercase(self):
        content = self.text.get("1.0", "end-1c")
        self.text.delete("1.0", "end")
        self.text.insert("1.0", content.upper())

    def convert_to_lowercase(self):
        content = self.text.get("1.0", "end-1c")
        self.text.delete("1.0", "end")
        self.text.insert("1.0", content.lower())

    def invert_case(self):
        content = self.text.get("1.0", "end-1c")
        self.text.delete("1.0", "end")
        self.text.insert("1.0", content.swapcase())

    def title_case(self):
        content = self.text.get("1.0", "end-1c")
        self.text.delete("1.0", "end")
        self.text.insert("1.0", content.title())

        def sentence_case(self):
            content = self.text.get("1.0", "end-1c")
            sentences = content.split('. ')
            sentence_cased = '. '.join([s.capitalize() for s in sentences])
            self.text.delete("1.0", "end")
            self.text.insert("1.0", sentence_cased)

        def search(self):
            search_query = simpledialog.askstring("Search", "Enter search query:", parent=self.root)
            if search_query:
                start = self.text.search(search_query, "1.0", stopindex="end")
                if start:
                    end = f"{start.split('.')[0]}.{int(start.split('.')[1]) + len(search_query)}"
                    self.text.tag_add("highlight", start, end)
                    self.text.tag_configure("highlight", background="yellow", foreground="black")
                    self.text.mark_set("insert", end)
                else:
                    messagebox.showinfo("Search", f"'{search_query}' not found.")

        def replace(self):
            replace_dialog = tk.Toplevel(self.root)
            replace_dialog.title("Replace")
            tk.Label(replace_dialog, text="Find:").grid(row=0, column=0, sticky='e')
            tk.Label(replace_dialog, text="Replace:").grid(row=1, column=0, sticky='e')

            find_entry = tk.Entry(replace_dialog)
            replace_entry = tk.Entry(replace_dialog)
            find_entry.grid(row=0, column=1, padx=2, pady=2, sticky='we')
            replace_entry.grid(row=1, column=1, padx=2, pady=2, sticky='we')

            def find_and_replace():
                find_text = find_entry.get()
                replace_text = replace_entry.get()
                content = self.text.get("1.0", "end-1c")
                new_content = content.replace(find_text, replace_text)
                self.text.delete("1.0", "end")
                self.text.insert("1.0", new_content)

            tk.Button(replace_dialog, text="Replace All", command=find_and_replace).grid(row=2, column=1, sticky='e',
                                                                                         padx=2, pady=2)
            replace_dialog.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    notepad = Notepad(root)
    root.mainloop()

