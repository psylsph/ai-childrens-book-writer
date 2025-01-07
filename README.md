# Pydantic AI Book Generation and Text-to-Speech

This project consists of two main Python scripts: `app.py` and `text-to-speech.py`.

## `app.py`

This script uses the `pydantic-ai` library to generate a multi-chapter book. It leverages different language models (currently configured for Gemini and a local Ollama model) to perform the following steps:

1. **Planning:** An `Agent` is used to create a detailed outline for the book, defining the structure and key elements of each chapter. The outline is based on an initial prompt provided in `story_prose.md`.
2. **Writing:** Another `Agent` takes the generated outline and writes the content for each chapter, ensuring a minimum word count and adherence to the plot. The generated book is saved to a file named `book-[model_name].md`.
3. **Summarization:** A third `Agent` creates summaries for each chapter, which are saved to `summary-[model_name].md`.

The script uses environment variables (loaded from a `.env` file) for API keys and model configurations.

## `text-to-speech.py`

This script takes a text file (`book.md`) and converts it into an audiobook. It performs the following actions:

1. **Text Chunking:** The script splits the input text into smaller, manageable chunks, ensuring that splits occur at spaces to maintain word integrity.
2. **TTS Model Loading:** It downloads a pre-trained text-to-speech model from Silero AI if it doesn't already exist locally (`model.pt`).
3. **Speech Generation:** It iterates through the text chunks and uses the loaded model to generate speech audio for each chunk.
4. **Audio Combination:** The generated audio chunks are combined into a single audio file (`audio_book.mp4`).

## Workflow

The intended workflow is to first run `app.py` to generate the book content. The output of this script (`book.md`) can then be used as the input for `text-to-speech.py` to create an audiobook version.

## Requirements

- Python 3.6+
- Required Python packages: `pydantic-ai`, `torch`, `pydub`, `python-dotenv`. Install them using:
  ```bash
  pip install pydantic-ai torch pydub python-dotenv
  ```
- For `app.py`, you may need API keys for the language models you intend to use (e.g., Gemini). These should be set as environment variables in a `.env` file.
- For `text-to-speech.py`, ensure you have a `book.md` file with the text you want to convert to speech.

## Model

The `text-to-speech.py` script downloads a pre-trained Silero TTS model (`model.pt`).

## Usage

1. **Generate Book Content:**
   ```bash
   python app.py
   ```
   This will generate the book content and save it to `book-[model_name].md`.

2. **Generate Audiobook:**
   - Ensure that the `book.md` file exists (you may need to rename the output of `app.py`).
   ```bash
   python text-to-speech.py
   ```
   This will create an audiobook file named `audio_book.mp4`.