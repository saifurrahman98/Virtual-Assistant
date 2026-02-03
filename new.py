import os
import numpy as np
import speech_recognition as sr
import pyttsx3
import requests
import webbrowser
from gtts import gTTS
import pygame
import soundfile as sf
from python_speech_features import mfcc

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = 'a1d9a008ac2549d5b91ad89c5a93912b'
REFERENCE_VOICE_FOLDER = "/Users/saifurrahman/Desktop/Virtual_Assistant_project/voices"

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    os.remove("temp.mp3")

def load_audio(file_path):
    """Load audio file using soundfile."""
    audio, sample_rate = sf.read(file_path)
    return audio, sample_rate

def compute_mfcc(audio, sample_rate, fixed_length=2.0):
    """Compute MFCC features for fixed-length audio."""
    target_length = int(fixed_length * sample_rate)
    if len(audio) > target_length:
        audio = audio[:target_length]
    else:
        padding = target_length - len(audio)
        audio = np.pad(audio, (0, padding), mode='constant')
    mfcc_features = mfcc(audio, samplerate=sample_rate, numcep=20, nfft=2048)
    return mfcc_features

def create_voice_profile(folder_path, fixed_length=2.0):
    """Generate a voice profile by averaging MFCC features from all reference audio files."""
    all_mfcc = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.wav'):
            file_path = os.path.join(folder_path, file_name)
            audio, sample_rate = load_audio(file_path)
            mfcc_features = compute_mfcc(audio, sample_rate, fixed_length)
            all_mfcc.append(np.mean(mfcc_features, axis=0))
    voice_profile = np.mean(all_mfcc, axis=0) if all_mfcc else None
    return voice_profile

def verify_voice(input_audio_path, voice_profile, fixed_length=2.0):
    """Compare input voice with the precomputed voice profile."""
    input_audio, input_sr = load_audio(input_audio_path)
    input_mfcc = compute_mfcc(input_audio, input_sr, fixed_length)
    input_mfcc_mean = np.mean(input_mfcc, axis=0)
    similarity = np.dot(input_mfcc_mean, voice_profile) / (
        np.linalg.norm(input_mfcc_mean) * np.linalg.norm(voice_profile)
    )
    return similarity > 0.8  # Adjust threshold for accuracy

def process_command(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = music_library.music.get(song, None)
        if link:
            webbrowser.open(link)
        else:
            speak("Song not found.")
    elif "news" in c.lower():
        r = requests.get(f'https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}')
        if r.status_code == 200:
            articles = r.json().get('articles', [])
            for article in articles:
                speak(article["title"])
        else:
            speak("Unable to fetch news.")
    else:
        speak("Command not recognized.")

if __name__ == "__main__":
    if not os.path.exists(REFERENCE_VOICE_FOLDER):
        print("Reference voice folder does not exist.")
        exit()

    # Generate voice profile from reference samples
    voice_profile = create_voice_profile(REFERENCE_VOICE_FOLDER)
    if voice_profile is None:
        print("No valid voice samples found in the reference folder.")
        exit()

    speak("Initializing virtual assistant")

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=3)
                word = recognizer.recognize_google(audio)

                if word.lower() in ["marcus", "hey marcus"]:
                    input_voice_path = "input_voice.wav"
                    with open(input_voice_path, "wb") as f:
                        f.write(audio.get_wav_data())

                    if verify_voice(input_voice_path, voice_profile):
                        speak("Voice verified. How can I assist you?")
                        os.remove(input_voice_path)

                        with sr.Microphone() as source:
                            print("Marcus active...")
                            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                            command = recognizer.recognize_google(audio)
                            process_command(command)

                            if "stop" in command.lower():
                                speak("Shutting down... Goodbye.")
                                break
                    else:
                        speak("Voice not recognized. Access denied.")
                        os.remove(input_voice_path)
        except Exception as e:
            print("Error: ", str(e))












# import os
# import numpy as np
# import speech_recognition as sr
# import pyttsx3
# import requests
# import music_library
# import webbrowser
# from openai import OpenAI
# from gtts import gTTS
# import pygame
# import soundfile as sf
# from python_speech_features import mfcc


# # Initialize recognizer and text-to-speech engine
# recognizer = sr.Recognizer()
# engine = pyttsx3.init()
# newsapi = 'a1d9a008ac2549d5b91ad89c5a93912b'

# def speak(text):
#     tts = gTTS(text)
#     tts.save('temp.mp3')
    
#     # Initialize Pygame mixer
#     pygame.mixer.init()
 
#     # Load the MP3 file
#     pygame.mixer.music.load('temp.mp3')

#     # Play the MP3 file
#     pygame.mixer.music.play()

#     # Keep the program running until the music stops playing
#     while pygame.mixer.music.get_busy():
#         pygame.time.Clock().tick(10)

#     os.remove("temp.mp3")

# def aiprocess(command):
#     client = OpenAI(api_key="sk-proj-B1V5vyIV3a3iR1QpsyZkvQRC-vScvQQSvcig6Sj5U9qHY8zybFRKJVBKblRsqD5gnoTL_XW19T3BlbkFJ8OGjV_1PS8pZn7GmdQza2DAAPBIobhiCmbVpSPLidcWhfFS7O4zsgVMJUjgh_EYLPiY1-_gjYA",)
#     completion = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[
#         {"role": "system", "content": "You are a virtual assistant named Marcus skilled in general tasks like Alexa and google cloud.give short answer"},
#         { "role": "user", "content": command}
#     ]
#     )

#     return (completion.choices[0].message.content)

# def processCommand(c):
#     if "open google" in c.lower():
#           webbrowser.open("https://google.com")
#     elif "open youtube" in c.lower():
#           webbrowser.open("https://youtube.com")
#     elif "open facebook" in c.lower():
#           webbrowser.open("https://facebook.com") 
#     elif "open linkedin" in c. lower():
#           webbrowser.open ("https://linkedin.com")
#     elif c.lower().startswith("play"):
#          song = c.lower().split(" ")[1]
#          link = music_library.music[song]
#          webbrowser.open(link)
#     elif "news" in c.lower():
#          r=requests.get(f'https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}')
#          if r.status_code == 200:
#             data = r.json()                       #Parse the JSON response
#             articles = data.get('articles',[])    #Extract the articles
#             for article in articles:           
#                 print(article["title"])
#                 speak(article["title"])
#     else:
#          #lets handled to open AI
#          output=aiprocess(c)
#          speak(output)

# def train_model(reference_audio_folder):
#   """
#   Trains a simple MLP classifier using reference audio files.

#   Args:
#     reference_audio_folder: Path to the folder containing reference audio files.

#   Returns:
#     Trained MLP classifier.
#   """

#   X_train = []
#   y_train = []

#   for filename in os.listdir(reference_audio_folder):
#     if filename.endswith(".wav"):
#       audio_path = os.path.join(reference_audio_folder, filename)
#       y_train.append(filename)  # Use filename as a simple label
      
#       try:
#         audio, sr = sf.read(audio_path)
#         mfccs = compute_mfcc(audio, sr)  # Use compute_mfcc function
#         mfccs_mean = np.mean(mfccs.T,axis=0) 
#         X_train.append(mfccs