import tkinter as tk
from tkinter import filedialog
import subprocess
import os
import shutil
import zipfile

class PyInstallerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PyInstaller GUI")
        self.geometry("400x200")

        self.file_path = ""
        self.output_path = ""
        # self.copy_files = ["C:\\Users\\NicCornejo\\Documents\\create-executables\\config.json",
        #                    "C:\\Users\\NicCornejo\\Documents\\create-executables\\IDAutomationHC39M Free Version.otf",
        #                    "C:\\Users\\NicCornejo\\Documents\\create-executables\\pdfium.dll",
        #                    "C:\\Users\\NicCornejo\\Documents\\create-executables\\Technical-Response-Logo.ico"
        #                    ]

        self.create_widgets()

    def create_widgets(self):
        self.file_label = tk.Label(self, text="Select File:")
        self.file_label.pack()

        self.file_button = tk.Button(self, text="Browse", command=self.browse_file)
        self.file_button.pack()

        self.output_label = tk.Label(self, text="Output Path:")
        self.output_label.pack()

        self.output_button = tk.Button(self, text="Browse", command=self.browse_output)
        self.output_button.pack()

        self.include_label = tk.Label(self, text="Click to begin package export:")
        self.include_label.pack()

        self.run_button = tk.Button(self, text="Run PyInstaller", command=self.run_pyinstaller)
        self.run_button.pack()

    def browse_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        
    def browse_output(self):
        self.output_path = filedialog.asksaveasfilename(defaultextension=".exe")


    def run_pyinstaller(self):
        if not self.file_path:
            tk.messagebox.showerror("Error", "Please select a file.")
            return

        if not self.output_path:
            tk.messagebox.showerror("Error", "Please select an output path.")
            return

        command = [
            "pyinstaller",
            "--onefile",
            f"--distpath={os.path.dirname(self.output_path)}",
            f"--name={os.path.basename(self.output_path)}",
            self.file_path
        ]

        try:
            subprocess.run(command, check=True)
            # for file_path in self.copy_files:
            #     file_name = os.path.basename(file_path)
            #     shutil.copy(file_path, os.path.join(os.path.dirname(self.output_path), file_name))

            # Copy the build folder
            # Move the build folder and spec file to the same location
            build_path = os.path.join(os.path.dirname(self.output_path), 'build')
            shutil.move('build', build_path)
            spec_file = os.path.basename(self.output_path) + '.spec'
            spec_file_path = os.path.join(os.path.dirname(self.output_path), spec_file)
            shutil.move(spec_file, spec_file_path)


            # Create a zip file containing the build folder and spec file
            output_filename = os.path.basename(self.output_path)
            base_name, extension = os.path.splitext(output_filename)
            zip_file_path = os.path.join(os.path.dirname(self.output_path), f"{base_name}.zip")

            with zipfile.ZipFile(zip_file_path, 'w') as zipf:
                zipf.write(self.output_path, os.path.basename(self.output_path))
                zipf.write(build_path, os.path.basename(build_path))
                zipf.write(spec_file_path, os.path.basename(spec_file_path))

            # Delete the original files
            os.remove(self.output_path)
            shutil.rmtree(build_path)
            os.remove(spec_file_path)

            tk.messagebox.showinfo("Success", "Files created and copied successfully!")

        except subprocess.CalledProcessError as e:
            tk.messagebox.showerror("Error", f"PyInstaller failed with error: {e}")

if __name__ == "__main__":
    app = PyInstallerGUI()
    app.mainloop()