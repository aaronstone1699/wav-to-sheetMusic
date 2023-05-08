# wav-to-sheetMusic
The provided code is an audio processing application implemented using the Tkinter library in Python. It allows the user to select a WAV file, clean the audio, convert it to MIDI format, and display the corresponding sheet music.

# Libraries Used
The following libraries are imported in the code:

1. tkinter: Provides the necessary functions and classes for creating the graphical user interface (GUI).
2. filedialog: Part of tkinter, provides file dialog functionality for selecting files.
3. os: Provides functions for interacting with the operating system, such as file path manipulation.
4. PIL: Stands for Python Imaging Library, provides image processing capabilities.
5. matplotlib.pyplot: Used for creating and displaying plots.
6. music21: A toolkit for computer-aided musicology, used for music file parsing and manipulation.
7. sys: Provides access to some variables and functions used for interacting with the Python interpreter.
8. crepe: A library for pitch estimation and analysis of audio signals.
9. librosa: A library for audio and music analysis, used for loading audio files and extracting features.
10. numpy: A library for numerical computing with arrays, used for various mathematical operations.
11. soundfile: A library for reading and writing audio files.
12. noisereduce: A library for audio noise reduction.

# Functions
1. clean_wav(input_wav, output_wav)
* Description: Cleans the input WAV audio file by applying noise reduction using the noisereduce library and saves the cleaned audio to a new WAV file.
Parameters:
* input_wav (str): The path to the input WAV file.
* output_wav (str): The path to save the cleaned WAV file.
2. display_sheet_music(xml_file)
* Description: Parses an XML file containing sheet music using the music21 library, extracts note positions and durations, creates a plot using matplotlib, and displays the sheet music image in the GUI.
* Parameters:
xml_file (str): The path to the XML file containing the sheet music.
3. wav_to_midi(wav_file, output_midi, output_sheet)
* Description: Converts a WAV audio file to MIDI format using the librosa and crepe libraries, creates a MIDI object with piano notes based on the pitch and duration information, and saves the MIDI file. It also converts the MIDI file to sheet music notation and saves it as an XML file.
* Parameters:
wav_file (str): The path to the input WAV file.
output_midi (str): The path to save the output MIDI file.
output_sheet (str): The path to save the output sheet music XML file.
* Returns:
A list containing time, frequency, and confidence information from the pitch estimation.
4. convert_and_display()
* Description: This function is executed when the "Select and Process WAV" button is clicked. It opens a file dialog to select a WAV file, cleans the audio, converts it to MIDI format, and displays the corresponding sheet music in the GUI.
5. quit_program()
Description: Exits the program by calling sys.exit().

# GUI Window
The code creates a GUI window using the tkinter.Tk class. The window has a title "Audio Processing" and a size of 800x600 pixels. The background color is set to a dark shade of gray.

1. Buttons
Two buttons are created using the tkinter.Button class:

* "Select and Process WAV" button: When clicked, it opens a file dialog for selecting a WAV file. It then calls the convert_and_display() function to clean the audio, convert it to MIDI, and display the sheet music.

* "Quit" button: When clicked, it calls the quit_program() function to exit the program.

Both buttons are styled with a solid relief, zero border width, and a dark gray background color. The "Select and Process WAV" button has white text color and some padding, while the "Quit" button has white text color and padding as well.

* Sheet Music Label
A label widget is created using the tkinter.Label class to display the sheet music image. It is initially empty and will be updated when the display_sheet_music() function is called.

