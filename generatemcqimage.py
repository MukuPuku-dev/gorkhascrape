import random
import imgkit
import os
from styles_module import styles, get_style
# Constants
INPUT_FILE = 'QAonly.txt'
OUTPUT_IMAGE_PREFIX = 'output_image'
OUTPUT_FOLDER = 'output_images'  # Folder name updated to Images_MCQ
FONT_NAME = 'Kalimati'  # Use installed font name
FONT_SIZE = 30
IMAGE_WIDTH = 1000
MARGIN = 50
MAX_QUESTIONS_PER_IMAGE = 1  # One question per image
TEXT_WIDTH = IMAGE_WIDTH - 2 * MARGIN

# Create output folder if it doesn't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Ask user to choose a style

print("Choose a style for your question-answer format:")
for key, value in styles.items():
    print(f"{key}. {value}")

style_choice = input("Enter the style number (1-12): ").strip()
column_choice = input("Choose column type:\n1. Single Column\n2. Two Columns\nEnter 1 or 2: ").strip()

# Define different CSS styles

def create_html_content(question, options, style_choice):
    html_content = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>{get_style(style_choice)}</style></head><body>"""

    if column_choice == "2":  # KBC
        html_content += f"""
        <div class="container">
            <div class="question">{question}</div>
            <hr />
            <table class="options" style="width: 100%; border-collapse: collapse;">
                <tr>
                    {''.join([f'<td><div class="option">{chr(65 + idx)}. {option}</div></td>' for idx, option in enumerate(options[:2])])}
                </tr>
                <tr>
                    {''.join([f'<td><div class="option">{chr(65 + idx + 2)}. {option}</div></td>' for idx, option in enumerate(options[2:])])}
                </tr>
            </table>
        </div>
        """
    else:  # Default (or your existing 1-12 styles) - Important!
        html_content += f"""
        <div class="container">
            <div class="question">{question}</div>
            {''.join([f'<div class="option">{chr(65 + idx)}. {option}</div>' for idx, option in enumerate(options)])}
        </div>
        """

    html_content += "</body></html>"  # Close the HTML tags here
    return html_content

def extract_questions_and_answers(file_path):
    questions_and_answers = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    current_question = None
    current_options = []

    for line in lines:
        line = line.strip()
        if line.startswith("question_"):
            if current_question and len(current_options) == 4:
                random.shuffle(current_options)
                questions_and_answers.append((current_question, current_options))
            current_question = line.replace("question_", "").strip()
            current_options = []
        elif line.startswith("A_") or line.startswith("B_") or line.startswith("C_") or line.startswith("D_"):
            current_options.append(line.replace("A_", "").replace("B_", "").replace("C_", "").replace("D_", "").strip())

    if current_question and len(current_options) == 4:
        random.shuffle(current_options)
        questions_and_answers.append((current_question, current_options))

    return questions_and_answers

def generate_images_from_file(file_path):
    questions_and_answers = extract_questions_and_answers(file_path)
    image_number = 1

    for question, options in questions_and_answers:
        html_content = create_html_content(question, options, style_choice)    
              
        output_path = os.path.join(OUTPUT_FOLDER, f"{OUTPUT_IMAGE_PREFIX}_{image_number}.jpg")
        
        options = {
            'encoding': 'UTF-8',
            'quality': 100,
            'width': IMAGE_WIDTH,
            'enable-local-file-access': ''  # Ensure access to system fonts
        }

        try:
            # Generate the image from HTML content
            imgkit.from_string(html_content, output_path, options=options)
            print(f"Saved image: {OUTPUT_IMAGE_PREFIX}_{image_number}.jpg")
        except Exception as e:
            print(f"Error generating image: {e}")

        # Increment the image number for the next image
        image_number += 1


# Run the program
generate_images_from_file(INPUT_FILE)
