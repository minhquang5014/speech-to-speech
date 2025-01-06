import logging
import os
from time import perf_counter

from faster_whisper import WhisperModel
from rich.console import Console

from baseHandler import BaseHandler

console = Console()

logger = logging.getLogger(__name__)


class FasterWhisperSTTHandler(BaseHandler):
    """
    Handles the Speech To Text generation using a Whisper model.
    """

    def setup(
        self,
        model_name: str = "tiny.en",
        device: str = "auto",
        compute_type: str = "auto",
        gen_kwargs={},  # additional keyword arguments for the model
    ):
        self.gen_kwargs = self.adapt_gen_kwargs(gen_kwargs)

        os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"  # rsolves conflicts with OpenMP when multiple models are loaded
        
        # loading the model FasterWhisper is instantiated with the given parameters
        self.model = WhisperModel(model_name, device=device, compute_type=compute_type)

    def process(self, audio):
        """
        Process the audio and return the transcribed text.
        """
        global pipeline_start
        
        # to measure performance using perf_counter to track the pipeline's runtime
        pipeline_start = perf_counter()

        # the transcibe function, passing the audio and any configured parameters
        segments, info = self.model.transcribe(audio, **self.gen_kwargs)
        output_text = []

        for segment in segments:
            # group all the segments into a full text
            logger.debug(
                "[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text)
            )
            output_text.append(segment.text)

        pred_text = " ".join(output_text).strip()

        if pred_text:
            console.print(f"[yellow]USER: {pred_text}")
            # the yield keyword is used to return transcription text iteratively, enabling the caller to process partial outputs in real-time
            yield pred_text
        else:
            logger.debug("no text detected. skipping...")

    def cleanup(self):
        print("Stopping FasterWhisperSTTHandler")
        del self.model

    def adapt_gen_kwargs(self, gen_kwargs: dict):
        gen_kwargs["without_timestamps"] = not gen_kwargs.pop("return_timestamps", True)

        return gen_kwargs
