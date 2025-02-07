import os
import re

def extract_explanations(formatted_file):
    """ Extracts question-explanation pairs from formatted_output.txt. """
    if not os.path.exists(formatted_file):
        print("Error: formatted_output.txt not found.")
        return {}

    with open(formatted_file, "r", encoding="utf-8") as file:
        content = file.read()

    # Splitting based on "question_"
    sections = re.split(r"(question_.*?\n)", content)  # Keeps "question_" in results
    explanation_dict = {}

    current_question = None
    for section in sections:
        section = section.strip()
        if section.startswith("question_"):
            current_question = section.replace("question_", "").strip()
        elif current_question:
            # Extract explanation if it exists
            explanation_match = re.search(r"Explanation_(.*)", section, re.DOTALL)
            if explanation_match:
                explanation_dict[current_question] = explanation_match.group(1).strip()
            current_question = None  # Reset for next question

    return explanation_dict

def append_explanations(options_file, formatted_file, final_output):
    """ Reads optionsAdded.txt, finds matching explanations, and appends them correctly. """
    if not os.path.exists(options_file):
        print("Error: optionsAdded.txt not found.")
        return

    explanations = extract_explanations(formatted_file)
    final_lines = []
    current_question = None

    with open(options_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        stripped_line = line.strip()
        final_lines.append(stripped_line + "\n")  # Preserve original formatting

        if stripped_line.startswith("question_"):
            current_question = stripped_line.replace("question_", "").strip()
        elif stripped_line.startswith("D_") and current_question in explanations:
            # Append explanation after D_
            final_lines.append(f"Explanation_{explanations[current_question]}\n")

    # Save final file
    with open(final_output, "w", encoding="utf-8") as file:
        file.writelines(final_lines)

    print(f"Final file with explanations saved to {final_output}")

# Example usage:
append_explanations("optionsAdded.txt", "formatted_output.txt", "final_with_explanations.txt")
