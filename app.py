import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pyttsx3


class TextToSpeechApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text-to-Speech Desktop App")
        self.root.geometry("600x520")
        self.root.minsize(500, 450)

        # Initialize pyttsx3 engine
        self.engine = pyttsx3.init()
        self.is_paused = False

        # Load available voices
        self.voices = self.engine.getProperty("voices")

        # Build UI
        self._create_widgets()

    def _create_widgets(self):
        # Configure layout weights for responsiveness
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        # Header Frame
        header_frame = ttk.Frame(self.root, padding=10)
        header_frame.grid(row=0, column=0, sticky="ew")

        ttk.Label(
            header_frame,
            text="Text-to-Speech Converter",
            font=("Helvetica", 16, "bold"),
        ).pack(anchor="w")

        # Input Text Area
        text_frame = ttk.Frame(self.root, padding=10)
        text_frame.grid(row=1, column=0, sticky="nsew")
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)

        self.text_input = tk.Text(text_frame, wrap="word", font=("Arial", 11))
        self.text_input.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(
            text_frame, orient="vertical", command=self.text_input.yview
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.text_input["yscrollcommand"] = scrollbar.set

        # Controls & Settings Frame
        controls_frame = ttk.LabelFrame(
            self.root, text=" Settings ", padding=10
        )
        controls_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        controls_frame.columnconfigure(1, weight=1)
        controls_frame.columnconfigure(3, weight=1)

        # Voice Selection
        ttk.Label(controls_frame, text="Voice:").grid(
            row=0, column=0, sticky="w", padx=5, pady=5
        )
        self.voice_var = tk.StringVar()
        voice_names = [
            f"{v.name} ({v.languages[0] if v.languages else 'Default'})"
            for v in self.voices
        ]
        self.voice_combobox = ttk.Combobox(
            controls_frame,
            textvariable=self.voice_var,
            values=voice_names,
            state="readonly",
        )
        if voice_names:
            self.voice_combobox.current(0)
        self.voice_combobox.grid(
            row=0, column=1, columnspan=3, sticky="ew", padx=5, pady=5
        )

        # Rate / Speed Slider
        ttk.Label(controls_frame, text="Speed:").grid(
            row=1, column=0, sticky="w", padx=5, pady=5
        )
        self.rate_slider = ttk.Scale(
            controls_frame,
            from_=50,
            to=300,
            orient="horizontal",
            value=self.engine.getProperty("rate"),
        )
        self.rate_slider.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        # Volume Slider
        ttk.Label(controls_frame, text="Volume:").grid(
            row=1, column=2, sticky="w", padx=5, pady=5
        )
        self.volume_slider = ttk.Scale(
            controls_frame,
            from_=0.0,
            to=1.0,
            orient="horizontal",
            value=self.engine.getProperty("volume"),
        )
        self.volume_slider.grid(row=1, column=3, sticky="ew", padx=5, pady=5)

        # Action Buttons Frame
        button_frame = ttk.Frame(self.root, padding=10)
        button_frame.grid(row=3, column=0, sticky="ew")

        ttk.Button(button_frame, text="Play", command=self.play_audio).pack(
            side="left", padx=5
        )
        ttk.Button(button_frame, text="Stop", command=self.stop_audio).pack(
            side="left", padx=5
        )
        ttk.Button(
            button_frame, text="Save Audio", command=self.save_audio
        ).pack(side="right", padx=5)

    def _apply_settings(self):
        """Apply user-selected voice, rate, and volume settings."""
        selected_index = self.voice_combobox.current()
        if selected_index >= 0 and selected_index < len(self.voices):
            self.engine.setProperty("voice", self.voices[selected_index].id)

        self.engine.setProperty("rate", int(self.rate_slider.get()))
        self.engine.setProperty("volume", float(self.volume_slider.get()))

    def play_audio(self):
        """Convert input text to speech asynchronously to keep UI responsive."""
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter text to speak.")
            return

        def run_speech():
            self._apply_settings()
            self.engine.say(text)
            self.engine.runAndWait()

        # Run in a separate thread so UI does not freeze
        threading.Thread(target=run_speech, daemon=True).start()

    def stop_audio(self):
        """Stop current speech playback."""
        if self.engine.isBusy():
            self.engine.stop()

    def save_audio(self):
        """Export speech input to an MP3 / WAV file."""
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter text to save.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".wav",
            filetypes=[("WAV Audio", "*.wav"), ("MP3 Audio", "*.mp3")],
            title="Save Audio File",
        )

        if file_path:

            def save_speech():
                self._apply_settings()
                self.engine.save_to_file(text, file_path)
                self.engine.runAndWait()
                messagebox.showinfo(
                    "Success", f"Audio saved successfully to:\n{file_path}"
                )

            threading.Thread(target=save_speech, daemon=True).start()


if __name__ == "__main__":
    root = tk.Tk()
    app = TextToSpeechApp(root)
    root.mainloop()
