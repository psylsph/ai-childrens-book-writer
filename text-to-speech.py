import shutil
import os
from pydub import AudioSegment
from pyt2s.services import stream_elements

def split_string_at_spaces(text, chunk_size=1000):
    """
    Splits a string into chunks of specified size, ensuring splits occur at spaces.
    
    Args:
        text (str): The input string to split
        chunk_size (int): Maximum size of each chunk (default: 1000)
        
    Returns:
        list: List of string chunks
    """
    chunks = []
    while len(text) > chunk_size:
        # Find the last space within the chunk size
        split_at = text.rfind(' ', 0, chunk_size)
        
        # If no space found, force split at chunk_size
        if split_at == -1:
            split_at = chunk_size
            
        chunks.append(text[:split_at].strip())
        text = text[split_at:].strip()
    
    # Add the remaining text
    if text:
        chunks.append(text)
        
    return chunks

book_text = open("runs/llama-70b/book.txt", "r").read()

text_as_chunks = split_string_at_spaces(book_text,500)

for i, text in enumerate(text_as_chunks):
    data = stream_elements.requestTTS(text)
    with open('test.mp3', '+wb') as file:
        file.write(data)
    if i == 0:
        shutil.move("test.mp3", "audio_book.mp3")
    else:
        final_wav = AudioSegment.from_file("audio_book.mp3", "mp3")
        current_chunk = AudioSegment.from_file("test.mp3", format="mp3")
        combined_sounds = final_wav + current_chunk
        combined_sounds.export("audio_book.mp3", format="mp3")
os.remove("test.mp3")
