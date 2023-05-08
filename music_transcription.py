import tkinter as tk
from tkinter import filedialog
from tkinter import Tk, Button
import os
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from music21 import converter
import sys
import crepe
import librosa
from music21 import stream, meter, tempo
from music21.note import Note
import numpy as np
import soundfile as sf
import noisereduce as nr


def clean_wav(input_wav, output_wav):
    # Load the input audio file
    audio_data, sample_rate = librosa.load(input_wav)

    # Apply noise reduction
    reduced_noise = nr.reduce_noise(
        y=audio_data, sr=sample_rate, prop_decrease=0.4)

    # Save the cleaned audio to a new WAV file
    sf.write(output_wav, reduced_noise, sample_rate)


def display_sheet_music(xml_file):
    # Parse the XML file
    sheet = converter.parse(xml_file)

    # Extract the notes from the sheet music
    notes = sheet.recurse().notes

    # Initialize lists to store note positions and durations
    positions = []
    durations = []

    # Iterate through the notes and extract position and duration information
    for note in notes:
        positions.append(note.offset)
        durations.append(note.duration.quarterLength)

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.scatter(positions, durations, color='black', marker='o')
    plt.xlabel('Time')
    plt.ylabel('Duration')
    plt.title('Sheet Music')
    plt.grid(True)

    # Save the plot as an image
    plt.savefig('sheet_music.png')

    # Display the image in the GUI
    image = Image.open('sheet_music.png')
    image = image.resize((400, 400), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(image)
    sheet_music_label.configure(image=image)
    sheet_music_label.image = image


def wav_to_midi(wav_file, output_midi, output_sheet):
    # Load the audio file
    y, sr = librosa.load(wav_file)

    # Use CREPE to estimate the pitches and activations
    time, frequency, confidence, _ = crepe.predict(y, sr, viterbi=True)

    # Process the predictions
    voiced_frames = confidence > 0.8

    # Compute the time positions of the voiced frames
    times = time[voiced_frames]

    # Compute the time differences between consecutive voiced frames
    time_diffs = np.diff(times)

    # Create a MIDI object
    midi = stream.Stream()

    # Set the time signature and tempo in the MIDI object
    midi.timeSignature = meter.TimeSignature('4/4')
    midi.insert(0, tempo.MetronomeMark(number=100))

    # Add the piano notes to the MIDI object
    piano_part = stream.Part()
    for note, time_diff in zip(frequency[voiced_frames], time_diffs):
        note_obj = Note()
        note_obj.pitch.frequency = note
        note_obj.duration.quarterLength = time_diff
        piano_part.append(note_obj)

    # Add the piano part to the MIDI object
    midi.insert(0, piano_part)

    # Save the MIDI file
    midi.write('midi', fp=output_midi)

    # Convert MIDI to sheet music notation
    sheet = converter.parse(output_midi)
    sheet.write('musicxml', fp=output_sheet)

    return [time, frequency, confidence]


def convert_and_display():
    # Get the input WAV file path
    input_wav = filedialog.askopenfilename(
        title='Select Input WAV File', filetypes=[('WAV Files', '*.wav')])

    # Clean the WAV file
    output_wav = os.path.splitext(input_wav)[0] + '_clean.wav'
    clean_wav(input_wav, output_wav)

    # Convert WAV to MIDI and display sheet music
    output_midi = os.path.splitext(input_wav)[0] + '.mid'
    output_sheet = os.path.splitext(input_wav)[0] + '.xml'
    wav_to_midi(output_wav, output_midi, output_sheet)
    display_sheet_music(output_sheet)


def quit_program():
    #quit the program
    sys.exit(0)


# Create the GUI window
window = tk.Tk()
window.title("Audio Processing")
window.geometry("800x600")
R = 60
G = 78
B = 89
color_code = '#%02x%02x%02x' % (R, G, B)
window.configure(bg=color_code)

# Create a button to select and process the WAV file
process_button = tk.Button(window, text="Select and Process WAV", command=convert_and_display,
                           relief="solid", borderwidth=0, bg="#263233", padx=10, pady=5, fg='white')
process_button.pack(pady=20)

button_quit = Button(window, text="Quit", command=quit_program, relief="solid",
                     borderwidth=0, bg="#263233", padx=10, pady=5, fg='white')
button_quit.pack()


# Create a label to display the sheet music image
sheet_music_label = tk.Label(window)
sheet_music_label.pack()

# Run the GUI loop
window.mainloop()
