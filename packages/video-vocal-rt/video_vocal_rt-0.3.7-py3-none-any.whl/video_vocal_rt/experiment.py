import os
import random
import time
import cv2
import PySimpleGUI as sg
import sounddevice as sd 
import numpy as np
import tkinter as tk
from scipy.io.wavfile import write
from openpyxl import Workbook

def is_dir(dir_path: str) -> str:
    """
    Determines if a given string represents a valid directory path.

    Args:
        dir_path (str): The directory path to be checked.

    Returns:
        str: The original directory path string if it is valid.

    Raises:
        ValueError: If the provided string does not represent a valid directory path.
    """
    if not os.path.isdir(dir_path):
        raise ValueError(f"{dir_path} is not a valid directory path")
    
    return dir_path


def str_to_int(value: str, positive: bool = False) -> int:
    """
    Converts a given string to an integer and enforces that it is positive if specified.

    Args:
        value (str): The string to be converted to an integer.
        positive (bool, optional): If True, the resulting integer must be positive. 

    Returns:
        int: The resulting integer.

    Raises:
        ValueError: If the provided string cannot be converted to an integer or if the resulting 
            integer is not positive when it should be.
    """
    try: 
        value = int(value)  
    except ValueError:
        raise ValueError(f"{value} is not a valid integer")
    
    if positive and value <= 0:
        raise ValueError(f"{value} is not a positive integer")
    
    return value

class Parameters:
    def __init__(self, participant_id="", fixation_cross_duration=1000, white_duration=1000,
                 audio_duration=5, video_dir="VIDEO_FILES", audio_dir="RECORDINGS",
                 instruction_path=None, sample_rate=44100):
        self.participant_id = participant_id
        self.cross_dur = fixation_cross_duration
        self.white_dur = white_duration
        self.audio_dur = audio_duration
        self.video_dir = video_dir
        self.audio_dir = audio_dir
        self.inst_path = instruction_path
        self.sample_rate = sample_rate
        self.num_samples = int(self.audio_dur*self.sample_rate)
        self.audio_devices = [(d["index"], d["name"]) for d in sd.query_devices()]
        self.audio_device = sd.default.device[0]
        self.unique_key = str(time.time())      

    def gui_layout(self):
        layout = [

            [
            sg.Column([
                [sg.Text("Participant ID:")],
                [sg.Text("Fixation Duration (ms):")],
                [sg.Text("White Duration (ms):")],
                [sg.Text("Audio Duration (s):")],
                [sg.Text("Audio Device:")],
                ], element_justification="left", pad=(0, 5)),

            sg.Column([
                [sg.InputText(size = (35, 1), key = "-PARTICIPANT_ID-")],
                [sg.InputText(default_text=str(self.cross_dur), key="-CROSS-DUR-", size=(10, 1))],
                [sg.InputText(default_text=str(self.white_dur), key="-WHITE-DUR-", size=(10, 1))],
                [sg.InputText(default_text=str(self.audio_dur), key="-AUDIO-DUR-", size=(10, 1))],
                [sg.DropDown(self.audio_devices, default_value=self.audio_devices[self.audio_device], size=(40, 1), key="-AUDIO-DEV-")],
                ], element_justification="left", pad=(0, 5))
            ],

            [
            sg.Column([
                [sg.Text("Video Directory:")],
                [sg.Text("Audio Directory:")],
                [sg.Text("Instructions File (.txt):")],
                ], element_justification="left", pad=(0, 5)),

            sg.Column([
                [sg.InputText(default_text=self.video_dir, key="-VIDEO-DIR-", size=(40, 1)), sg.FolderBrowse()],
                [sg.InputText(default_text=self.audio_dir, key="-AUDIO-DIR-", size=(40, 1)), sg.FolderBrowse()],
                [sg.InputText(default_text=self.inst_path, key="-INST-PATH-", size=(40, 1)), sg.FileBrowse()],
                ], element_justification="left", pad=(0, 5))
            ],
            
            [
            sg.Column([ 
                [sg.Button("Start Experiment", size=(20,1))]
                ], expand_x=True, element_justification="left", pad=(0, 5)),
            
            sg.Column([ 
                [sg.Button("Reset", size=(10,1)), sg.Button("Cancel", size=(10,1))] 
                ], expand_x=True, element_justification="right", pad=(0, 5))
            ],
        ]
        return layout
    


    def set_attributes_values(self, values):
        self.participant_id = str(values["-PARTICIPANT_ID-"])
        self.white_dur = str_to_int(values["-WHITE-DUR-"])
        self.cross_dur = str_to_int(values["-CROSS-DUR-"])
        self.audio_dur = str_to_int(values["-AUDIO-DUR-"])
        self.audio_dev = str_to_int(values["-AUDIO-DEV-"][0])
        self.video_dir = is_dir(values["-VIDEO-DIR-"])
        self.audio_dir = is_dir(values["-AUDIO-DIR-"])
        self.inst_path = values["-INST-PATH-"]

    def reset_attributes_values(self, window):
        window["-PARTICIPANT_ID-"].update(str(self.participant_id))
        window["-CROSS-DUR-"].update(str(self.cross_dur))
        window["-WHITE-DUR-"].update(str(self.white_dur))
        window["-AUDIO-DUR-"].update(str(self.audio_dur))
        window["-AUDIO-DEV-"].update(self.audio_devices[sd.default.device[0]])
        window["-VIDEO-DIR-"].update(str(self.video_dir))
        window["-AUDIO-DIR-"].update(str(self.audio_dir))
        window["-INST-PATH-"].update(str(self.inst_path))
    
    def get_from_gui(self):
        layout = self.gui_layout()
        window = sg.Window("Experiment Setup", layout)
        
        while True:
            event, values = window.read()
            if event == "Cancel" or event == sg.WIN_CLOSED:
                window.close()
                exit()

            elif event == "Start Experiment":
                try:
                    self.set_attributes_values(values)
                    window.close()
                    break
                except Exception as e:
                    sg.popup(f"Error: {e}")
                    continue
            
            if event == "Reset":
                self.reset_attributes_values(window)

        window.close()

