from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.models.openai import OpenAIModel
import os
from dotenv import load_dotenv
load_dotenv()

#GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# model = GroqModel('llama-3.1-70b-versatile', api_key=GROQ_API_KEY)
#model = GroqModel('mixtral-8x7b-32768', api_key=GROQ_API_KEY)

# DEEPSEEK_API_KEY= os.getenv("DEEPSEEK_API_KEY")

# model = OpenAIModel(
#     'deepseek-chat',
#     base_url='https://api.deepseek.com/v1',
#     api_key=DEEPSEEK_API_KEY,
# )

#GEMINI_API_KEY= os.getenv("GEMINI_API_KEY")
#model = GeminiModel('gemini-2.0-flash-exp', api_key=GEMINI_API_KEY)

OLLAMA_API_KEY= os.getenv("OLLAMA_API_KEY")
model = OpenAIModel(
     'Darkest-muse-v1-32768',
     base_url='http://localhost:11434/v1',
     api_key=OLLAMA_API_KEY,
 )

num_chapters = 7
initial_prompt = open("story_prose.md").read()

plan_name = f"plan-{model.model_name}.md"

if os.path.exists(plan_name):
    # load the plan from a file, delete the file if you want to regenerate
    planner_result = open(plan_name, encoding='utf-8').read()
else:
    try:
        planner = Agent(  
            model,
            result_type=str,
            system_prompt=("""Prompt: Generate a detailed outline for at least {num_chapters} chapters.

                    Instructions:
                    1. YOU MUST USE EXACTLY THIS FORMAT FOR EACH CHAPTER - NO DEVIATIONS.
                    2. Ensure that every field is filled out completely and accurately for each chapter.
                    3. Do not deviate from the structure or add any additional text outside the specified format.
                    
                    Required Format for Each Chapter:
                    Chapter [X]: [Title]
                    Key Events:
                    - [Event 1]
                    - [Event 2]
                    - [Event 3]
                    Scenes:
                    - [Scene 1]
                    - [Scene 2]
                    - [Scene 3]
                    Character Developments: [Specific character moments and changes]
                    Setting: [Specific location and atmosphere]
                    Tone: [Specific emotional and narrative tone]
                    Themes: [Specific thematic elements]
                    Plot Significance: [Specific impact on overall story]

                    [REPEAT THIS EXACT FORMAT FOR ALL {num_chapters} CHAPTERS]

                    Requirements:
                    1. EVERY field must be present for EVERY chapter
                    2. EVERY chapter must have AT LEAST 3 specific Key Events
                    3. ALL chapters must be detailed - no placeholders
                    4. Format must match EXACTLY - including all headings and bullet points

                    Initial Premise:
                    {initial_prompt}

                    Final Instruction:
                    1. DO NOT include any explanations or narratives outside the outline format.
                    2. ADHERE STRICTLY to the format and requirements outlined above.
                    """
            ),
            retries=5)

        planner_result = planner.run_sync(f'Generate a comprehensive outline for a novel using {initial_prompt} it should have at least {num_chapters} chapters.').data
        open(plan_name, "w", encoding='utf-8').write(planner_result)
        print(planner_result)
    except Exception as e:
        print(f"An error occurred: {e}")
    
book_name = f"book-{model.model_name}.md"

if os.path.exists(book_name):
    # load the plan from a file, delete the file if you want to regenerate
    writer_result = open(book_name, encoding='utf-8').read()
else:
    writer = Agent(  
        model,
        result_type=str,
        system_prompt=(f"""Prompt:
                Role: You are a highly skilled creative writer with a talent for bringing scenes to life through vivid descriptions and engaging prose. Your task is to craft compelling chapters for a book based on the provided outline and context.

                Book Context:
                {planner_result}

                Guidelines:
                1. Adhere to the Plot Outline: Ensure that each chapter follows the outlined plot points closely, staying true to the story's direction.
                2. Character Consistency: Maintain consistent and authentic character voices throughout the chapter. Each character should be distinct and true to their established personalities.
                3. World-Building: Incorporate detailed descriptions of the setting and environment to enrich the world-building. This should enhance the reader's immersion without slowing down the pace of the narrative.
                4. Engaging Prose: Write in a style that is both engaging and descriptive, drawing the reader into the scene and making it feel real.
                5. Complete Scenes: Make sure that each chapter is a complete narrative unit with a clear beginning, middle, and end. Do not leave scenes hanging or unresolved.
                6. Word Count Requirement: Each chapter MUST be at least 2000 words (30000 chracters). This is a hard requirement. If the output is shorter, continue writing until the minimum length is reached.
                7. Smooth Transitions: Ensure that transitions between scenes and chapters are smooth and logically flowing, maintaining the story's momentum.
                8. Detailed Descriptions: Add detailed descriptions of the environment and characters where appropriate, but avoid info-dumping. Balance is key.
                9. Reference the Outline and Previous Content: Always refer back to the plot outline and previous chapters to maintain consistency and continuity.
                10. Ensure each chapter is self-contained and can stand on its own as a complete narrative unit.
                11. Ensure each chapter covers the narrative of ALL the defined Scenes.
                12. Use British English spelling and grammer.

                Additional Notes:
                - Take your time with each chapter, ensuring that it meets all the guidelines and requirements.
                - Feel free to ask for clarification if any part of the outline is unclear."""),
        retries=5)

    with open(book_name, "w", encoding='utf-8') as book:
        try:
            chapter_outlines = planner_result.split("Chapter ")
            for chapter_num in range(1, num_chapters+1):
                print(f"##########################################################################################################################")
                print(f"{chapter_outlines[chapter_num]}")
                writer_result = writer.run_sync(f"""
                    For the chapter outlined in the following Chapter Outline please write a 2000 chapter covering all of the scenes.
                    Ensure each of the scene flows from one to the next. If you first attempt does not have 2000 words try again.
                    Chapter Outline: {chapter_outlines[chapter_num]}""")
                print(writer_result.data)
                book.write(f"{writer_result.data}\n\n")
                book.flush()
        except Exception as e:
            print(f"An error occurred: {e}")
    
chapter_text = open(book_name, encoding='utf-8').read().split("Chapter ")


summary_writer = Agent(  
    model,
    result_type=str,
    system_prompt=(f"""Prompt:
            Role: You are a highly skilled creative artist with a talent for bringing scenes to life through vivid descriptions and engaging prose."""),
    retries=5)

with open(f"summary-{model.model_name}.md", "w", encoding='utf-8') as summary:
    try: 
        for chapter in chapter_text:
            # ingore short lines it means the split messed up the first split
            if len(chapter) > 20:
                writer_result = summary_writer.run_sync(f"""
                    Your task is to craft a short 20 word summary of the chapter text that will allow an AI to generate an image that reflects the chapter's content.
                    Chapter Text: {chapter}""")
                summary.write(f"{writer_result.data}\n")
                summary.write(f"###########################\n\n")
                summary.flush()
    except Exception as e:
        print(f"An error occurred: {e}")
