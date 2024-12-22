import os 
import sys

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_dir)

from connections.local_audio_streamer import LocalAudioStreamer
from queue import Queue

input_queue = Queue()
output_queue = Queue()
local_audio = LocalAudioStreamer(input_queue=input_queue, output_queue=output_queue)

local_audio.run()