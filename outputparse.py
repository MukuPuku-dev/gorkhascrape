import os

def process_text(input_file, output_file, qa_output_file):
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: The file {input_file} does not exist.")
        return

    # Try reading the file
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except Exception as e:
        print(f"Error reading the file: {e}")
        return

    output_lines = []
    qa_lines = []
    current_question = ''
    current_answer = ''
    current_explanation = ''

    for line in lines:
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Check if the line is a question (starts with number and ends with question mark)
        if line[0].isdigit() and line.endswith('?'):
            if current_question:  # If there is a previous question, save it
                output_lines.append(f"question_{current_question[3:]}\n")
                output_lines.append(f"A_{current_answer[2:]}\n")
                output_lines.append(f"B_ C_ D_ Explanation_{current_explanation}\n")

                # Add question and answer only for QA file
                qa_lines.append(f"question_{current_question[3:]}\n")
                qa_lines.append(f"A_{current_answer[2:]}\nB_ \nC_ \nD_ \n")

            # Now, set the new question
            current_question = line
            current_answer = ''
            current_explanation = ''
        
        elif current_answer == '':  # This line should be the answer if no answer is set
            current_answer = line
        else:
            # After the answer, everything is part of the explanation
            current_explanation += line + "\n"
    
    # Add the last question-answer-explanation block
    if current_question:
        output_lines.append(f"question_{current_question[3:]}\n")
        output_lines.append(f"A_{current_answer[2:]}\n")
        output_lines.append(f"B_ C_ D_ Explanation_{current_explanation}\n")

        # Add the last question-answer block to QA file
        qa_lines.append(f"question_{current_question[3:]}\n")
        qa_lines.append(f"A_{current_answer[2:]}\nB_ \nC_ \nD_ \n")

    # Write the formatted output to the main output file
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.writelines(output_lines)
        print(f"Formatted output saved to {output_file}")
    except Exception as e:
        print(f"Error writing to file: {e}")

    # Write the questions and answers to QAonly.txt
    try:
        with open(qa_output_file, 'w', encoding='utf-8') as file:
            file.writelines(qa_lines)
        print(f"QA-only output saved to {qa_output_file}")
    except Exception as e:
        print(f"Error writing to QA-only file: {e}")

# Example usage:
process_text('output.txt', 'formatted_output.txt', 'QAonly.txt')
