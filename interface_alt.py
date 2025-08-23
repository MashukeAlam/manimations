import customtkinter
import tkinter
from tkinter import ttk
import os
import glob
import threading
import subprocess
import json

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Manimations GUI")
        self.geometry("1200x700")
        self.scripts_dir = "scripts"
        self.done_file = os.path.join(self.scripts_dir, "done.txt")
        self.current_file_path = None

        # Configure grid layout (3 columns, 1 row)
        self.grid_columnconfigure(0, weight=1, minsize=250)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=2, minsize=300)
        self.grid_rowconfigure(0, weight=1)

        self.setup_left_panel()
        self.setup_center_panel()
        self.setup_right_panel()

        self.populate_script_list()

    def setup_left_panel(self):
        left_panel = customtkinter.CTkFrame(self, corner_radius=0)
        left_panel.grid(row=0, column=0, sticky="nsew")
        left_panel.grid_rowconfigure(1, weight=1)
        left_panel.grid_columnconfigure(0, weight=1)

        title_label = customtkinter.CTkLabel(left_panel, text="Script Management", font=customtkinter.CTkFont(size=16, weight="bold"))
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.tree = ttk.Treeview(left_panel, columns=("Status",), show="tree headings")
        self.tree.heading("#0", text="Script Name")
        self.tree.heading("Status", text="Status")
        self.tree.column("#0", anchor="w")
        self.tree.column("Status", anchor="center", width=60)
        self.tree.grid(row=1, column=0, sticky="nsew", padx=(10, 0))
        self.tree.bind("<<TreeviewSelect>>", self.on_script_select)

        refresh_button = customtkinter.CTkButton(left_panel, text="Refresh", command=self.populate_script_list)
        refresh_button.grid(row=2, column=0, padx=20, pady=10)

    def setup_center_panel(self):
        center_panel = customtkinter.CTkFrame(self, corner_radius=0)
        center_panel.grid(row=0, column=1, sticky="nsew")
        center_panel.grid_rowconfigure(1, weight=1)
        center_panel.grid_columnconfigure(0, weight=1)
        
        tab_view = customtkinter.CTkTabview(center_panel)
        tab_view.grid(row=0, column=0, sticky="nsew", rowspan=2)
        tab_view.add("JSON Editor")

        self.editor_textbox = customtkinter.CTkTextbox(tab_view.tab("JSON Editor"), wrap="none")
        self.editor_textbox.pack(expand=True, fill="both")

        save_button = customtkinter.CTkButton(center_panel, text="Save Script", command=self.save_script)
        save_button.grid(row=2, column=0, padx=20, pady=10)

    def setup_right_panel(self):
        right_panel = customtkinter.CTkFrame(self, corner_radius=0)
        right_panel.grid(row=0, column=2, sticky="nsew")
        right_panel.grid_rowconfigure(3, weight=1)
        right_panel.grid_columnconfigure(0, weight=1)

        title_label = customtkinter.CTkLabel(right_panel, text="Controls & Status", font=customtkinter.CTkFont(size=16, weight="bold"))
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        controls_frame = customtkinter.CTkFrame(right_panel)
        controls_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        controls_frame.grid_columnconfigure(0, weight=1)

        gen_video_button = customtkinter.CTkButton(controls_frame, text="Generate Video")
        gen_video_button.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        
        process_all_button = customtkinter.CTkButton(controls_frame, text="Process All New")
        process_all_button.grid(row=1, column=0, sticky="ew", pady=5)

        gen_shorts_button = customtkinter.CTkButton(controls_frame, text="Generate Shorts")
        gen_shorts_button.grid(row=2, column=0, sticky="ew", pady=5)

        self.progress_bar = customtkinter.CTkProgressBar(right_panel)
        self.progress_bar.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        self.progress_bar.set(0)

        self.log_textbox = customtkinter.CTkTextbox(right_panel, wrap="word", state="disabled")
        self.log_textbox.grid(row=3, column=0, sticky="nsew", padx=20, pady=(0, 20))

    def populate_script_list(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        processed_files = []
        if os.path.exists(self.done_file):
            with open(self.done_file, 'r') as f:
                processed_files = [line.strip() for line in f.readlines()]

        script_files = glob.glob(os.path.join(self.scripts_dir, "*.json"))
        for script_file in sorted(script_files):
            file_name = os.path.basename(script_file)
            status = "✅" if file_name in processed_files else "⏳"
            self.tree.insert("", "end", text=file_name, values=(status,), iid=script_file)

    def on_script_select(self, event=None):
        selected_items = self.tree.selection()
        if not selected_items:
            return
        
        self.current_file_path = selected_items[0]
        try:
            with open(self.current_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.editor_textbox.delete("1.0", "end")
            self.editor_textbox.insert("1.0", content)
        except (IOError, UnicodeDecodeError) as e:
            self.log(f"Error reading file: {e}")

    def save_script(self):
        if not self.current_file_path:
            self.log("No file selected to save.")
            return

        content = self.editor_textbox.get("1.0", "end-1c")
        try:
            # Validate JSON before saving
            json.loads(content)
            with open(self.current_file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.log(f"Successfully saved {os.path.basename(self.current_file_path)}")
        except json.JSONDecodeError:
            self.log("Error: Invalid JSON format. Please correct and save again.")
        except IOError as e:
            self.log(f"Error saving file: {e}")

    def log(self, message):
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert("end", message + "\n")
        self.log_textbox.configure(state="disabled")
        self.log_textbox.see("end")


if __name__ == "__main__":
    app = App()
    app.mainloop()
