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
engine.save_to_file(text, "principal_profile.mp3")
engine.runAndWait()

print("MP3 file created successfully")
