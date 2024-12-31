import sys
import os
from transformers import VitsModel, AutoTokenizer

# Add the root directory (SPEECH-TO-SPEECH) to Python's path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_dir)

from TTS.facebookmms_handler import FacebookMMSTTSHandler
import threading
import queue
import torch
from scipy.io.wavfile import write
from output_speech import output_audio_stream_with_pyaudio, output_audio_stream_with_sd

def load_model_and_run_inference():
    stop_event = threading.Event()
    queue_in = queue.Queue()
    queue_out = queue.Queue()
    should_listen = threading.Event()
    chat = FacebookMMSTTSHandler(stop_event=stop_event, queue_in=queue_in, queue_out=queue_out)
    chat.setup(should_listen=should_listen) 
    chat.load_model("en")
    text = """The Israeli airstrikes, including on ports and energy infrastructure in the capital Sanaa, 
    were retaliation for Houthi missile and drone attacks on Israel over the past year, most of which were intercepted, the Israel Defense Forces (IDF) said in a statement."""
    wav_form = chat.generate_audio(text)
    output_audio_stream_with_sd(wav_form)

def finetune_model(text):
    ### TODO: tweak the parameter so that the model can speak slowly
    model_name = "facebook/mms-tts-eng"
    device = "cpu"
    model = VitsModel.from_pretrained(model_name).to(device)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    input_ids = inputs.input_ids.to(device).long()
    attention_mask = inputs.attention_mask.to(device)
    with torch.no_grad():
        output = model(input_ids=input_ids, attention_mask=attention_mask)
    
    print(model, tokenizer)
    return output.waveform
if __name__ == "__main__":
    load_model_and_run_inference()