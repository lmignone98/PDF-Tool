import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
from PyPDF2 import PdfReader, PdfWriter
import logging
from colorama import Fore
from typing import Tuple
from PIL import Image

logging.basicConfig(level=logging.INFO)


class App:

    ext_allowed = {
        "pdf" : "pdf",
        "jpg" : "image",
        "jpeg" : "image",
        "png" : "image" 
    }

    directions = {"clockwise" : 1, "counterclockwise" : -1}

    def __init__(self) -> None:
        self.logger = logging.getLogger(__file__)
        self.root = TkinterDnD.Tk() 
        self.files = list()
        self.angle : int = None
        self.filetype : str = None
    

    def start(self) -> None:
        self.root.title("Edit your PDFs")
        self.root.geometry("400x275")
        self.root.resizable(False, False)

        lb_info = tk.Label(self.root, text="Drag and Drop your files here")
        lb_info.pack(pady=10)

        self.listbox = tk.Listbox(self.root, width=50, height=8)
        self.listbox.pack(pady=10)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        btn_merge = tk.Button(button_frame, text="Merge", command=self._merge)
        btn_merge.pack(side=tk.LEFT, padx=10)

        btn_rotate = tk.Button(button_frame, text="Rotate", command=self._rotate)
        btn_rotate.pack(side=tk.LEFT, padx=10)

        btn_remove = tk.Button(button_frame, text="Remove", command=self._remove_files)
        btn_remove.pack(side=tk.LEFT, padx=10)

        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self._drop_files)

        self.logger.info(Fore.GREEN + "Starting app" + Fore.RESET)
        self.root.mainloop()
        self.logger.info(Fore.GREEN + "Closing app" + Fore.RESET)
    
    def _remove_files(self) -> None:
        for index in self.listbox.curselection():
            self.files.pop(index)
            self.listbox.delete(index)
        
        self.logger.info(Fore.GREEN + "Removed file" + Fore.RESET)
        self.logger.debug(Fore.YELLOW + f"Files: {self.files}" + Fore.RESET)

    def _drop_files(self, event) -> None:
        self.listbox.delete(0, tk.END)
        files = self.root.tk.splitlist(event.data)
        self.files.extend(files)

        s = set()
        file : str
        for file in self.files:
            ext = file.split(".")[-1].lower()
            name = file.split("/")[-1]

            try:
                ext = self.ext_allowed[ext]
                s.add(ext)
                self.listbox.insert(tk.END, name)
            except KeyError:
                messagebox.showwarning("Error", "Invalid file type")
                self.logger.error(Fore.RED + "Invalid file type" + Fore.RESET)
                self._clear_all()
                return

        if len(s) > 1:
            messagebox.showwarning("Error", "Select files of the same type")
            self.logger.error(Fore.RED + "Different file types selected" + Fore.RESET)
            self._clear_all()
            return

        self.filetype = ext
       
        self.logger.info(Fore.GREEN + "Input files selected" + Fore.RESET)
        self.logger.debug(Fore.YELLOW + f"Selected files: {self.files}" + Fore.RESET)
        

    def _check_files(self, *, n_files : int = None) -> bool:
        if not self.files:
            messagebox.showwarning("Error", "Select at least one file")
            self.logger.error(Fore.RED + "No files selected" + Fore.RESET)
            return False
        
        if n_files and len(self.files) > n_files:
            messagebox.showwarning("Error", "Select only one file")
            self.logger.error(Fore.RED + "More than one file selected" + Fore.RESET)
            return False
    
        return True
    
    def _ask_save_path(self, ext : str, type : Tuple[str, str], title : str = "Save your file") -> str:
        out = filedialog.asksaveasfilename(defaultextension=ext, filetypes=[type], title=title, initialfile="output")
        self.logger.info(Fore.GREEN + "Output file selected" + Fore.RESET)
        self.logger.debug(Fore.YELLOW + f"Output file: {out}" + Fore.RESET)
        return out
    
    def _ask_angle(self) -> bool:
        self.logger.info(Fore.GREEN + "Asking for angle" + Fore.RESET)

        ask_window = tk.Toplevel(self.root)
        ask_window.title("Select the angle")
        ask_window.resizable(False, False)
        ask_window.geometry("230x130")

        angles = [90, 180]
        angle_selection = tk.StringVar(ask_window)
        angle_selection.set(angles[0])

        directions = list(self.directions.keys())
        direction_selection = tk.StringVar(ask_window)
        direction_selection.set(directions[0])

        label = tk.Label(ask_window, text="Select the angle:")
        label.pack(pady=5)

        frame = tk.Frame(ask_window)
        frame.pack(pady=5)

        dropdown_angles = tk.OptionMenu(frame, angle_selection, *angles)
        dropdown_angles.pack(side=tk.LEFT, padx=10)

        dropdown_directions = tk.OptionMenu(frame, direction_selection, *directions)
        dropdown_directions.pack(side=tk.LEFT, padx=10)

        confirm_btn = tk.Button(ask_window, text="Confirm", command = lambda: (setattr(self, 'angle', int(angle_selection.get()) * self.directions[direction_selection.get()]), ask_window.destroy()))
        confirm_btn.pack(pady=5)

        ask_window.wait_window()
        
        if self.angle is None:
            self.logger.error(Fore.RED + "No angle selected" + Fore.RESET)
            return False
        
        return True
    
    def _rotate(self) -> None:
        if not self._check_files(n_files=1) or not self._ask_angle():
            self._clear_all()
            return
        
        self.logger.info(Fore.GREEN + f"Executing rotate operation on {self.filetype}" + Fore.RESET)

        try:
            if self.filetype == "pdf":
                output_path = self._ask_save_path(".pdf", ("PDF files", "*.pdf"))
                self._rotate_pdf(output_path)
            
            elif self.filetype == "image":
                output_path = self._ask_save_path(".jpg", ("JPG files", "*.jpg"))
                self._rotate_image(output_path)
            
            self.logger.info(Fore.GREEN + "Completed" + Fore.RESET)
            messagebox.showinfo("Success", f"Rotated {self.filetype} saved in {output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            self.logger.error(Fore.RED + f"{e}" + Fore.RESET)
        
        self._clear_all()
    
    def _rotate_image(self, output_path) -> None:
        reader = Image.open(self.files[0])
        rotated = reader.rotate(-self.angle, expand=True)
        rotated.save(output_path)

    def _rotate_pdf(self, output_path) -> None:
        reader = PdfReader(self.files[0])
        writer = PdfWriter()

        for page in reader.pages:
            page.rotate(self.angle)
            writer.add_page(page)

        with open(output_path, "wb") as output_file:
            writer.write(output_file)

    def _merge(self) -> None:
        if not self._check_files():
            self._clear_all()
            return
        
        self.logger.info(Fore.GREEN + f"Executing merge operation on {self.filetype}s" + Fore.RESET)

        try:
            output_path = self._ask_save_path(".pdf", ("PDF files", "*.pdf"))

            if self.filetype == "pdf":
                self._merge_pdfs(output_path)

            elif self.filetype == "image":
                self._merge_images(output_path)
            
            self.logger.info(Fore.GREEN + "Completed" + Fore.RESET)
            messagebox.showinfo("Success", f"Merged pdf saved in {output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            self.logger.error(Fore.RED + f"{e}" + Fore.RESET)
        
        self._clear_all()

    def _merge_images(self, output_path) -> None:
        images = [Image.open(img).convert("RGB") for img in self.files]
        images[0].save(output_path, save_all=True, append_images=images[1:])

    def _merge_pdfs(self, output_path) -> None:
        readers = [PdfReader(path) for path in self.files]
        writer = PdfWriter()

        for reader in readers:
            for page in reader.pages:
                writer.add_page(page)

        with open(output_path, "wb") as output_file:
            writer.write(output_file)

    def _clear_all(self) -> None:
        self.listbox.delete(0, tk.END)
        self.files.clear()
        self.angle = None
        self.filetype = None
        self.logger.info(Fore.GREEN + "Cleared all" + Fore.RESET)


if __name__ == "__main__":
    app = App()
    app.start()
