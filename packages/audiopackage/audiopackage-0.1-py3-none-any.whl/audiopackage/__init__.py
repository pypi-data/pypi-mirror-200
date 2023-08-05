import openai
from tkinter.filedialog import askopenfilename
import os


new_directory = '/Users/JUNAID/Desktop'
os.chdir(new_directory)

api_key = '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'
# chosen_file = askopenfilename()
chosen_file = askopenfilename()
openai.api_key = api_key
audio_file= open(chosen_file, "rb")
transcript = openai.Audio.transcribe("whisper-1", audio_file)
print(transcript.text)
