import tkinter as tk
from tkinter import ttk, filedialog, simpledialog
import os
import smtplib
from email.mime.text import MIMEText

class Preferences:
    def __init__(self, root):
        self.root = root
        self.root.title("Preferences")

        ttk.Button(self.root, text="Set file save location", command=self.select_save_location).grid(row=0, column=0, padx=10, pady=10)

        ttk.Button(self.root, text="Ilerna web", command=self.launch_browser).grid(row=1, column=0, padx=10, pady=10)

        ttk.Button(self.root, text="Request for help", command=self.send_email).grid(row=2, column=0, padx=10, pady=10)

        ttk.Button(self.root, text="Option 4").grid(row=3, column=0, padx=10, pady=10)

        self.save_location = ""

    def select_save_location(self):
        folder_path = filedialog.askdirectory()
        self.save_location = folder_path

    def launch_browser(self):
        os.system("python browser.py")

    def send_email(self):
        smtp_server = "smtp.gmail.com"
        port = 587

        sender_email = simpledialog.askstring("Email", "Ingresa tu dirección de correo electrónico:", parent=self.root)
        password = simpledialog.askstring("Password", "Ingresa tu contraseña de correo electrónico:", parent=self.root, show="*")
        receiver_email = "Javiergraciafn@gmail.com"
        message = MIMEText("Este es un mensaje de prueba enviado desde Python")
        message["Subject"] = "Solicitud de ayuda"
        message["From"] = sender_email
        message["To"] = receiver_email

        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())

def open_preferences():
    preferences_window = tk.Toplevel()
    Preferences(preferences_window)

if __name__ == "__main__":
    root = tk.Tk()
    preferences_button = tk.Button(root, text="Preferences", command=open_preferences)
    preferences_button.pack()
    root.mainloop()
