import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import os
from PIL import Image, ImageTk
from close import close_program
import tkinter.simpledialog as simpledialog
from print import print_file
from preferences import Preferences
import os
import shutil
import tkinter as tk
from tkinter import ttk
from preferences import Preferences
import tkinter.filedialog as filedialog
import subprocess



class Notepad:
    def __init__(self, root):
        self.root = root
        self.root.title("Otterpad")
        self.current_file = None
        self.text = tk.Text(self.root, font=("Arial", 12), undo=True, wrap='word')
        self.text.pack(expand=True, fill='both')

        scrollbar = tk.Scrollbar(self.root, command=self.text.yview)
        scrollbar.pack(side='right', fill='y')
        self.text['yscrollcommand'] = scrollbar.set

        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save", command=self.save)
        file_menu.add_command(label="Open", command=self.open)
        file_menu.add_command(label="New", command=self.create_new_file)
        file_menu.add_command(label="Open containing folder", command=self.open_containing_folder)
        file_menu.add_command(label="Open in Notepad", command=self.open_in_notepad)
        file_menu.add_command(label="Save As", command=self.save_as)
        file_menu.add_command(label="Rename", command=self.rename_file)
        file_menu.add_command(label="Cerrar", command=close_program)
        file_menu.add_command(label="Print", command=lambda: print.print_file(notepad=self))
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

    def select_all(self):
        self.text.tag_add("sel", "1.0", "end")

    def save(self):
        if self.current_file:
            contents = self.text.get("1.0", "end-1c")
            with open(self.current_file, "w") as file:
                file.write(contents)
        else:
            self.save_as()

    def open(self):
        file_dialog = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_dialog:
            with open(file_dialog, "r") as file:
                contents = file.read()

            self.text.delete("1.0", "end")
            self.text.insert("1.0", contents)
            self.current_file = file_dialog
            self.root.title(os.path.basename(self.current_file) + " - Otterpad")

    def create_new_file(self):
        self.text.delete("1.0", "end")
        self.current_file = None
        self.root.title("Untitled - Otterpad")

    def search(self):
        search_term = simpledialog.askstring("Search", "Enter text to search:")
        if search_term:
            index = self.text.search(search_term, "1.0", stopindex="end")
            if index != "":
                line, col = index.split(".")
                self.text.tag_configure("search", background="yellow")
                self.text.tag_add("search", index, f"{index}+{len(search_term)}c")
                self.text.mark_set("insert", f"{index}+{len(search_term)}c")
                self.text.see(index)
            else:
                messagebox.showinfo("Search", "Text not found")
    def convert_to_uppercase(self):
        content = self.text.get("1.0", "end-1c")
        upper_content = content.upper()
        self.text.delete("1.0", "end")
        self.text.insert("1.0", upper_content)

    def convert_to_lowercase(self):
        content = self.text.get("1.0", "end-1c")
        lower_content = content.lower()
        self.text.delete("1.0", "end")
        self.text.insert("1.0", lower_content)

    def replace(self):
        find_text = simpledialog.askstring("Replace", "Find text:")
        if find_text:
            replace_text = simpledialog.askstring("Replace", "Replace with:")
            if replace_text is not None:
                content = self.text.get("1.0", "end-1c")
                replaced_content = content.replace(find_text, replace_text)
                self.text.delete("1.0", "end")
                self.text.insert("1.0", replaced_content)
    def cut(self):
        self.text.event_generate("<<Cut>>")

    def copy(self):
        self.text.event_generate("<<Copy>>")

    def paste(self):
        self.text.event_generate("<<Paste>>")

    def deselect_all(self):
        self.text.tag_remove("sel", "1.0", "end")

    def goto_line(self):
        line_number = simpledialog.askinteger("Go to Line", "Enter line number:")
        if line_number is not None:
            self.text.mark_set("insert", f"{line_number}.0")
            self.text.see("insert")

    def word_count(self):
        content = self.text.get("1.0", "end-1c")
        words = len(content.split())
        messagebox.showinfo("Word Count", f"Words: {words}")

    def character_count(self):
        content = self.text.get("1.0", "end-1c")
        chars = len(content)
        messagebox.showinfo("Character Count", f"Characters: {chars}")

    def invert_case(self):
        content = self.text.get("1.0", "end-1c")
        inverted_content = content.swapcase()
        self.text.delete("1.0", "end")
        self.text.insert("1.0", inverted_content)

    def title_case(self):
        content = self.text.get("1.0", "end-1c")
        title_content = content.title()
        self.text.delete("1.0", "end")
        self.text.insert("1.0", title_content)

    def sentence_case(self):
        content = self.text.get("1.0", "end-1c")
        sentence_content = content.capitalize()
        self.text.delete("1.0", "end")
        self.text.insert("1.0", sentence_content)


    def open_containing_folder(self):
        if self.current_file:
            folder_path = os.path.dirname(os.path.abspath(self.current_file))
            if os.name == 'nt':  # Si es Windows
                subprocess.Popen(f'explorer "{folder_path}"')
            elif os.name == 'posix':  # Si es macOS o Linux
                subprocess.Popen(['open', folder_path])
        else:
            messagebox.showerror("Error", "No hay archivo abierto para mostrar su directorio.")
    def open_in_notepad(self):
        if self.current_file:
            if os.name == 'nt':  # Si es Windows
                subprocess.Popen(['notepad.exe', self.current_file])
            else:
                messagebox.showerror("Error", "Esta función solo está disponible en Windows.")
        else:
            messagebox.showerror("Error", "No hay archivo abierto para abrir en Notepad.")

    def save_as(self):
        file_dialog = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_dialog:
            contents = self.text.get("1.0", "end-1c")
            with open(file_dialog, "w") as file:
                file.write(contents)

            self.current_file = file_dialog
            self.root.title(os.path.basename(self.current_file) + " - Otterpad")

    def rename_file(self):
        if self.current_file:
            file_directory, old_filename = os.path.split(self.current_file)
            new_filename = filedialog.asksaveasfilename(initialdir=file_directory, initialfile=old_filename, defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if new_filename:
                shutil.move(self.current_file, new_filename)
                self.current_file = new_filename
                self.root.title(os.path.basename(self.current_file) + " - Otterpad")
        else:
            messagebox.showerror("Error")

def main():
    root = tk.Tk()
    root.geometry("800x600")

    icon_path = os.path.join("imagenes", "iconoblockdenotas.ico")

    icon_image = Image.open(icon_path)
    icon_image = icon_image.resize((32, 32), Image.LANCZOS)
    icon = ImageTk.PhotoImage(icon_image)
    root.call('wm', 'iconphoto', root._w, icon)

    root.title("Otterpad")

    notepad = Notepad(root)
    root.mainloop()

if __name__ == "__main__":
    main()

