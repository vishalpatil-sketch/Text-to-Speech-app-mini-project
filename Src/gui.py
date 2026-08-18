import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from src.tts_engine import TTSEngine


class TTSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text-to-Speech Desktop Application")
        self.root.geometry("580x520")
        self.root.resizable(False, False)

        self.engine = TTSEngine()
        self._build_ui()

    def _build_ui(self):
        # Header
        header = tk.Label(self.root, text="Text-to-Speech Converter", font=("Arial", 16, "bold"))
        header.pack(pady=10)

        # Input Field
        input_frame = tk.LabelFrame(self.root, text=" Input Text ", padx=10, pady=5)
        input_frame.pack(fill="x", padx=15, pady=5)
        
        self.text_area = tk.Text(input_frame, height=7, width=65, font=("Arial", 10))
        self.text_area.pack()

        # Engine & Controls Selection
        controls_frame = tk.LabelFrame(self.root, text=" Voice Settings ", padx=10, pady=10)
        controls_frame.pack(fill="x", padx=15, pady=5)

        # Engine Mode (Offline vs Online)
        tk.Label(controls_frame, text="Engine Mode:").grid(row=0, column=0, sticky="w")
        self.engine_var = tk.StringVar(value="pyttsx3 (Offline)")
        engine_combo = ttk.Combobox(controls_frame, textvariable=self.engine_var, values=["pyttsx3 (Offline)", "gTTS (Online)"], state="readonly", width=25)
        engine_combo.grid(row=0, column=1, padx=5, pady=5)

        # Voice Selector
        tk.Label(controls_frame, text="Voice Type:").grid(row=1, column=0, sticky="w")
        self.voice_combo = ttk.Combobox(controls_frame, values=self.engine.get_available_voices(), state="readonly", width=25)
        if self.engine.get_available_voices():
            self.voice_combo.current(0)
        self.voice_combo.grid(row=1, column=1, padx=5, pady=5)

        # Speed Slider
        tk.Label(controls_frame, text="Speed (WPM):").grid(row=2, column=0, sticky="w")
        self.speed_slider = tk.Scale(controls_frame, from_=100, to=300, orient="horizontal", length=200)
        self.speed_slider.set(200)
        self.speed_slider.grid(row=2, column=1, padx=5, pady=5)

        # Volume Slider
        tk.Label(controls_frame, text="Volume:").grid(row=3, column=0, sticky="w")
        self.volume_slider = tk.Scale(controls_frame, from_=0.0, to=1.0, resolution=0.1, orient="horizontal", length=200)
        self.volume_slider.set(1.0)
        self.volume_slider.grid(row=3, column=1, padx=5, pady=5)

        # Action Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="▶ Play", command=self.handle_play, bg="#4CAF50", fg="white", width=9, font=("Arial", 9, "bold")).grid(row=0, column=0, padx=4)
        tk.Button(btn_frame, text="⏸ Pause", command=self.engine.pause_audio, bg="#FF9800", fg="white", width=9, font=("Arial", 9, "bold")).grid(row=0, column=1, padx=4)
        tk.Button(btn_frame, text="⏯ Resume", command=self.engine.resume_audio, bg="#2196F3", fg="white", width=9, font=("Arial", 9, "bold")).grid(row=0, column=2, padx=4)
        tk.Button(btn_frame, text="⏹ Stop", command=self.engine.stop_audio, bg="#F44336", fg="white", width=9, font=("Arial", 9, "bold")).grid(row=0, column=3, padx=4)
        tk.Button(btn_frame, text="💾 Save", command=self.handle_save, bg="#9C27B0", fg="white", width=9, font=("Arial", 9, "bold")).grid(row=0, column=4, padx=4)

    def get_text_input(self):
        text = self.text_area.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter text into the field.")
            return None
        return text

    def handle_play(self):
        text = self.get_text_input()
        if not text:
            return

        mode = self.engine_var.get()
        if "Offline" in mode:
            self.engine.speak_offline(
                text=text,
                voice_index=self.voice_combo.current(),
                rate=self.speed_slider.get(),
                volume=self.volume_slider.get()
            )
        else:
            self.engine.speak_online(text=text)

    def handle_save(self):
        text = self.get_text_input()
        if not text:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".mp3",
            filetypes=[("MP3 File", "*.mp3"), ("WAV File", "*.wav")]
        )
        if file_path:
            mode = "offline" if "Offline" in self.engine_var.get() else "online"
            self.engine.save_audio(
                text=text,
                file_path=file_path,
                engine_type=mode,
                voice_index=self.voice_combo.current(),
                rate=self.speed_slider.get(),
                volume=self.volume_slider.get()
            )
            messagebox.showinfo("Success", f"Audio file saved successfully:\n{file_path}")
