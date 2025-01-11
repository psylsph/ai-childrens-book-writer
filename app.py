from matplotlib import use
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.models.openai import OpenAIModel
import os
from dotenv import load_dotenv
load_dotenv()

#GROQ_API_KEY = os.getenv("GROQ_API_KEY")
#model = GroqModel('llama-3.1-70b-versatile', api_key=GROQ_API_KEY)
#writer_model = GroqModel('mixtral-8x7b-32768', api_key=GROQ_API_KEY)

# DEEPSEEK_API_KEY= os.getenv("DEEPSEEK_API_KEY")

# model = OpenAIModel(
#     'deepseek-chat',
#     base_url='https://api.deepseek.com/v1',
#     api_key=DEEPSEEK_API_KEY,
# )

# GEMINI_API_KEY= os.getenv("GEMINI_API_KEY")
# model = GeminiModel('gemini-1.5-exp', api_key=GEMINI_API_KEY)

#default_model= model
#writer_model = model

# dolphin-mistral7b-12k
# unsensored-mistral-v03-7b-12k
OLLAMA_API_KEY= os.getenv("OLLAMA_API_KEY")
default_model = OpenAIModel(
     "darkest-muse-v1",
     base_url='http://192.168.1.5:1234/v1',
     api_key=OLLAMA_API_KEY,
 )

OLLAMA_API_KEY= os.getenv("OLLAMA_API_KEY")
writer_model = OpenAIModel(
     "darkest-muse-v1",
     base_url='http://192.168.1.5:1234/v1',
     api_key=OLLAMA_API_KEY,
)

num_chapters = 25
use_existing_plan = False
childrens_story = False

idea = "ideas/unit985.md"

initial_prompt = open(idea, mode="r", encoding='utf-8').read()
if initial_prompt.capitalize().startswith("CHILDREN BOOK"):
    print("Children's story detected")
    childrens_story = True

plan_name = f"book_output/plan.md"

if (use_existing_plan):
    print(f"Using existing plan: {plan_name}")
    planner_result = open(plan_name, mode="r", encoding='utf-8').read()
else:
    try:

        planner = Agent(  
            default_model,
            result_type=str,
            system_prompt=(f"""Prompt: Generate a detailed outline for a novel with exactly {num_chapters} chapters.

                    Instructions:
                    1. YOU MUST USE EXACTLY THIS FORMAT FOR EACH CHAPTER - NO DEVIATIONS.
                    2. Ensure that every field is filled out completely and accurately for each chapter.
                    3. Do not deviate from the structure or add any additional text outside the specified format.
                    4. All characters MUST be over the age of 18.
                    
                    Required Format for Each Chapter Plan:
                    
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

                    [REPEAT THIS EXACT FORMAT FOR ALL {num_chapters} CHAPTERS]

                    Requirements:
                    1. EVERY chapter MUST have AT LEAST 3 Key Events
                    2. EVERY chapter MUST have AT LEAST 3 Scenes
                    3. ALL chapters MUST be detailed - NO placeholders
                    4. Format MUST match EXACTLY - including all headings and bullet points

                    Novel Premise:
                    {initial_prompt}

                    Final Instruction:
                    1. DO NOT include any explanations or narratives outside the outline format.
                    2. ADHERE STRICTLY to the format and requirements outlined above.
                    
                    Additional Notes:
                    - Take your time with each chapter plan, ensuring that it meets all the guidelines and requirements."""),
            retries=5)

        planner_result = planner.run_sync(f'Generate a comprehensive outline for a novel using {initial_prompt} with exactly {num_chapters} chapters.').data
        open(file=plan_name, mode="w", encoding='utf-8').write(planner_result)
        print(planner_result)
    except Exception as e:
        print(f"An error occurred: {e}")
    
book_name_raw = f"book_output/book_raw.md"

