import requests
import re
import json
import os

SERVER_URL_POST = "https://capricious-dorian-macaroni.glitch.me/postmultipleImages"
SERVER_URL_COMMENTS = "https://capricious-dorian-macaroni.glitch.me/makeComments"

QA_FILE = "QAonly.txt"
IDS_FILE = "ids.txt"
IMAGE_FOLDER = "output_images"

PAGE_ACCESS_TOKEN = "YOUR_PAGE_ACCESS_TOKEN"  # Replace with actual token


def extract_answers(filepath):
    """Extracts answers from QAonly.txt (for comments)"""
    answers = []
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        matches = re.findall(r"A_([^\n]+)\n", content)
        for match in matches:
            answers.append("ans " + match.strip())
    return answers


def extract_captions(filepath):
    """Extracts captions from QAonly.txt (for image posts)"""
    captions = []
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        matches = re.findall(r"question_(.*?)A_", content, re.DOTALL)
        for match in matches:
            captions.append(match.strip())
    return captions


def extract_image_ids():
    """Extracts image IDs from ids.txt"""
    if not os.path.exists(IDS_FILE):
        print(f"File {IDS_FILE} not found. No images to attach.")
        return None, []

    with open(IDS_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    post_id = None
    image_ids = []

    for line in lines:
        line = line.strip()
        if line.startswith("Post ID:"):
            post_id = line.split(": ")[1]
        elif line and not line.startswith("Image IDs:"):
            image_ids.append(line)

    if not post_id:
        print("Post ID not found in ids.txt.")
    return post_id, image_ids


def get_image_files():
    """Gets all image files from the 'output_images' folder"""
    if not os.path.exists(IMAGE_FOLDER):
        print(f"Folder '{IMAGE_FOLDER}' not found.")
        return []

    image_extensions = {".jpg", ".jpeg", ".png", ".gif"}  # Allowed extensions
    image_files = sorted(
    [
        os.path.join(IMAGE_FOLDER, f)
        for f in os.listdir(IMAGE_FOLDER)
        if os.path.splitext(f)[1].lower() in image_extensions
    ],
    key=lambda x: int(re.search(r'\d+', x).group())  # Extract number and sort numerically
)

    if not image_files:
        print("No images found in 'output_images'.")
    
    return image_files


def post_images():
    """Handles posting images with or without captions."""
    captions_option = input("Post with captions? (yes/no): ").strip().lower()

    captions = []
    if captions_option == "yes":
        captions = extract_captions(QA_FILE)  # Extract captions from QAonly.txt
    else:
        captions = []  # No captions will be sent

    image_paths = get_image_files()
    if not image_paths:
        print("No images found to upload.")
        return

    files = [("images", (os.path.basename(img), open(img, "rb"), "image/jpeg")) for img in image_paths]

    data = {}
    if captions:
        data["captions"] = json.dumps(captions)
        print("Captions:", captions)

    response = requests.post(SERVER_URL_POST, files=files, data=data)

    if response.status_code == 200:
        res_json = response.json()
        post_id = res_json.get("postId")
        image_ids = res_json.get("image_ids", [])

        with open(IDS_FILE, "w") as file:
            file.write(f"Post ID: {post_id}\n")
            file.write("Image IDs:\n")
            for img_id in image_ids:
                file.write(f"{img_id}\n")

        print("Images posted successfully!")
        print(f"Post ID: {post_id}")
        print(f"Image IDs: {image_ids}")
    else:
        print("Error posting images:", response.text)


def post_all_comments():
    """Handles posting comments with or without image IDs."""
    comment_option = input("Attach image IDs to comments? (yes/no): ").strip().lower()

    answers = extract_answers(QA_FILE)
    if not answers:
        print("No answers found to comment.")
        return

    post_id, image_ids = extract_image_ids()

    if not post_id:
        print("Cannot proceed without a post ID.")
        return

    data = {
        "POST_ID": post_id,
        "answers": answers,
        "pageAccessToken": PAGE_ACCESS_TOKEN,
    }

    if comment_option == "yes" and image_ids:
        data["image_ids"] = image_ids

    response = requests.post(SERVER_URL_COMMENTS, json=data)

    if response.status_code == 200:
        print("Answers sent successfully!")
        print(response.json())
    else:
        print("Error sending comments:", response.text)


if __name__ == "__main__":
    choice = input("Do you want to post images or make comments? (images/comments): ").strip().lower()

    if choice == "images":
        post_images()
    elif choice == "comments":
        post_all_comments()
    else:
        print("Invalid choice. Please enter 'images' or 'comments'.")
