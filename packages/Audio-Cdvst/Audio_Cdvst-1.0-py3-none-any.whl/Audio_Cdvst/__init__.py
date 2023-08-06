import asyncio
import logging
import os
import tempfile
from contextlib import contextmanager
from typing import Dict, Optional, Any, Type, TypeVar
import speech_recognition as sr
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
from collections import Counter
import re
from gtts import gTTS
from playsound import playsound
from Data_Cdvst import Database as DatabaseManager
import openai
from google.cloud import storage
import mega
import mega as Mega
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fügen Sie hier Ihren OpenAI API-Schlüssel ein
openai.api_key = "your_openai_api_key"

# Fügen Sie hier Ihren Google Cloud Storage API-Schlüssel ein
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/google-cloud-storage-key.json"

T = TypeVar("T", bound="Singleton")

class Singleton(type):
    _instances: Dict[Type[T], T] = {}

    def __call__(cls, *args, **kwargs) -> T:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class SpeechProcessingError(Exception):
    ...

class SentimentAnalyzer:
    def __init__(self):
        nltk.download("vader_lexicon", quiet=True)
        self.sia = SentimentIntensityAnalyzer()

    def analyze_sentiment(self, text):
        sentiment_scores = self.sia.polarity_scores(text)
        return sentiment_scores

class WordCloudVisualizer:
    def visualize_word_cloud(self, text):
        words = re.findall(r'\w+', text.lower())
        word_counts = Counter(words)
        labels, values = zip(*word_counts.items())

        plt.figure(figsize=(15, 10))
        plt.bar(labels, values)
        plt.xticks(rotation=90)
        plt.xlabel("Wörter")
        plt.ylabel("Häufigkeit")
        plt.title("Wort-Häufigkeitsdiagramm")
        plt.show()

class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    async def recognize_speech_async(self):
        loop = asyncio.get_event_loop()
        recognized_text = await loop.run_in_executor(None, self.recognize_speech)
        return recognized_text

    def recognize_speech(self):
        with sr.Microphone() as source:
            print("Sprechen Sie jetzt...")
            audio_data = self.recognizer.listen(source)
            try:
                recognized_text = self.recognizer.recognize_google(audio_data, language="de-DE")
                return recognized_text, audio_data
            except sr.UnknownValueError:
                print("Spracherkennung konnte nicht verstanden werden.")
            except sr.RequestError as e:
                print(f"Spracherkennungsdienstfehler: {e}")

class TextToSpeech:
    def __init__(self, lang="de", voice="default"):
        self.lang = lang
        self.voice = voice

    def synthesize(self, text):
        try:
            tts = gTTS(text, lang=self.lang, tld="co.uk", slow=False)
            with tempfile.NamedTemporaryFile(delete=True) as fp:
                tts.save(fp.name)
                playsound(fp.name)
        except Exception as e:
            logger.error(f"Text-to-Speech-Fehler: {e}")

class CloudStorageUploader:
    def upload_to_google_cloud(self, file_path, bucket_name):
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(os.path.basename(file_path))
        blob.upload_from_filename(file_path)
        logger.info(f"File {file_path} uploaded to {bucket_name}.")

    def upload_to_onedrive(self, file_path):
        # Implementierung des OneDrive-Uploads
        pass

    def upload_to_mega(self, file_path, email, password):
        mega_instance = Mega()
        mega = mega_instance.login(email, password)
        folder = mega.find('MyAppData')
        if not folder:
            folder = mega.create_folder('MyAppData')
        file = mega.upload(file_path, folder[0])
        logger.info(f"File {file_path} uploaded to Mega.")

class SpeechProcessing(metaclass=Singleton):
    def __init__(self, lang="de", voice="default"):
        self.speech_recognizer = SpeechRecognizer()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.word_cloud_visualizer = WordCloudVisualizer()
        self.text_to_speech = TextToSpeech(lang=lang, voice=voice)
        self.cloud_storage_uploader = CloudStorageUploader()

    def process_audio(self, visualize=True, speak=True, save_to_cloud=None, cloud_credentials: Optional[Dict[str, Any]] = None, output_format="wav"):
        try:
            # Schritt 1: Spracherkennung
            recognized_text, audio_data = asyncio.run(self.speech_recognizer.recognize_speech_async())
            print(f"Erkannter Text: {recognized_text}")

            # Schritt 2: Sentiment-Analyse
            sentiment_scores = self.sentiment_analyzer.analyze_sentiment(recognized_text)
            print(f"Sentiment-Scores: {sentiment_scores}")

            # Schritt 3: Wortwolke anzeigen (optional)
            if visualize:
                self.word_cloud_visualizer.visualize_word_cloud(recognized_text)

            # Schritt 4: Text in gesprochene Sprache umwandeln und abspielen (optional)
            if speak:
                self.text_to_speech.synthesize(recognized_text)

            # Schritt 5: Datei in Cloud-Speicher hochladen (optional)
            if save_to_cloud:
                with tempfile.NamedTemporaryFile(suffix=f".{output_format}", delete=True) as fp:
                    if output_format == "wav":
                        audio_data.export(fp.name, format="wav")
                    elif output_format == "mp3":
                        audio_data.export(fp.name, format="mp3")
                    else:
                        raise SpeechProcessingError(f"Unsupported output_format: {output_format}")

                    if save_to_cloud == "google_cloud":
                        if cloud_credentials is None or 'bucket_name' not in cloud_credentials:
                            raise SpeechProcessingError("Google Cloud bucket_name is missing in cloud_credentials")
                        bucket_name = cloud_credentials.get("bucket_name")
                        self.cloud_storage_uploader.upload_to_google_cloud(fp.name, bucket_name)
                    elif save_to_cloud == "onedrive":
                        pass  # Implementierung für OneDrive
                    elif save_to_cloud == "mega":
                        if cloud_credentials is None or 'email' not in cloud_credentials or 'password' not in cloud_credentials:
                            raise SpeechProcessingError("Mega email and password are missing in cloud_credentials")
                        email = cloud_credentials.get("email")
                        password = cloud_credentials.get("password")
                        self.cloud_storage_uploader.upload_to_mega(fp.name, email, password)

        except SpeechProcessingError as e:
            logger.error(f"SpeechProcessingError: {e}")
        except Exception as e:
            logger.error(f"Unerwarteter Fehler: {e}")

# Hier können Sie die erweiterten Funktionen testen
if __name__ == "__main__":
    speech_processing = SpeechProcessing()
    speech_processing.process_audio(visualize=True, speak=True, save_to_cloud="google_cloud",
                                     cloud_credentials={"bucket_name": "your_bucket_name"},
                                     output_format="wav")
