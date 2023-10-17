import speech_recognition as sr
from pydub import AudioSegment
import re
import csv

# Function to transcribe and format the audio file
def transcribe_and_format(audio_file_path):
    # Load the audio file
    audio = AudioSegment.from_file(audio_file_path, format="aac")

    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # List to store formatted results
    results = []

    # Split the audio into chunks for transcription
    chunk_duration_ms = 5000  # 5 seconds per chunk
    for i in range(0, len(audio), chunk_duration_ms):
        print("chunk {0} out of {1}".format(i, len(audio)))
        chunk = audio[i:i + chunk_duration_ms]

        # Export the chunk to a temporary audio file
        chunk.export("temp_chunk.wav", format="wav")

        # Transcribe the chunk
        with sr.AudioFile("temp_chunk.wav") as source:
            audio_data = recognizer.record(source)

            # Use the Google Web Speech API for transcription
            try:
                transcription = recognizer.recognize_google(audio_data)
            except sr.UnknownValueError:
                transcription = ""
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))
                return

        # Calculate the start and end time for the chunk
        start_time = i / 1000  # Convert milliseconds to seconds
        end_time = min((i + chunk_duration_ms) / 1000, len(audio) / 1000)  # Ensure end_time does not exceed audio duration

        # Format the result and add to the list
        # result = "{:.2f} - {:.2f}: {}".format(start_time, end_time, transcription)
        result = [start_time, end_time, transcription]
        results.append(result)
        # break

    # Clean up temporary files
    import os
    os.remove("temp_chunk.wav")

    return results

# Specify the path to your audio file
audio_file_path = "audios/dilshad.aac"

# Transcribe and format the audio
formatted_transcription = transcribe_and_format(audio_file_path)
# Specify the path to the CSV file
csv_file_path = "output.csv"

# Write the results to a CSV file
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Start Time", "End Time", "Transcription"])  # Header row
    writer.writerows(formatted_transcription)

print(f"Transcription results saved to {csv_file_path}")

# print(formatted_transcription)
