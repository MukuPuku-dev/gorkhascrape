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
IMAGE_HEIGHT = 800  # Height of the image
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

def create_html_content(question, options, style_choice, correct_answer):
    logo_path = os.path.abspath(os.path.join("assets", "loksewa_automatic_logo.jpg"))
    
    html_content = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>{get_style(style_choice)}</style></head><body>"""
    if style_choice == "15":  # KBC Style
        html_content += f"""
        <div class="container">
            <div class="logo-container" align="center">
                <img src="file:///{logo_path}" alt="App Logo" class="logo" />
            </div>
           
            <div class="question">{question}</div>
            <hr />
            <table class="options">
                <tr>
                    <td><div class="option"><span class="option-label">A:</span> {options[0]}</div></td>
                    <td><div class="option"><span class="option-label">B:</span> {options[1]}</div></td>
                </tr>
                <tr>
                    <td><div class="option"><span class="option-label">C:</span> {options[2]}</div></td>
                    <td><div class="option"><span class="option-label">D:</span> {options[3]}</div></td>
                </tr>
            </table>
        </div>
        """
    elif column_choice == "2":  # KBC
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
   
    # Add a small message encouraging the user to comment to receive the correct answer
    html_content += f"""<div style="font-size: 10px; text-align: right;">Comment your answer to get the correct answer in inbox!</div>"""
    html_content += "</body></html>"  # Close the HTML tags here
    return html_content

def extract_questions_and_answers(file_path):
    questions_and_answers = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    current_question = None
    current_options = []
    correct_answer = None

    for line in lines:
        line = line.strip()
        if line.startswith("question_"):
            if current_question and len(current_options) == 4:
                random.shuffle(current_options)
                questions_and_answers.append((current_question, current_options, correct_answer))
            current_question = line.replace("question_", "").strip()
            current_options = []
            correct_answer = None
        elif line.startswith("A_") or line.startswith("B_") or line.startswith("C_") or line.startswith("D_"):
            option = line.replace("A_", "").replace("B_", "").replace("C_", "").replace("D_", "").strip()
            current_options.append(option)
            if line.startswith("A_"):
                correct_answer = "A"
            elif line.startswith("B_"):
                correct_answer = "B"
            elif line.startswith("C_"):
                correct_answer = "C"
            elif line.startswith("D_"):
                correct_answer = "D"

    if current_question and len(current_options) == 4:
        random.shuffle(current_options)
        questions_and_answers.append((current_question, current_options, correct_answer))

    return questions_and_answers

def generate_images_from_file(file_path):
    questions_and_answers = extract_questions_and_answers(file_path)
    image_number = 1

    for question, options, correct_answer in questions_and_answers:
        html_content = create_html_content(question, options, style_choice, correct_answer)    
              
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
