import os
import threading
import pyttsx3
from gtts import gTTS
import pygame


class TTSEngine:
    def __init__(self):
        # Initialize pyttsx3
        self.pyttsx_engine = pyttsx3.init()
        self.voices = self.pyttsx_engine.getProperty('voices')
        
        # Initialize Pygame Mixer for audio playback controls (pause/stop)
        pygame.mixer.init()
        self.current_audio_file = "temp_speech.mp3"
        self.is_paused = False

    def get_available_voices(self):
        """Returns list of available system voice names."""
        return [voice.name for voice in self.voices]

    def speak_offline(self, text, voice_index=0, rate=200, volume=1.0):
        """Offline TTS using pyttsx3."""
        def _run():
            self.pyttsx_engine.setProperty('rate', rate)
            self.pyttsx_engine.setProperty('volume', volume)
            if 0 <= voice_index < len(self.voices):
                self.pyttsx_engine.setProperty('voice', self.voices[voice_index].id)
            self.pyttsx_engine.say(text)
            self.pyttsx_engine.runAndWait()

        threading.Thread(target=_run, daemon=True).start()

    def speak_online(self, text, lang='en'):
        """Online TTS using gTTS and Pygame playback."""
        def _run():
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(self.current_audio_file)
            pygame.mixer.music.load(self.current_audio_file)
            pygame.mixer.music.play()

        threading.Thread(target=_run, daemon=True).start()

    def pause_audio(self):
        if pygame.mixer.music.get_busy() and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True

    def resume_audio(self):
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False

    def stop_audio(self):
        if pygame.mixer.music.get_busy() or self.is_paused:
            pygame.mixer.music.stop()
            self.is_paused = False
        try:
            self.pyttsx_engine.stop()
        except Exception:
            pass

    def save_audio(self, text, file_path, engine_type='offline', voice_index=0, rate=200, volume=1.0):
        """Saves text to .mp3 or .wav file."""
        if engine_type == 'offline':
            self.pyttsx_engine.setProperty('rate', rate)
            self.pyttsx_engine.setProperty('volume', volume)
            if 0 <= voice_index < len(self.voices):
                self.pyttsx_engine.setProperty('voice', self.voices[voice_index].id)
            self.pyttsx_engine.save_to_file(text, file_path)
            self.pyttsx_engine.runAndWait()
        else:
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(file_path)
