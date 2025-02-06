from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

# Constants
INPUT_FILE = 'formatted_output.txt'
OUTPUT_IMAGE_PREFIX = 'output_image'
OUTPUT_FOLDER = 'output_images'
FONT_PATH = 'NotoSansDevanagari-Regular.ttf'  # Path to a Nepali Unicode font file
FONT_SIZE = 30
IMAGE_WIDTH = 1000
IMAGE_HEIGHT = 1400
LINE_SPACING = 40
MARGIN = 50
MAX_QUESTIONS_PER_IMAGE = 5

# Create output folder if it doesn't exist
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Load font
try:
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
except IOError:
    print(f"Error: Font file '{FONT_PATH}' not found. Please provide a valid Nepali Unicode font.")
    exit()

def extract_questions_and_answers(file_path):
    """
    Extract questions and answers from the formatted text file.
    Returns a list of tuples: [(question, answer), ...]
    """
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

def wrap_text(text, max_width):
    """
    Wrap text into multiple lines based on the max width.
    """
    wrapper = textwrap.TextWrapper(width=max_width)
    return wrapper.wrap(text)

def create_image_with_questions(questions_and_answers, image_number):
    """
    Create an image with a list of questions and answers.
    """
    image = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    y = MARGIN
    for idx, (question, answer) in enumerate(questions_and_answers):
        # Draw question
        question_text = f"{idx + 1}. {question}"
        wrapped_question = wrap_text(question_text, max_width=80)  # Wrap text
        for line in wrapped_question:
            draw.text((MARGIN, y), line, font=font, fill=(0, 0, 0))
            y += LINE_SPACING

        # Draw answer
        answer_text = f"   उत्तर: {answer}"
        wrapped_answer = wrap_text(answer_text, max_width=80)  # Wrap text
        for line in wrapped_answer:
            draw.text((MARGIN, y), line, font=font, fill=(0, 0, 0))
            y += LINE_SPACING

        y += LINE_SPACING  # Extra spacing between Q&A pairs

    # Save the image
    output_path = os.path.join(OUTPUT_FOLDER, f"{OUTPUT_IMAGE_PREFIX}_{image_number}.png")
    image.save(output_path)
    print(f"Saved image: {output_path}")

def generate_images_from_file(file_path):
    """
    Generate images from the formatted text file.
    """
    questions_and_answers = extract_questions_and_answers(file_path)

    # Split questions and answers into chunks of MAX_QUESTIONS_PER_IMAGE
    for i in range(0, len(questions_and_answers), MAX_QUESTIONS_PER_IMAGE):
        chunk = questions_and_answers[i:i + MAX_QUESTIONS_PER_IMAGE]
        image_number = (i // MAX_QUESTIONS_PER_IMAGE) + 1
        create_image_with_questions(chunk, image_number)

# Run the program
generate_images_from_file(INPUT_FILE)