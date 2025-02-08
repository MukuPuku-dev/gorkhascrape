import requests
import re
import json

def extract_answers(filepath):
    answers = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        matches = re.findall(r"A_([^\n]+)\n", content)
        for match in matches:
            answers.append("ans " + match.strip())
    # return answers[:12]  # Get only the first 12 answers
    return answers

def post_all_comments(post_id, answers, page_access_token):
    url = "https://capricious-dorian-macaroni.glitch.me/makeComments"  # Your server URL
    data = {
        "POST_ID": post_id,
        "answers": answers,  # Send all answers at once
        "pageAccessToken": page_access_token
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        print("Answers sent successfully!")
        print(response.json())
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error sending answers: {e}")
        if response.status_code != 200: # Print server error if available
            try:
                print(response.json())
            except json.JSONDecodeError:
                print(f"Server returned non-json error: {response.text}") # Print raw text if not json
        return False


if __name__ == "__main__":
    filepath = "QAonly.txt"
    post_id = "103517251052640_1019530980216348" # Replace with your Facebook post ID
    page_access_token = "YOUR_PAGE_ACCESS_TOKEN" # Replace with your Page Access Token

    answers = extract_answers(filepath)

    if answers:
        for i, answer in enumerate(answers):
            print(f"Answer {i+1}: {answer}")
        success = post_all_comments(post_id, answers, page_access_token)
        if not success:
            print("Failed to send all answers.")
    else:
        print("No answers found in the file.")