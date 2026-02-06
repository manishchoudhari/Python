# Text to Speech Conversion Script
# Author: Manish Choudhari
# Prerequisites: Install pyttsx3 library using pip install pyttsx3

import pyttsx3

text = """
Principal Data and AI MS Engineer with over fifteen years of experience
architecting enterprise scale data platforms and intelligent solutions.
Deep expertise in modern data engineering including SQL, Azure Data Factory,
and Databricks, with a strong focus on the Azure AI stack.
"""

engine = pyttsx3.init()

# Set the parameters for voices like speed, volume and voice type (male / female)

voices = engine.getProperty('voices')       # Show details of current voice
engine.setProperty('voice', voices[0].id)  # Index 0 for male
#engine.setProperty('voice', voices[1].id)   # Index 1 for female

engine.setProperty('rate', 160)     # Speaking speed
engine.setProperty('volume', 1)     # Volume 0 for Mute, 1 for Max

engine.save_to_file(text, "Output.mp3")
engine.runAndWait()

print("MP3 file created successfully")
