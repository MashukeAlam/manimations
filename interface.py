import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import glob
import subprocess
import threading
import datetime
from pathlib import Path

# Set appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ManimationsGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Manimations - Video Tutorial Generator")
        self.root.geometry("1400x900")
        
        # Variables
        self.current_script = None
        self.quality_var = ctk.StringVar(value="ql")  # Default to low quality
        self.show_logs_var = ctk.BooleanVar(value=True)
        self.nasa_api_key = ctk.StringVar()
        self.voice_var = ctk.StringVar(value="en-GB-SoniaNeural")
        
        self.setup_ui()
        self.refresh_script_list()
        self.load_voice_setting()
        
    def setup_ui(self):
        # Create main container
        main_container = ctk.CTkFrame(self.root)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Top menu bar
        self.create_menu_bar()
        
        # Main content area
        content_frame = ctk.CTkFrame(main_container)
        content_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        # Left panel - Script Management
        self.create_left_panel(content_frame)
        
        # Center panel - Script Editor
        self.create_center_panel(content_frame)
        
        # Right panel - Controls & Status
        self.create_right_panel(content_frame)
        
        # Bottom panel - Logs (initially hidden)
        self.create_bottom_panel(main_container)
        
    def create_menu_bar(self):
        menu_frame = ctk.CTkFrame(self.root, height=40)
        menu_frame.pack(fill="x", padx=10, pady=(10, 0))
        menu_frame.pack_propagate(False)
        
        # File menu buttons
        ctk.CTkButton(menu_frame, text="New Script", command=self.new_script, width=100).pack(side="left", padx=5, pady=5)
        ctk.CTkButton(menu_frame, text="Open Script", command=self.open_script, width=100).pack(side="left", padx=5, pady=5)
        ctk.CTkButton(menu_frame, text="Save Script", command=self.save_script, width=100).pack(side="left", padx=5, pady=5)
        
        # Tools menu buttons
        ctk.CTkButton(menu_frame, text="Cleanup Logs", command=self.cleanup_logs, width=100).pack(side="left", padx=(20, 5), pady=5)
        
        # Help button
        ctk.CTkButton(menu_frame, text="Help", command=self.show_help, width=80).pack(side="right", padx=5, pady=5)
        
    def create_left_panel(self, parent):
        left_frame = ctk.CTkFrame(parent, width=300)
        left_frame.pack(side="left", fill="y", padx=(0, 10))
        left_frame.pack_propagate(False)
        
        # Title
        ctk.CTkLabel(left_frame, text="Script Explorer", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        # Script list
        self.script_listbox = tk.Listbox(left_frame, bg="#2b2b2b", fg="white", selectbackground="#1f538d")
        self.script_listbox.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.script_listbox.bind("<<ListboxSelect>>", self.on_script_select)
        
        # Buttons
        button_frame = ctk.CTkFrame(left_frame)
        button_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        ctk.CTkButton(button_frame, text="Refresh", command=self.refresh_script_list).pack(fill="x", pady=2)
        ctk.CTkButton(button_frame, text="Delete Script", command=self.delete_script).pack(fill="x", pady=2)
        
    def create_center_panel(self, parent):
        center_frame = ctk.CTkFrame(parent)
        center_frame.pack(side="left", fill="both", expand=True)
        
        # Title
        ctk.CTkLabel(center_frame, text="Script Editor", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        # Text editor
        self.text_editor = tk.Text(center_frame, bg="#2b2b2b", fg="white", insertbackground="white")
        self.text_editor.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
    def create_right_panel(self, parent):
        right_frame = ctk.CTkFrame(parent, width=350)
        right_frame.pack(side="right", fill="y", padx=(10, 0))
        right_frame.pack_propagate(False)
        
        # Quick Actions
        actions_frame = ctk.CTkFrame(right_frame)
        actions_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(actions_frame, text="Quick Actions", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5))
        
        ctk.CTkButton(actions_frame, text="Generate Single Video", command=self.generate_single_video, height=40).pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(actions_frame, text="Process All Scripts", command=self.process_all_scripts, height=40).pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(actions_frame, text="Generate Shorts", command=self.generate_shorts, height=40).pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(actions_frame, text="Generate Podcast", command=self.generate_podcast, height=40).pack(fill="x", padx=10, pady=5)
        
        # Settings
        settings_frame = ctk.CTkFrame(right_frame)
        settings_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        ctk.CTkLabel(settings_frame, text="Settings", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5))
        
        # Quality dropdown
        ctk.CTkLabel(settings_frame, text="Video Quality:").pack(anchor="w", padx=10)
        quality_combo = ctk.CTkComboBox(settings_frame, values=["ql (Low)", "qm (Medium)", "qh (High)"], variable=self.quality_var)
        quality_combo.pack(fill="x", padx=10, pady=5)
        
        # Voice settings
        ctk.CTkLabel(settings_frame, text="Voice:").pack(anchor="w", padx=10, pady=(10, 0))
        voice_combo = ctk.CTkComboBox(settings_frame, values=["en-GB-SoniaNeural", "en-US-AriaNeural", "en-AU-NatashaNeural"], variable=self.voice_var, command=self.on_voice_change)
        voice_combo.pack(fill="x", padx=10, pady=5)
        
        # NASA API Key
        ctk.CTkLabel(settings_frame, text="NASA API Key:").pack(anchor="w", padx=10, pady=(10, 0))
        ctk.CTkEntry(settings_frame, textvariable=self.nasa_api_key).pack(fill="x", padx=10, pady=5)
        
        # Show logs checkbox
        ctk.CTkCheckBox(settings_frame, text="Show Live Logs", variable=self.show_logs_var, command=self.toggle_logs).pack(anchor="w", padx=10, pady=10)
        
        # Progress section
        progress_frame = ctk.CTkFrame(right_frame)
        progress_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        ctk.CTkLabel(progress_frame, text="Progress", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5))
        
        self.status_label = ctk.CTkLabel(progress_frame, text="Ready")
        self.status_label.pack(pady=5)
        
        self.progress_bar = ctk.CTkProgressBar(progress_frame)
        self.progress_bar.pack(fill="x", padx=10, pady=5)
        self.progress_bar.set(0)
        
    def create_bottom_panel(self, parent):
        self.bottom_frame = ctk.CTkFrame(parent)
        # Initially hidden
        
        ctk.CTkLabel(self.bottom_frame, text="Live Logs", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5))
        
        self.log_text = tk.Text(self.bottom_frame, height=10, bg="#1e1e1e", fg="white")
        self.log_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
    def toggle_logs(self):
        if self.show_logs_var.get():
            self.bottom_frame.pack(fill="both", expand=True, pady=(10, 0))
        else:
            self.bottom_frame.pack_forget()
            
    def refresh_script_list(self):
        self.script_listbox.delete(0, tk.END)
        
        # Get all JSON files in scripts folder
        script_files = glob.glob(os.path.join("scripts", "*.json"))
        
        # Get processed files
        done_file = os.path.join("scripts", "done.txt")
        processed_files = []
        if os.path.exists(done_file):
            with open(done_file, 'r') as f:
                processed_files = [line.strip() for line in f.readlines()]
        
        for script_file in sorted(script_files):
            basename = os.path.basename(script_file)
            if basename in processed_files:
                display_name = f"✅ {basename}"
            else:
                display_name = f"⏳ {basename}"
            
            self.script_listbox.insert(tk.END, display_name)
            
    def on_script_select(self, event):
        selection = self.script_listbox.curselection()
        if selection:
            selected_text = self.script_listbox.get(selection[0])
            # Remove the emoji prefix
            filename = selected_text[2:].strip()
            script_path = os.path.join("scripts", filename)
            
            if os.path.exists(script_path):
                with open(script_path, 'r') as f:
                    content = f.read()
                
                self.text_editor.delete(1.0, tk.END)
                self.text_editor.insert(1.0, content)
                self.current_script = script_path
                
    def new_script(self):
        template = {
            "intro": "Welcome to this tutorial!",
            "sections": [
                {
                    "type": "code",
                    "code_string": "print('Hello World')",
                    "annotation": "Basic print statement",
                    "highlight_lines": [1],
                    "explanation": "This prints text to console"
                },
                {
                    "type": "quiz",
                    "question": "What does print() do?",
                    "answer": "Displays text output"
                }
            ],
            "outro": "Great job learning!"
        }
        
        self.text_editor.delete(1.0, tk.END)
        self.text_editor.insert(1.0, json.dumps(template, indent=2))
        self.current_script = None
        
    def open_script(self):
        filename = filedialog.askopenfilename(
            title="Open Script",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            with open(filename, 'r') as f:
                content = f.read()
            
            self.text_editor.delete(1.0, tk.END)
            self.text_editor.insert(1.0, content)
            self.current_script = filename
            
    def save_script(self):
        if self.current_script:
            with open(self.current_script, 'w') as f:
                f.write(self.text_editor.get(1.0, tk.END))
        else:
            filename = filedialog.asksaveasfilename(
                title="Save Script",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if filename:
                with open(filename, 'w') as f:
                    f.write(self.text_editor.get(1.0, tk.END))
                self.current_script = filename
        
        self.refresh_script_list()
        
    def delete_script(self):
        selection = self.script_listbox.curselection()
        if selection:
            selected_text = self.script_listbox.get(selection[0])
            filename = selected_text[2:].strip()
            script_path = os.path.join("scripts", filename)
            
            if messagebox.askyesno("Delete Script", f"Are you sure you want to delete {filename}?"):
                try:
                    os.remove(script_path)
                    self.refresh_script_list()
                    self.text_editor.delete(1.0, tk.END)
                except Exception as e:
                    messagebox.showerror("Error", f"Could not delete file: {e}")
                    
    def generate_single_video(self):
        if not self.current_script:
            messagebox.showwarning("No Script", "Please select a script first.")
            return
            
        def run_generation():
            self.update_status("Generating single video...")
            self.progress_bar.set(0.5)
            
            # Get quality setting
            quality = self.quality_var.get().split()[0]  # Extract 'ql', 'qm', or 'qh'
            
            # Copy script to test.json
            with open(self.current_script, 'r') as f:
                content = f.read()
            with open('test.json', 'w') as f:
                f.write(content)
                
            # Run manim
            timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            script_name = Path(self.current_script).stem
            video_filename = f"{script_name}.mp4"
            log_filename = os.path.join("logs", f"manim_log_{script_name}_{timestamp}.txt")
            
            command = ["manim", f"-{quality}", "main.py", "Video", "-o", video_filename]
            
            try:
                os.makedirs("logs", exist_ok=True)
                with open(log_filename, "w", encoding="utf-8") as log_file:
                    process = subprocess.run(command, stdout=log_file, stderr=subprocess.STDOUT, text=True)
                
                if process.returncode == 0:
                    self.update_status("Video generated successfully!")
                    messagebox.showinfo("Success", f"Video generated: {video_filename}")
                else:
                    self.update_status("Video generation failed!")
                    messagebox.showerror("Error", f"Video generation failed. Check log: {log_filename}")
            except Exception as e:
                self.update_status("Error occurred!")
                messagebox.showerror("Error", f"An error occurred: {e}")
            
            self.progress_bar.set(0)
            
        threading.Thread(target=run_generation, daemon=True).start()
        
    def process_all_scripts(self):
        def run_batch():
            self.update_status("Processing all scripts...")
            
            # Get quality setting
            quality = self.quality_var.get().split()[0]
            
            # Run wrapper.py with quality setting
            try:
                # Modify wrapper.py to use the selected quality
                self.modify_wrapper_quality(quality)
                
                process = subprocess.run(["uv", "run", "wrapper.py"], capture_output=True, text=True)
                
                if process.returncode == 0:
                    self.update_status("All scripts processed successfully!")
                    messagebox.showinfo("Success", "All scripts processed successfully!")
                else:
                    self.update_status("Batch processing failed!")
                    messagebox.showerror("Error", f"Batch processing failed: {process.stderr}")
                    
                self.refresh_script_list()
            except Exception as e:
                self.update_status("Error occurred!")
                messagebox.showerror("Error", f"An error occurred: {e}")
                
            self.progress_bar.set(0)
            
        threading.Thread(target=run_batch, daemon=True).start()
        
    def modify_wrapper_quality(self, quality):
        """Temporarily modify wrapper.py to use the selected quality"""
        # Read wrapper.py
        with open("wrapper.py", 'r') as f:
            content = f.read()
        
        # Replace the quality setting
        import re
        content = re.sub(r'"-ql"', f'"-{quality}"', content)
        
        # Write back
        with open("wrapper.py", 'w') as f:
            f.write(content)
            
    def generate_shorts(self):
        def run_shorts():
            self.update_status("Generating shorts...")
            self.progress_bar.set(0.5)
            
            try:
                process = subprocess.run(["python", "shorts.py"], capture_output=True, text=True)
                
                if process.returncode == 0:
                    self.update_status("Shorts generated successfully!")
                    messagebox.showinfo("Success", "Shorts generated successfully!")
                else:
                    self.update_status("Shorts generation failed!")
                    messagebox.showerror("Error", f"Shorts generation failed: {process.stderr}")
            except Exception as e:
                self.update_status("Error occurred!")
                messagebox.showerror("Error", f"An error occurred: {e}")
                
            self.progress_bar.set(0)
            
        threading.Thread(target=run_shorts, daemon=True).start()
        
    def generate_podcast(self):
        messagebox.showinfo("Coming Soon", "Podcast generation feature is coming soon!")
        
    def cleanup_logs(self):
        def run_cleanup():
            self.update_status("Cleaning up logs...")
            self.progress_bar.set(0.5)
            
            try:
                process = subprocess.run(["python", "cleanup.py"], capture_output=True, text=True)
                
                if process.returncode == 0:
                    self.update_status("Logs cleaned up successfully!")
                    messagebox.showinfo("Success", "Logs cleaned up successfully!")
                else:
                    self.update_status("Log cleanup failed!")
                    messagebox.showerror("Error", f"Log cleanup failed: {process.stderr}")
            except Exception as e:
                self.update_status("Error occurred!")
                messagebox.showerror("Error", f"An error occurred: {e}")
                
            self.progress_bar.set(0)
            
        threading.Thread(target=run_cleanup, daemon=True).start()
        
    def show_help(self):
        help_text = """
Manimations GUI Help

Quick Actions:
• Generate Single Video: Creates a video from the currently selected script
• Process All Scripts: Batch processes all unprocessed scripts in the scripts folder
• Generate Shorts: Creates short videos from quotes.json
• Generate Podcast: (Coming Soon) Creates podcast from scripts

Settings:
• Video Quality: Choose between Low (ql), Medium (qm), or High (qh)
• Voice: Select the TTS voice for narration
• NASA API Key: Required for shorts generation
• Show Live Logs: Toggle the log display panel

Script Explorer:
• ✅ = Processed script
• ⏳ = Pending script
• Click on a script to edit it

For more information, check the README.md file.
        """
        
        help_window = ctk.CTkToplevel(self.root)
        help_window.title("Help")
        help_window.geometry("600x500")
        
        text_widget = tk.Text(help_window, wrap=tk.WORD, bg="#2b2b2b", fg="white")
        text_widget.pack(fill="both", expand=True, padx=20, pady=20)
        text_widget.insert(1.0, help_text)
        text_widget.config(state=tk.DISABLED)
        
    def update_status(self, status):
        self.status_label.configure(text=status)
        if self.show_logs_var.get():
            self.log_text.insert(tk.END, f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {status}\n")
            self.log_text.see(tk.END)
        
    def run(self):
        self.root.mainloop()
    
    def on_voice_change(self, choice):
        """Save the selected voice to .voice file"""
        try:
            with open('.voice', 'w') as f:
                f.write(choice)
            self.update_status(f"Voice changed to: {choice}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save voice setting: {e}")

    def load_voice_setting(self):
        """Load voice setting from .voice file if it exists"""
        try:
            if os.path.exists('.voice'):
                with open('.voice', 'r') as f:
                    voice = f.read().strip()
                    self.voice_var.set(voice)
        except Exception:
            pass  # Use default if file doesn't exist or can't be read

if __name__ == "__main__":
    # Create necessary directories
    os.makedirs("scripts", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    os.makedirs("generated_shorts", exist_ok=True)
    
    app = ManimationsGUI()
    app.run()