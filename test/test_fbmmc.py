from TTS.facebookmms_handler import FacebookMMSTTSHandler
import threading
import queue
from scipy.io.wavfile import write
import numpy as np
import torch
from output_speech import save_file_input_mp3
# specify some params for call the facebookMMSTTS model out
stop_event = threading.Event()
queue_in = queue.Queue()
queue_out = queue.Queue()

should_listen = threading.Event()

chat = FacebookMMSTTSHandler(stop_event=stop_event, queue_in=queue_in, queue_out=queue_out)

# chat.setup(should_listen=should_listen) 

chat.load_model("en")
text = """The Israeli airstrikes, including on ports and energy infrastructure in the capital Sanaa, 
were retaliation for Houthi missile and drone attacks on Israel over the past year, most of which were intercepted, the Israel Defense Forces (IDF) said in a statement."""
wav_form = chat.generate_audio(text)
save_file_input_mp3(wav_form, "test_output.mp3")