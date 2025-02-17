import random
import imgkit
import os

# Constants
INPUT_FILE = 'QAonly.txt'
OUTPUT_IMAGE_PREFIX = 'output_image'
OUTPUT_FOLDER = 'output_images'  # Folder name updated to Images_MCQ
FONT_NAME = 'Kalimati'  # Use installed font name
FONT_SIZE = 30
IMAGE_WIDTH = 900
MARGIN = 50
MAX_QUESTIONS_PER_IMAGE = 1  # One question per image
TEXT_WIDTH = IMAGE_WIDTH - 2 * MARGIN

# Create output folder if it doesn't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Ask user to choose a style
styles = {
    "1": "Classic",
    "2": "Modern",
    "3": "Minimalist",
    "4": "Playful",
    "5": "Elegant",
    "6": "Dark Mode",
    "7": "Newspaper",
    "8": "Tech",
    "9": "Handwritten",
    "10": "Royal",
    "11": "Retro",
    "12": "Gradient",
    "13": "KBC"  # Added KBC style
}

print("Choose a style for your question-answer format:")
for key, value in styles.items():
    print(f"{key}. {value}")

style_choice = input("Enter the style number (1-12): ").strip()
column_choice = input("Choose column type:\n1. Single Column\n2. Two Columns\nEnter 1 or 2: ").strip()

