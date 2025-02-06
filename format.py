import re

# Open the file and read its content
with open("formatted_output.txt", "r", encoding="utf-8") as file:
    text = file.read()

# Replace 'question_***' with 'question_'
updated_text = re.sub(r'question_...', 'question_', text)

# Save the modified content back to the file
with open("formatted_output.txt", "w", encoding="utf-8") as file:
    file.write(updated_text)

print("File updated successfully!")