def get_parameters_from_user():
    parameters = Parameters()
    parameters.get_from_gui()
    return parameters

def create_white_screen():
    root = tk.Tk()
    height = root.winfo_screenheight()
    width = root.winfo_screenwidth()
    root.destroy()
    return np.ones((height, width, 3), dtype=np.uint8) * 255

def get_center_coordinates(image):
    height, width, _ = image.shape
    return (width // 2, height // 2)    # return (x, y)

def create_instruction_screen(text):
    instructions = create_white_screen()
    x_mid, y_mid = get_center_coordinates(instructions)
    x0, y0 = x_mid //2, y_mid //2
    dy = 18
    for i, line in enumerate(text.split('\n')):
        y = y0 + i * dy
        x = x0
        cv2.putText(img=instructions, text=line, org = (x,y),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                    color=(0,0,0), thickness=2, lineType=cv2.LINE_AA)
    return instructions

def create_fixation_screen():
    fixation = create_white_screen()
    x, y = get_center_coordinates(fixation)

    size = 20
    cv2.line(fixation, (x - size, y), (x + size, y), (0, 0, 0), thickness=2)
    cv2.line(fixation, (x, y - size), (x, y + size), (0, 0, 0), thickness=2)
    return fixation

def run():
    # Create the GUI to enter experiment parameters, returns a parameters object
    params = get_parameters_from_user()

    # List of all the files in the video directory and shuffle them
    video_files = [f for f in os.listdir(params.video_dir) if f.endswith('.avi')]
    random.shuffle(video_files)

    # Create a new directory with the participant name in the audio directory 
    participant_dir = os.path.join(params.audio_dir, params.participant_id)
    os.makedirs(participant_dir, exist_ok=True)   

    # Set up excel file
    wb = Workbook()
    ws = wb.active
    ws.append(['ID', 'Order', 'Video', 'Audio_path'])

    # Display blank screen and wait for key press
    blank = create_white_screen()
    fixation = create_fixation_screen()
    try:
        with open (params.inst_path, 'r') as f:
            instructions = create_instruction_screen(f.read())
    except FileNotFoundError:
        instructions = create_instruction_screen("Press any key to continue...")

    cv2.namedWindow('main_window', cv2.WINDOW_NORMAL)
    cv2.imshow('main_window', instructions)
    cv2.waitKey(0)

    for i, video_file in enumerate(video_files):
        video = cv2.VideoCapture(os.path.join(params.video_dir, video_file))
        mspf = int(1000 / video.get(cv2.CAP_PROP_FPS))  # ms per frame

        # Fixation screen display
        cv2.imshow('main_window', fixation)
        cv2.waitKey(params.cross_dur)

        recording = sd.rec(params.num_samples, samplerate=params.sample_rate, channels=1, device=params.audio_device)
        
        while True: # Video playing loop
            ret, frame = video.read()
            if not ret:
                break
            cv2.imshow('main_window', frame)
            key = cv2.waitKey(mspf)
            if key == ord('q'): # Exit loop if 'q' key is pressed
                exit()
            
        # white screen display
        cv2.imshow('main_window', blank)
        cv2.waitKey(params.white_dur)

        sd.wait() # wait for recording to finish
        audio_file = f"{video_file[:-4]}_{params.participant_id}_{params.unique_key}.wav"
        audio_path = os.path.join(participant_dir, audio_file)
        write(audio_path, params.sample_rate, recording)

        ws.append([params.participant_id, i+1, video_file, audio_path])

        video.release()

    cv2.destroyAllWindows()

    data_file = f"{params.participant_id}_{params.unique_key}.xlsx"
    wb.save(os.path.join(participant_dir, data_file))

if __name__ == "__main__":
    run()