# Define different CSS styles
def get_style(style_choice):
    if style_choice == "1":  # Classic
        return """
        body { font-family: 'Kalimati', sans-serif; font-size: 30px; color: #333; background: #fff; }
        .question { font-weight: bold; color: black; margin-bottom: 10px; }
        .option { font-style: italic; color: #555; margin-bottom: 20px; }
        hr { border: 1px solid #ccc; }
        """
    elif style_choice == "2":  # Modern
        return """
        body { font-family: 'Kalimati', sans-serif; font-size: 30px; background: #f8f9fa; padding: 20px; }
        .container { background: white; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1); }
        .question { font-weight: bold; font-size: 36px; color: #007bff; border-left: 5px solid #007bff; padding-left: 15px; background: #e9f2ff; margin-bottom: 10px; padding: 10px; border-radius: 5px; }
        .option { font-size: 32px; color: #28a745; font-style: italic; background: #ebfbee; padding: 10px; margin-bottom: 20px; border-radius: 5px; }
        hr { border: none; height: 2px; background: linear-gradient(to right, #ddd, #bbb, #ddd); margin: 20px 0; }
        """
    elif style_choice == "3":  # Minimalist
        return """
        body { font-family: 'Kalimati', sans-serif; font-size: 30px; background: #fff; color: #222; text-align: center; }
        .question { font-weight: bold; font-size: 34px; color: #000; margin-bottom: 10px; }
        .option { font-size: 30px; color: #444; margin-bottom: 20px; }
        hr { border-top: 1px solid #ddd; }
        """
    elif style_choice == "4":  # Playful
        return """
        body { font-family: 'Kalimati', sans-serif; font-size: 30px; background: #ffefd5; }
        .question { font-weight: bold; font-size: 34px; color: #ff4500; background: #ffd700; padding: 10px; border-radius: 10px; }
        .option { font-size: 30px; color: #008000; font-style: italic; background: #adff2f; padding: 10px; border-radius: 10px; }
        hr { border-top: 2px dashed #ff4500; }
        """
    elif style_choice == "5":  # Elegant
        return """
        body { font-family: 'Kalimati', serif; font-size: 30px; background: #f3e5ab; color: #333; }
        .question { font-weight: bold; font-size: 36px; color: #b8860b; border-bottom: 2px solid #b8860b; margin-bottom: 10px; }
        .option { font-size: 32px; color: #6b4226; font-style: italic; }
        hr { border-top: 2px solid #b8860b; }
        """
    elif style_choice == "6":  # Dark Mode
        return """
        body { font-family: 'Kalimati', sans-serif; font-size: 30px; background: #222; color: #fff; }
        .question { font-weight: bold; font-size: 34px; color: #ffcc00; border-left: 4px solid #ffcc00; padding-left: 10px; }
        .option { font-size: 30px; color: #0ff; font-style: italic; }
        hr { border-top: 1px solid #666; }
        """
    elif style_choice == "7":  # Newspaper
        return """
        body { font-family: 'Times New Roman', serif; font-size: 30px; background: #f4f4f4; color: #333; }
        .question { font-weight: bold; font-size: 34px; color: black; text-decoration: underline; }
        .option { font-size: 30px; color: #444; font-style: italic; }
        hr { border-top: 1px dashed black; }
        """
    elif style_choice == "8":  # Tech
        return """
        body { font-family: 'Kalimati', sans-serif; font-size: 30px; background: #001f3f; color: #0ff; text-shadow: 0px 0px 5px #0ff; }
        .question { font-weight: bold; font-size: 34px; color: #0ff; border-left: 4px solid #0ff; padding-left: 10px; }
        .option { font-size: 30px; color: #39ff14; font-style: italic; }
        hr { border-top: 1px solid #0ff; }
        """
    elif style_choice == "9":  # Handwritten
        return """
        body { font-family: 'Patrick Hand', cursive; font-size: 30px; background: #f9f4dc; color: #5a4231; }
        .question { font-weight: bold; font-size: 34px; color: #3e2723; background: #fff8e1; padding: 10px; border-radius: 10px; border: 2px dashed #795548; }
        .option { font-size: 30px; color: #5d4037; font-style: italic; background: #ffecb3; padding: 10px; border-radius: 10px; }
        hr { border-top: 2px dashed #795548; }
        """
    elif style_choice == "10":  # Royal
        return """
        body { font-family: 'Kalimati', serif; font-size: 30px; background: #4b0082; color: #ffd700; }
        .question { font-weight: bold; font-size: 36px; color: #ffd700; border-bottom: 2px solid #ffd700; margin-bottom: 10px; }
        .option { font-size: 32px; color: #dda0dd; font-style: italic; }
        hr { border-top: 2px solid #ffd700; }
        """
    elif style_choice == "11":  # Retro
        return """
        body { font-family: 'Press Start 2P', cursive; font-size: 20px; background: #ffcc00; color: #000; }
        .question { font-weight: bold; font-size: 24px; color: #ff0000; background: #fff; padding: 5px; border-radius: 5px; }
        .option { font-size: 22px; color: #0000ff; font-style: italic; background: #fff; padding: 5px; border-radius: 5px; }
        hr { border-top: 2px dashed #000; }
        """
    elif style_choice == "12":  # Eye-Catching Gradient
        return """
        body { font-family: 'Kalimati', sans-serif; font-size: 32px; background: linear-gradient(135deg, #ff6a00, #ee0979, #00c9ff, #92fe9d); color: #fff; text-align: center; margin: 0; padding: 20px; }
        .container { max-width: 900px; margin: auto; padding: 20px; border-radius: 15px; background: rgba(0, 0, 0, 0.6); box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3); }
        .question { font-weight: bold; font-size: 36px; color: #fff; background: linear-gradient(45deg, #ff4e50, #fc913a); padding: 15px; border-radius: 15px; text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3); }
        .option { font-size: 32px; color: #fff; font-style: italic; background: linear-gradient(45deg, #1f4037, #99f2c8); padding: 15px; border-radius: 15px; }
        hr { border: 4px solid #fff; border-radius: 5px; margin-top: 20px; }
        """

    elif style_choice == "13":  # KBC
        return """
        body { font-family: 'Kalimati', sans-serif; background: #000; color: #ffd700; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .container { background: rgba(0, 0, 0, 0.7); padding: 30px; border-radius: 10px; width: 80%; max-width: 900px; }
        .question { font-size: 36px; font-weight: bold; margin-bottom: 20px; text-align: center; }
        .options { width: 100%; border-collapse: collapse; }
        .options td { padding: 15px; text-align: center; }
        .option { background: #222; border-radius: 5px; cursor: pointer; transition: background 0.3s ease; font-size: 32px; display:inline-block; width:100%;}
        .option:hover { background: #444; }
        hr { border-top: 1px solid #666; margin-top: 30px; }
        """
    else:  # Default to Classic if an invalid choice is entered
        return get_style("1")
    

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
