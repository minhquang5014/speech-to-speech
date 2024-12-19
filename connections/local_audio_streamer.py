import threading
import sounddevice as sd
import numpy as np

import time
import logging

logger = logging.getLogger(__name__)


class LocalAudioStreamer:
    def __init__(
        self,
        input_queue,
        output_queue,
        list_play_chunk_size=512,
    ):
        self.list_play_chunk_size = list_play_chunk_size

        self.stop_event = threading.Event()
        self.input_queue = input_queue
        self.output_queue = output_queue

    def run(self):
<<<<<<< HEAD
        """The main method responsible for handling audio input and output using sounddevice library"""
        def callback(indata, outdata, frames, time, status):
            """This function is passed to the sd.Stream object. It handles real-time audio processing"""
=======
        def callback(indata, outdata, frames, time, status):
>>>>>>> 3962cf5b87f28ee586a66cab80e234db49fd23c2
            if self.output_queue.empty():
                self.input_queue.put(indata.copy())
                outdata[:] = 0 * outdata
            else:
                outdata[:] = self.output_queue.get()[:, np.newaxis]

        logger.debug("Available devices:")
<<<<<<< HEAD

        # logs the list of available audio devices to help debug device-related issues
        logger.debug(sd.query_devices())


=======
        logger.debug(sd.query_devices())
>>>>>>> 3962cf5b87f28ee586a66cab80e234db49fd23c2
        with sd.Stream(
            samplerate=16000,
            dtype="int16",
            channels=1,
            callback=callback,
            blocksize=self.list_play_chunk_size,
        ):
            logger.info("Starting local audio stream")
<<<<<<< HEAD

            # continuously checks the stop-event. If it's set, the loop ends, stopping the audio stream
=======
>>>>>>> 3962cf5b87f28ee586a66cab80e234db49fd23c2
            while not self.stop_event.is_set():
                time.sleep(0.001)
            print("Stopping recording")
