import imgkit
import pdfkit     # added import for pdf generation
import os
from styles_module import styles, get_style
# Constants
INPUT_FILE = 'formatted_output.txt'
OUTPUT_IMAGE_PREFIX = 'output_image'
OUTPUT_FOLDER = 'output_images'
FONT_SIZE = 30
IMAGE_WIDTH = 1000
MARGIN = 50
MAX_QUESTIONS_PER_IMAGE = 5
TEXT_WIDTH = IMAGE_WIDTH - 2 * MARGIN

# Create output folder if it doesn't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
# Ask user to choose a style
print("Choose a style for your question-answer format:")
for key, value in styles.items():
    print(f"{key}. {value}")
style_choice = input("Enter the style number (1-12): ").strip()

# Ask the user what to generate: 1 for images only, 2 for PDF only, 3 for both.
print("Select output type:")
print("1. Images only")
print("2. PDF only")
print("3. Both images and PDF")
output_choice = input("Enter your choice (1/2/3): ").strip()

def create_html_content(questions_and_answers, style_choice):
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <style>
    {get_style(style_choice)}
    </style>
    </head>
    <body>
    <div class="container">
    """
    for idx, (question, answer) in enumerate(questions_and_answers):
        html_content += f'<div class="question"><span class="question-number">{idx + 1}.</span> {question}</div>\n'
        html_content += f'<div class="answer">उत्तर: {answer}</div>\n'
        if idx < len(questions_and_answers) - 1:
            html_content += "<hr>"
    html_content += """
    </div>
    </body>
    </html>
    """
    return html_content

def extract_questions_and_answers(file_path):
    questions_and_answers = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    current_question = None
    current_answer = None

    for line in lines:
        line = line.strip()
        if line.startswith("question_"):
            current_question = line.replace("question_", "").strip()
        elif line.startswith("A_"):
            current_answer = line.replace("A_", "").strip()
            if current_question and current_answer:
                questions_and_answers.append((current_question, current_answer))
                current_question = None
                current_answer = None

    return questions_and_answers

def generate_images_from_file(file_path):
    questions_and_answers = extract_questions_and_answers(file_path)
    image_number = 1
    current_questions = []

    for question_and_answer in questions_and_answers:
        current_questions.append(question_and_answer)
        if len(current_questions) == MAX_QUESTIONS_PER_IMAGE:
            html_content = create_html_content(current_questions, style_choice)
            output_path = os.path.join(OUTPUT_FOLDER, f"{OUTPUT_IMAGE_PREFIX}_{image_number}.jpg")
            options = {
                'encoding': 'UTF-8',
                'quality': 100,
                'width': IMAGE_WIDTH,
                'enable-local-file-access': ''  # Ensure access to system fonts
            }
            try:
                imgkit.from_string(html_content, output_path, options=options)
                print(f"Saved image: {OUTPUT_IMAGE_PREFIX}_{image_number}.jpg")
            except Exception as e:
                print(f"Error generating image: {e}")
            image_number += 1
            current_questions = []
    # Handle any remaining questions
    if current_questions:
        html_content = create_html_content(current_questions, style_choice)
        output_path = os.path.join(OUTPUT_FOLDER, f"{OUTPUT_IMAGE_PREFIX}_{image_number}.jpg")
        options = {
            'encoding': 'UTF-8',
            'quality': 100,
            'width': IMAGE_WIDTH,
            'enable-local-file-access': ''
        }
        try:
            imgkit.from_string(html_content, output_path, options=options)
            print(f"Saved image: {OUTPUT_IMAGE_PREFIX}_{image_number}.jpg")
        except Exception as e:
            print(f"Error generating image: {e}")

# Generate based on user's choice
if output_choice == "1" or output_choice == "3":
    generate_images_from_file(INPUT_FILE)

if output_choice == "2" or output_choice == "3":
    pdf_output_path = os.path.join(OUTPUT_FOLDER, "questions.pdf")
    complete_html = create_html_content(extract_questions_and_answers(INPUT_FILE), style_choice)
    pdf_options = {
        'encoding': 'UTF-8',
        'enable-local-file-access': ''
    }
    try:
        pdfkit.from_string(complete_html, pdf_output_path, options=pdf_options)
        print("Saved PDF: questions.pdf")
    except Exception as e:
        print(f"Error generating PDF: {e}")