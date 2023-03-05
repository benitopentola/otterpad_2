import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import os
from PIL import Image, ImageTk
from close import close_program
from print import print_file
from preferences import Preferences
import tkinter as tk
from tkinter import ttk
from preferences import Preferences


class Notepad:
    def __init__(self, root):
        self.root = root
        self.root.title("Otterpad")
        self.current_file = None
        self.text = tk.Text(self.root, font=("Arial", 12))
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

        edit_menu = tk.Menu(menubar)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Search", command=self.search)
        edit_menu.add_command(label="Replace", command=self.replace)
        edit_menu.add_separator()
        edit_menu.add_command(label="Convert to Uppercase", command=self.convert_to_uppercase)
        edit_menu.add_command(label="Convert to Lowercase", command=self.convert_to_lowercase)
        edit_menu.add_command(label="Select All", command=self.select_all)

        preferences_menu = tk.Menu(menubar)
        menubar.add_cascade(label="Help", menu=preferences_menu)
        preferences_menu.add_command(label="Open Help", command=self.open_preferences)

    def open_preferences(self):
        preferences_window = tk.Toplevel(self.root)
        preferences_window.title("Preferences")
        preferences = Preferences(preferences_window)

    def rename_file(self):
        current_file = self.current_file
        if not current_file:
            return

        new_name = filedialog.asksaveasfilename(initialfile=os.path.basename(current_file), defaultextension=".txt")
        if not new_name:
            return

        os.rename(current_file, new_name)
        self.current_file = new_name
        self.root.title(os.path.basename(new_name) + " - Otterpad")

    def get_current_file(self):
        current_file = self.root.title().split(" - ")[0]
        return current_file

    def save(self):
        contents = self.text.get("1.0", "end-1c")

        file_dialog = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_dialog:
            with open(file_dialog, "w") as file:
                file.write(contents)
            self.current_file = file_dialog
            self.root.title(os.path.basename(self.current_file) + " - Otterpad")

    def open(self):
        file_dialog = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_dialog:
            with open(file_dialog, "r") as file:
                contents = file.read()

            self.text.delete("1.0", "end")
            self.text.insert("1.0", contents)

    def create_new_file(self):
        file_dialog = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_dialog:
            with open(file_dialog, "w") as file:
                file.write("")

    def open_containing_folder(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            folder_path = os.path.dirname(file_path)
            os.startfile(folder_path)

    def open_in_notepad(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            os.startfile(file_path)

    def search(self):
        search_window = tk.Toplevel(self.root)
        search_window.title("Search")

        tk.Label(search_window, text="Search term:").pack()
        search_term = tk.Entry(search_window)
        search_term.pack()

        def do_search():
            term = search_term.get()
            if not term:
                return

            self.text.tag_remove("sel", "1.0", "end")

            start = "1.0"
            while True:
                start = self.text.search(term, index=start, stopindex="end")
                if not start:
                    break

                end = f"{start}+{len(term)}c"
                self.text.tag_add("sel", start, end)
                self.text.see(start)

                self.text.tag_configure("highlight", background="yellow")

                self.text.tag_add("highlight", start, end)

                start = end

        search_button = tk.Button(search_window, text="Search", command=do_search)
        search_button.pack()

    def replace(self):
        replace_window = tk.Toplevel(self.root)
        replace_window.title("Replace")

        tk.Label(replace_window, text="Search term:").pack()
        search_term = tk.Entry(replace_window)
        search_term.pack()

        tk.Label(replace_window, text="Replace term:").pack()
        replace_term = tk.Entry(replace_window)
        replace_term.pack()

        def do_replace():
            search = search_term.get()
            replace = replace_term.get()

            start = "1.0"
            while True:
                start = self.text.search(search, start, stopindex="end")
                if not start:
                    break

                end = self.text.index(f"{start}+{len(search)}c")
                self.text.delete(start, end)
                self.text.insert(start, replace)

        replace_button = tk.Button(replace_window, text="Replace", command=do_replace)
        replace_button.pack()

    def convert_to_uppercase(self):

        current_text = self.text.get("1.0", "end-1c")

        uppercase_text = current_text.upper()

        self.text.delete("1.0", "end")

        self.text.insert("1.0", uppercase_text)

    def convert_to_lowercase(self):

        current_text = self.text.get("1.0", "end-1c")

        lowercase_text = current_text.lower()

        self.text.delete("1.0", "end")

        self.text.insert("1.0", lowercase_text)

    def save_as(self):
        # Obtener el contenido del editor
        contents = self.text.get("1.0", "end-1c")

        # Abrir un cuadro de diálogo para seleccionar el nombre y la ubicación de la copia
        file_dialog = filedialog.asksaveasfilename(defaultextension=".txt")

        if file_dialog:
            with open(file_dialog, "w") as file:
                file.write(contents)

    def select_all(self):
        self.text.tag_add("sel", "1.0", "end")


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Window")

        # Botón para abrir la ventana de preferencias
        preferences_button = tk.Button(self.root, text="Preferences", command=self.open_preferences)
        preferences_button.pack()

        # Etiqueta para mostrar el mensaje de confirmación de cambio de color
        self.message_label = ttk.Label(self.root, text="")
        self.message_label.pack(pady=10)

    def open_preferences(self):
        preferences_window = tk.Toplevel(self.root)
        Preferences(preferences_window, self.root, self.update_background_color)

    def update_background_color(self, color):
        # Configura el color de fondo de la ventana principal con el color seleccionado en la ventana de preferencias
        self.root.configure(background=color)

        # Actualiza la etiqueta de mensaje con el mensaje de confirmación
        self.message_label.configure(text="Color de fondo cambiado a {}".format(color))
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