import tkinter as tk
from src.gui import TTSApp

def main():
    root = tk.Tk()
    app = TTSApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
