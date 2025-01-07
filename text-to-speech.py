# Import TTS
#from TTS.api import TTS

# Initialize the TTS model (Tacotron2 + HiFi-GAN)
#tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=True, gpu=False)

book_text = open("book.txt", "r").read()
# Generate speech from text
#tts.tts_to_file(text=book, file_path="output.wav")


import os
import torch

device = torch.device('cpu')
torch.set_num_threads(4)
local_file = 'model.pt'

if not os.path.isfile(local_file):
    torch.hub.download_url_to_file('https://models.silero.ai/models/tts/en/v3_en.pt',
                                   local_file)  

model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
model.to(device)

example_text = "Matthew's room was a sanctuary of tranquility, adorned with posters of his favorite video games and superheroes. The warm, inviting glow of his computer screen bathed the space in a soft, incandescent light as Matthew, a thirteen-year-old boy with a mop of unruly brown hair, stared unblinkingly at his Minecraft world. A world he had painstakingly crafted over years, pixel by pixel."
sample_rate = 48000
speaker='en_10'

audio_paths = model.save_wav(text=book_text,
                             speaker=speaker,
                             sample_rate=sample_rate)
print(audio_paths)
