# Pydantic AI Book Generation and Text-to-Speech

This project consists of two main Python scripts: `app.py` and `text-to-speech.py`.

My Hardware

AMD 7700 XT 12GB - Using RocM unless fails and then use Vulkan
AMD 7600 with 32GB DDR5 6000
Mostly done using lm studio to allow quicker tuning of Context Size

Current Best Models
* mistral-nemo-instruct-2407 by far with 12k context window
* ifable_-_gemma-2-ifable-9b
* darkest-muse-v1 - OK for shorter max context 8192
* llama-3.1-70b-versatile - via Groq
* DeekSeek v3 - via DeepSeek API
* llama3.1-7b
* Quill v1, book seemed to cut off before end

Unsensor Models (No suitable for children's Content)
* hf.co/MaziyarPanahi/Mistral-7B-Instruct-v0.3-GGUF:Q8_0, TEMP 0.7, CTX 12000


Poor Models
* phi-4, Vulkan only and limited to 12000 context window and fails to generate even a plan, RocM failed to load so under Vulkan
* alphawriter-32768


Going down the list to test https://eqbench.com/creative_writing.html

## `app.py`

This script uses the `pydantic-ai` library to generate a multi-chapter book. It leverages different language models (currently configured for Gemini) to perform the following steps:

1. **Planning:** An `Agent` is used to create a detailed outline for the book. The outline is based on an initial prompt provided in `story_prose.md`. If a plan file (`plan-[model_name].md`) already exists, it will load the existing plan.
2. **Writing:** Another `Agent` takes the generated outline and writes the content for each chapter, ensuring a minimum word count. The generated book is saved to `book-[model_name].md`. If a book file already exists, it will load the existing book content.
3. **Summarization:** A third `Agent` creates short summaries (around 20 words) for each chapter, intended for AI image generation. These summaries are saved to `summary-[model_name].md`.

The script uses environment variables (loaded from a `.env` file) for API keys and model configurations.

## `text-to-speech.py`

This script converts a text file into an audiobook using an external text-to-speech service. It performs the following actions:

1. **Text Chunking:** The script splits the input text (from `runs/llama-70b/book.txt`) into smaller chunks of 500 characters.
2. **Speech Generation:** It uses the `stream_elements.requestTTS` function to generate speech audio for each chunk.
3. **Audio Combination:** The generated audio chunks are combined into a single MP3 audio file (`audio_book.mp3`).

## Workflow

The intended workflow is to first run `app.py` to generate the book content. The output of this script (`book-[model_name].md`) can then be used conceptually as input, although `text-to-speech.py` currently reads from a specific file (`runs/llama-70b/book.txt`). Running `text-to-speech.py` will create an audiobook version of the specified book.

## Requirements

- Python 3.6+
- Required Python packages: `pydantic-ai`, `pydub`, `python-dotenv`, `pyt2s`. Install them using:
  ```bash
  pip install pydantic-ai pydub python-dotenv pyt2s
  ```
- For `app.py`, you may need API keys for the language models you intend to use (e.g., Gemini). These should be set as environment variables in a `.env` file.
- For `text-to-speech.py`, the script currently expects the book content to be in `runs/llama-70b/book.txt`.

## Model

The `text-to-speech.py` script uses an external service for text-to-speech conversion.

## Usage

1. **Generate Book Content:**
   ```bash
   python app.py
   ```
   This will generate the book content and save it to `book-[model_name].md`, and the plan to `plan-[model_name].md`, and summaries to `summary-[model_name].md`.

2. **Generate Audiobook:**
   - Ensure that the book content you wish to convert is located in `runs/llama-70b/book.txt`.
   ```bash
   python text-to-speech.py
   ```
   This will create an audiobook file named `audio_book.mp3`.