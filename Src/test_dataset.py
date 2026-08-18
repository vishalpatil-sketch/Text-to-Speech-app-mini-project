import pandas as pd
from src.tts_engine import TTSEngine

def test_kaggle_dataset(csv_path="unigram_freq.csv", sample_count=10):
    """
    Tests text-to-speech rendering on sample words from Kaggle dataset:
    https://www.kaggle.com/datasets/rtatman/english-word-frequency
    """
    try:
        df = pd.read_csv(csv_path)
        sample_words = df['word'].head(sample_count).dropna().tolist()
        sample_text = " ".join(sample_words)
        
        print(f"[Dataset Test] Playing {sample_count} sample words from Kaggle dataset...")
        print(f"Sample String: {sample_text}")
        
        engine = TTSEngine()
        engine.speak_offline(sample_text, rate=180)
    except FileNotFoundError:
        print("[Dataset Test] 'unigram_freq.csv' not found locally. Skipping dataset benchmark test.")

if __name__ == "__main__":
    test_kaggle_dataset()
