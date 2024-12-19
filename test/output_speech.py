import numpy as np
from scipy.io.wavfile import write

def save_file_input_mp3(input_array, output_path):
    """unnormalize the data, save the data in the cpu, convert back to numpy array in the int16 format and save it in to mp3 sound file"""
    unnormalized_data = input_array * 32767

    audio_array = unnormalized_data.cpu().numpy().flatten()
    # int_audio_array = np.int16(audio_array)
    write(output_path, 22050, audio_array)
    

