import os 
import sys

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_dir)

from connections.local_audio_streamer import LocalAudioStreamer
from queue import Queue
from threading import Thread
import time

input_queue = Queue()
output_queue = Queue()
local_audio = LocalAudioStreamer(input_queue=input_queue, output_queue=output_queue)

streamer_thread = Thread(
    target = local_audio.run, 
    daemon = True
)
streamer_thread.start()

try:
    for _ in range(100):
        if not input_queue.empty():
            data = input_queue.get()
            output_queue.put(data)
        time.sleep(0.1)
finally:
    local_audio.stop_event.set()
    streamer_thread.join()