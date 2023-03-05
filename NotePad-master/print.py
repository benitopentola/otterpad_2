import os
import subprocess
import tempfile


def print_file(notepad):
    file_contents = notepad.text.get("1.0", "end-1c")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
        temp_file.write(file_contents.encode("utf-8"))
        temp_file.flush()

        temp_file_path = os.path.join(tempfile.gettempdir(), temp_file.name)

        if os.name == "nt":
            os.startfile(temp_file_path, "print")
        elif os.name == "posix":
            subprocess.call(["lp", temp_file_path])
