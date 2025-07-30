import tkinter as tk
from tkinter import ttk, scrolledtext, font
import os
import threading
import queue
import webbrowser
import re
from persona_refactored import ConversationalAI
import vlc

class App:
    """
    The main GUI application window.
    """
    def __init__(self, root):
        # --- Brand Colors ---
        self.KOCHO_EBONY = "#001619"
        self.KOCHO_LIME = "#19E738"
        self.KOCHO_OATMEAL = "#EBE9E2"
        self.KOCHO_WHITE = "#FFFFFF"
        self.KOCHO_DARK_TEXT = "#333333"

        self.root = root
        self.root.title("Kocho Conversational AI")
        self.root.geometry("1200x800")
        self.root.configure(bg=self.KOCHO_OATMEAL)

        self.update_queue = queue.Queue()
        self.ai_instance = ConversationalAI(self.update_queue)
        
        # --- VLC Player Setup ---
        self.vlc_instance = vlc.Instance()
        self.media_player = self.vlc_instance.media_player_new()
        # --- Hidden Sound Player Setup ---
        self.sound_player = self.vlc_instance.media_player_new()

        # --- Script ---
        self.script = []
        self.script_line_index = 0
        self.script_job = None

        # --- Create subdirectories ---
        for dir_name in ["videos", "personas", "scripts", "assets"]:
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)

        # --- Style Configuration ---
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background=self.KOCHO_OATMEAL)
        style.configure("TLabel", background=self.KOCHO_OATMEAL, foreground=self.KOCHO_DARK_TEXT, font=("Helvetica", 10))
        style.configure("Header.TLabel", font=("Helvetica", 16, "bold"), foreground=self.KOCHO_EBONY)
        style.configure("SummaryHeader.TLabel", font=("Helvetica", 12, "bold"), foreground=self.KOCHO_EBONY)
        style.configure("SummaryValue.TLabel", font=("Helvetica", 10), wraplength=350)
        style.configure("Start.TButton", font=("Helvetica", 10, "bold"), background=self.KOCHO_EBONY, foreground=self.KOCHO_WHITE)
        style.configure("Stop.TButton", font=("Helvetica", 10, "bold"), background=self.KOCHO_LIME, foreground=self.KOCHO_EBONY)
        style.configure("Video.TButton", font=("Helvetica", 10, "bold"))

        # --- Main Layout ---
        paned_window = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True)

        left_panel = ttk.Frame(paned_window, padding="15")
        paned_window.add(left_panel, weight=1)
        self.right_panel = ttk.Frame(paned_window, padding="15")
        paned_window.add(self.right_panel, weight=2)

        # --- Header ---
        header_frame = ttk.Frame(left_panel)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(header_frame, text="Kocho", font=("Helvetica", 24, "bold"), foreground=self.KOCHO_EBONY).pack()
        ttk.Label(header_frame, text="Become greater.", font=("Helvetica", 10, "italic"), foreground=self.KOCHO_EBONY).pack()
        ttk.Separator(left_panel, orient='horizontal').pack(fill='x', padx=20, pady=10)

        # --- Persona Selection ---
        persona_frame = ttk.Frame(left_panel)
        persona_frame.pack(fill=tk.X, pady=10)
        persona_frame.columnconfigure(1, weight=1)
        ttk.Label(persona_frame, text="Select Persona", style="Header.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))
        self.persona_listbox = tk.Listbox(persona_frame, height=5, exportselection=False, bg=self.KOCHO_WHITE, fg=self.KOCHO_DARK_TEXT, selectbackground=self.KOCHO_EBONY, selectforeground=self.KOCHO_WHITE, borderwidth=1, relief="solid", font=("Helvetica", 10))
        self.persona_listbox.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        self.persona_listbox.bind('<<ListboxSelect>>', self.on_persona_select)
        
        # --- Control Buttons ---
        self.start_button = ttk.Button(persona_frame, text="Start Session", command=self.start_conversation, style="Start.TButton")
        self.start_button.grid(row=2, column=0, sticky="ew", padx=(0, 5))
        self.stop_button = ttk.Button(persona_frame, text="Stop Session", command=self.stop_conversation, state=tk.DISABLED, style="Stop.TButton")
        self.stop_button.grid(row=2, column=1, sticky="ew", padx=(5, 0))

        # --- Conversation Log ---
        log_frame = ttk.Frame(left_panel)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        ttk.Label(log_frame, text="Conversation Log", style="Header.TLabel").pack(anchor="w", pady=(0, 10))
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, state=tk.DISABLED, font=("Helvetica", 10), bg=self.KOCHO_WHITE, fg=self.KOCHO_DARK_TEXT, borderwidth=1, relief="solid")
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # --- Status Bar & Footer ---
        footer_frame = ttk.Frame(left_panel)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10,0))
        self.status_var = tk.StringVar(value="Select a persona and start a session.")
        status_bar = ttk.Label(footer_frame, textvariable=self.status_var, relief=tk.FLAT, anchor=tk.W, padding=10, background=self.KOCHO_EBONY, foreground=self.KOCHO_WHITE)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        link_font = font.Font(family="Helvetica", size=9, underline=True)
        link_label = ttk.Label(footer_frame, text="www.kocho.co.uk", foreground=self.KOCHO_EBONY, font=link_font, cursor="hand2")
        link_label.pack(side=tk.BOTTOM, pady=5)
        link_label.bind("<Button-1>", lambda e: self.open_link("https://www.kocho.co.uk"))
        
        # --- Build Right Panel Widgets and Bind Keys ---
        self.build_right_panel_widgets()
        self.bind_keys()
        
        # --- Final Setup ---
        self.populate_personas()
        self.process_queue()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def bind_keys(self):
        """Binds the hidden key features."""
        self.root.bind("<F9>", self.play_intro_sound)
        self.root.bind("<F10>", self.stop_intro_sound)

    def play_intro_sound(self, event=None):
        """Plays the intro.mp3 sound file."""
        sound_path = os.path.join("assets", "HelpDesk-Demo.mp3")
        if os.path.exists(sound_path):
            try:
                media = self.vlc_instance.media_new(sound_path)
                self.sound_player.set_media(media)
                self.sound_player.play()
                print("Playing intro sound...") # Log to console, not GUI
            except Exception as e:
                print(f"Error playing sound: {e}")
        else:
            print(f"Sound file not found: {sound_path}")

    def stop_intro_sound(self, event=None):
        """Stops the intro sound."""
        if self.sound_player.is_playing():
            self.sound_player.stop()
            print("Intro sound stopped.")

    def build_right_panel_widgets(self):
        # Video Player Frame
        self.video_frame = ttk.Frame(self.right_panel)
        ttk.Label(self.video_frame, text="Video Demonstration", style="Header.TLabel").pack(anchor="w", pady=(0, 10))
        self.video_canvas = tk.Canvas(self.video_frame, bg="black")
        self.video_canvas.pack(fill=tk.BOTH, expand=True)
        self.media_player.set_hwnd(self.video_canvas.winfo_id())
        
        video_controls_frame = ttk.Frame(self.video_frame)
        video_controls_frame.pack(pady=10)
        self.play_btn = ttk.Button(video_controls_frame, text="Play", command=self.play_video, style="Video.TButton", state=tk.DISABLED)
        self.play_btn.pack(side=tk.LEFT, padx=5)
        self.pause_btn = ttk.Button(video_controls_frame, text="Pause", command=self.pause_video, style="Video.TButton", state=tk.DISABLED)
        self.pause_btn.pack(side=tk.LEFT, padx=5)
        self.stop_video_btn = ttk.Button(video_controls_frame, text="Stop", command=self.stop_video, style="Video.TButton", state=tk.DISABLED)
        self.stop_video_btn.pack(side=tk.LEFT, padx=5)
        
        # Persona Summary Frame
        self.summary_frame = ttk.Frame(self.right_panel)
        ttk.Label(self.summary_frame, text="Persona Summary", style="Header.TLabel").pack(anchor="w", pady=(0, 20))
        self.summary_vars = {}
        fields = ["Attacker", "Role", "Target", "Pretext", "Primary Goal"]
        for field in fields:
            ttk.Label(self.summary_frame, text=f"{field}:", style="SummaryHeader.TLabel").pack(anchor="w", pady=(10, 2))
            self.summary_vars[field] = tk.StringVar(value="-")
            ttk.Label(self.summary_frame, textvariable=self.summary_vars[field], style="SummaryValue.TLabel").pack(anchor="w")

    def on_persona_select(self, event=None):
        selection_indices = self.persona_listbox.curselection()
        if not selection_indices: return
        persona_name = self.persona_listbox.get(selection_indices[0])
        
        self.video_frame.pack_forget()
        self.summary_frame.pack_forget()
        self.stop_video()
        self.load_script(persona_name)

        video_path = os.path.join("videos", f"{persona_name}.mp4")
        
        if os.path.exists(video_path):
            self.video_frame.pack(fill=tk.BOTH, expand=True)
            self.load_video(video_path)
            self.start_button.config(state=tk.DISABLED)
        else:
            self.summary_frame.pack(fill=tk.BOTH, expand=True)
            self.update_persona_summary(persona_name)
            self.start_button.config(state=tk.NORMAL)

    def load_script(self, persona_name):
        self.script = []
        self.script_line_index = 0
        script_path = os.path.join("scripts", f"{persona_name}-script.txt")
        if os.path.exists(script_path):
            with open(script_path, 'r', encoding='utf-8') as f:
                self.script = [line.strip() for line in f if line.strip()]
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)

    def update_persona_summary(self, persona_name):
        persona_file = os.path.join("personas", f"{persona_name}.txt")
        if not os.path.exists(persona_file):
            for var in self.summary_vars.values(): var.set("-")
            return
        with open(persona_file, 'r', encoding='utf-8') as f: content = f.read()
        def parse_field(key):
            match = re.search(f"^{key}:(.*?)$", content, re.MULTILINE | re.IGNORECASE)
            return match.group(1).strip() if match else "-"
        self.summary_vars["Attacker"].set(parse_field("Your Name"))
        self.summary_vars["Role"].set(parse_field("Your Role"))
        self.summary_vars["Target"].set(parse_field("Your Target"))
        self.summary_vars["Pretext"].set(parse_field("The Pretext"))
        goal_match = re.search(r'# Goals\s*\n(.*?)(?=\n#|$)', content, re.DOTALL | re.IGNORECASE)
        goal_text = goal_match.group(1).strip().replace('\n', ' ') if goal_match else "-"
        self.summary_vars["Primary Goal"].set(goal_text)

    def load_video(self, file_path):
        try:
            media = self.vlc_instance.media_new(file_path)
            self.media_player.set_media(media)
            self.play_btn.config(state=tk.NORMAL)
            self.pause_btn.config(state=tk.NORMAL)
            self.stop_video_btn.config(state=tk.NORMAL)
            self.status_var.set(f"Loaded: {os.path.basename(file_path)}")
        except Exception as e:
            self.log_message(f"Error loading video: {e}")
            self.play_btn.config(state=tk.DISABLED)
            self.pause_btn.config(state=tk.DISABLED)
            self.stop_video_btn.config(state=tk.DISABLED)

    def play_video(self):
        if self.media_player.get_media() and not self.media_player.is_playing():
            if self.media_player.get_state() != vlc.State.Paused:
                self.stop_video()
                self.script_line_index = 0
                self.log_text.config(state=tk.NORMAL)
                self.log_text.delete(1.0, tk.END)
                self.log_text.config(state=tk.DISABLED)
            self.media_player.play()
            self.status_var.set("Playing video demo...")
            self.run_scripted_log()

    def run_scripted_log(self):
        if self.script_job:
            self.root.after_cancel(self.script_job)
        if self.script_line_index < len(self.script) and self.media_player.is_playing():
            line = self.script[self.script_line_index]
            self.log_text.config(state=tk.NORMAL)
            self.log_text.insert(tk.END, line + "\n")
            self.log_text.config(state=tk.DISABLED)
            self.log_text.see(tk.END)
            self.script_line_index += 1
            self.script_job = self.root.after(4000, self.run_scripted_log)

    def pause_video(self):
        if self.media_player.is_playing():
            self.media_player.pause()
            if self.script_job:
                self.root.after_cancel(self.script_job)
            self.status_var.set("Video paused.")

    def stop_video(self):
        if self.media_player.is_playing() or self.media_player.get_state() == vlc.State.Paused:
            self.media_player.stop()
            if self.script_job:
                self.root.after_cancel(self.script_job)
                self.script_job = None
            self.status_var.set("Video stopped.")

    def open_link(self, url):
        webbrowser.open_new(url)

    def populate_personas(self):
        persona_dir = "personas"
        personas = [f.replace(".txt", "") for f in os.listdir(persona_dir) if f.endswith(".txt")]
        if not personas:
            self.log_message(f"No personas found in '{persona_dir}' directory.")
            return
        for p in sorted(personas):
            self.persona_listbox.insert(tk.END, p)
        self.persona_listbox.selection_set(0)
        self.on_persona_select()

    def start_conversation(self):
        selection = self.persona_listbox.curselection()
        if not selection:
            self.status_var.set("Please select a persona first.")
            return
        persona_name = self.persona_listbox.get(selection[0])
        threading.Thread(target=self._start_and_run_loop, args=(persona_name,), daemon=True).start()

    def _start_and_run_loop(self, persona_name):
        self.ai_instance.start_session(persona_name)
        if self.ai_instance.is_running:
            self.ai_instance.run_conversation_loop()

    def stop_conversation(self):
        self.ai_instance.stop_session()

    def process_queue(self):
        try:
            while True:
                msg = self.update_queue.get_nowait()
                if msg["type"] == "log" and not self.script:
                    self.log_message(msg["value"])
                elif msg["type"] == "status":
                    self.status_var.set(msg["value"])
                elif msg["type"] == "session_started":
                    self.start_button.config(state=tk.DISABLED)
                    self.stop_button.config(state=tk.NORMAL)
                    self.persona_listbox.config(state=tk.DISABLED)
                elif msg["type"] == "session_stopped":
                    self.start_button.config(state=tk.NORMAL)
                    self.stop_button.config(state=tk.DISABLED)
                    self.persona_listbox.config(state=tk.NORMAL)
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.process_queue)

    def log_message(self, message):
        if not self.script:
            self.log_text.config(state=tk.NORMAL)
            self.log_text.insert(tk.END, message + "\n")
            self.log_text.config(state=tk.DISABLED)
            self.log_text.see(tk.END)

    def on_closing(self):
        self.stop_video()
        self.media_player.release()
        self.sound_player.release()
        self.stop_conversation()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
