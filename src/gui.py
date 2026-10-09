import os
from tkinter import filedialog, messagebox
import customtkinter as ctk
from src.touchstone_handler import TouchstoneManager

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Touchstone Multi-File Extractor")
        self.geometry("650x600")

        self.manager = TouchstoneManager()

        # UI Components Setup
        self._build_ui()

    def _build_ui(self):
        self.btn_browse = ctk.CTkButton(
            self, text="Select Touchstone File", command=self.on_load_file
        )
        self.btn_browse.pack(pady=15)

        self.lbl_file_info = ctk.CTkLabel(
            self,
            text="No file selected",
            wraplength=550,
            text_color="gray",
        )
        self.lbl_file_info.pack(pady=5)

        self.frame_config = ctk.CTkFrame(self)
        self.frame_config.pack(pady=10, padx=20, fill="both", expand=True)

        lbl_instructions = ctk.CTkLabel(
            self.frame_config,
            text=(
                "Specify port groups per file (1 line = 1 output file).\n"
                "Port numbering starts at 1, e.g, 2-port network has ports 1 and 2.\n"
                "Divide individual ports with \",\" or specify range with \"-\".\n"
                "Example: \n"
                "1,2\n"
                "3-8\n"
                "This will result in saving two networks:\n"
                "- two-port network with ports 1 and 2,\n"
                "- six-port network with ports 3, 4, 5, 6, 7, and 8.\n"
            ),
            justify="left",
        )
        lbl_instructions.pack(pady=10, padx=10, anchor="w")

        self.textbox_ports = ctk.CTkTextbox(self.frame_config, height=180)
        self.textbox_ports.pack(pady=5, padx=10, fill="both", expand=True)
        

        self.btn_process = ctk.CTkButton(
            self,
            text="Extract and Save All Files",
            command=self.on_process_batch,
            state="disabled",
        )
        self.btn_process.pack(pady=15)

    def on_load_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Touchstone File",
            filetypes=[("Touchstone files", "*.s*p"), ("All files", "*.*")],
        )
        if not file_path:
            return

        try:
            meta = self.manager.load_file(file_path)
            info_text = (
                f"Loaded: {meta['filename']}\n"
                f"Total Ports: {meta['ports']} | "
                f"Frequency: {meta['freq_start_mhz']:.1f} MHz - {meta['freq_stop_mhz']:.1f} MHz"
            )
            self.lbl_file_info.configure(text=info_text, text_color="white")
            self.btn_process.configure(state="normal")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{e}")

    def on_process_batch(self):
        text_content = self.textbox_ports.get("1.0", "end").strip()
        lines = [
            line.strip() for line in text_content.splitlines() if line.strip()
        ]
        
        if not lines:
            messagebox.showwarning("Missing Input", "Enter port configuration!")
            return
        
        initial_directory = ""
        if self.manager.file_path:
            initial_directory = os.path.dirname(self.manager.file_path)
        
        output_dir = filedialog.askdirectory(
            title="Select Output Folder",
            initialdir=initial_directory)
        if not output_dir:
            return

        try:
            count = self.manager.process_batch_extraction(lines, output_dir)
            messagebox.showinfo(
                "Success", f"Successfully generated {count} file(s)!"
            )
        except ValueError as ve:
            messagebox.showerror("Configuration Error", str(ve))
        except Exception as e:
            messagebox.showerror("Export Error", f"An error occurred:\n{e}")