writer = Agent(  
    writer_model,
    result_type=str,
    system_prompt=(f"""Prompt:
            Role: You are a highly skilled creative writer with a talent for bringing scenes to life through vivid descriptions and engaging prose.
            Your task is to write a complete chapter of the novel based on the provided outline.
            The chapter should be written in a way that is engaging, descriptive, and true to the outlined plot points.
            
            Novel Premise:
            {initial_prompt}
            
            Guidelines:
            1. Adhere to the Outline: Ensure that each chapter follows the outlined plot points closely, staying true to the story's direction.
            2. Character Consistency: Maintain consistent and authentic character voices throughout the chapter. Each character should be distinct and true to their established personalities.
            3. World-Building: Incorporate detailed descriptions of the setting and environment to enrich the world-building. This should enhance the reader's immersion without slowing down the pace of the narrative.
            4. Engaging Prose: Write in a style that is both engaging and descriptive, drawing the reader into the scene and making it feel real.
            5. Complete Scenes: Make sure that each chapter is a complete narrative unit with a clear beginning, middle, and end. Do not leave scenes hanging or unresolved.
            6. Word Count Requirement: Each chapter MUST be at least 3000 words (30000 characters). This is a hard requirement. Do not end the chapter until this requirement is met.
            7. Smooth Transitions: Ensure that transitions between scenes and chapters are smooth and logically flowing, maintaining the story's momentum.
            8. Detailed Descriptions: Add detailed descriptions of the environment and characters where appropriate, but avoid info-dumping. Balance is key.
            9. Reference the Outline and Previous Content: Always refer back to the plot outline and previous chapters to maintain consistency and continuity.

            Final Instruction:
            - Take your time with each chapter, ensuring that it meets all the guidelines above.
            - DO NOT include any explanations or narratives about your work."""),
    retries=5)

print(f"#################Generating Chapters#######################\n")

raw_chapters = []

with open(book_name_raw, "w", encoding='utf-8') as book:
    try:
        chapter_outlines = planner_result.split(r"**Chapter ")
        if len(chapter_outlines) < num_chapters:
            chapter_outlines = planner_result.split(r"Chapter ")
            if len(chapter_outlines) < num_chapters:
                raise ValueError("Not enough chapters in the outline")
            else:
                print(f"Found {len(chapter_outlines)-1} chapters in the outline\n")
        
        for chapter_num in range(1, num_chapters+1):
            chapter_text = "**Chapter " + chapter_outlines[chapter_num]
            print(f"{chapter_text}")
            print(f"#########################\n")
            writer_result = writer.run_sync(f"""
                 For the chapter outlined in the following Chapter Outline please write 3000 words covering all the details from the chapter plan.
                 Ensure each of the scene with the chapter flows from one to the next.
                 If you first attempt at writing the chapter does not have 3000 words try again.
                 Your response MUST only include text for THIS chapter.
                 Chapter Outline: {chapter_text}""")
            print(writer_result.data)
            book.write(writer_result.data + "\n")
            book.flush()
            print(f"#######################################################\n")
            raw_chapters.append(writer_result.data)
    except Exception as e:
        print(f"An error occurred: {e}")
    
human_editor = Agent(  
    writer_model,
    result_type=str,
    system_prompt=(f"""Prompt:
            Role: You are a highly skilled book editor with a talent proof reading chapters from novels and ensuring the text is humanized.
            Your task is to check the chapter text, fix any errors, and ensuring the story flows well in an engaging manner."""),
    retries=5)

book_name_edited = f"book_output/book_edited.md"

print(f"#################Editing Chapters#######################\n")

with open(book_name_edited, "w", encoding='utf-8') as book:
    try:
        for chapter_text in raw_chapters:

            print(f"#########################\n")

            if (childrens_story):
                human_editor_result = human_editor.run_sync(f"""
                    Ensure the content of the chapter is suitable for children, then proof read and humanize following text from an extract of a novel.
                    Chapter Text: {chapter_text}""")
            else:
                human_editor_result = human_editor.run_sync(f"""
                    Proof read and humanize the following text from an extract of a novel.
                    Chapter Text: {chapter_text}""")
                
            print(human_editor_result.data)
            book.write(human_editor_result.data + "\n")
            book.flush()
            print(f"#######################################################\n")
    except Exception as e:
        print(f"An error occurred: {e}")
    
#chapter_text = open(book_name,).read().split("Chapter ")

# summary_writer = Agent(  
#     default_model,
#     result_type=str,
#     system_prompt=(f"""Prompt:
#             Role: You are a highly skilled creative artist with a talent for bringing scenes to life through vivid descriptions and engaging prose."""),
#     retries=1)

# with open(f"summary.md", "w", encoding='ascii') as summary:
#     try: 
#         for chapter in chapter_text:
#             # ingore short lines it means the split messed up the first split
#             if len(chapter) > 20:
#                 writer_result = summary_writer.run_sync(f"""
#                     Your task is to craft a short 20 word summary of the chapter text that will allow an AI to generate an image that reflects the chapter's content.
#                     Chapter Text: {chapter}""")
#                 summary.write(f"{writer_result.data}\n")
#                 summary.write(f"###########################\n\n")
#                 summary.flush()
#     except Exception as e:
#         print(f"An error occurred: {e}")
