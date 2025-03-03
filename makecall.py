import requests
import re
import json
import os
import time

SERVER_URL_POST = "https://capricious-dorian-macaroni.glitch.me/postmultipleImages"
SERVER_URL_COMMENTS = "https://capricious-dorian-macaroni.glitch.me/makeComments"

QA_FILE = "QAonly.txt"
IDS_FILE = "ids.txt"
IMAGE_FOLDER = "output_images"

PAGE_ACCESS_TOKEN = "YOUR_PAGE_ACCESS_TOKEN"  # Replace with actual token

MAX_IMAGES_PER_BATCH = 60  # Maximum number of images to send in a single request

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
        key=lambda x: int(re.search(r"\d+", x).group())  # Extract number and sort numerically
    )

    if not image_files:
        print("No images found in 'output_images'.")

    return image_files


def post_images():
    """Handles posting images in batches with or without captions."""
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

    total_images = len(image_paths)
    print(f"Found {total_images} images to upload.")

    all_image_ids = []  # Store all image IDs from all batches
    all_post_ids = [] #store all post ids
    for i in range(0, total_images, MAX_IMAGES_PER_BATCH):
        # Process images in batches
        batch_image_paths = image_paths[i:i + MAX_IMAGES_PER_BATCH]
        print(f"Processing batch {int(i/MAX_IMAGES_PER_BATCH)+1} of images from index {i} to {min(i + MAX_IMAGES_PER_BATCH,total_images)}")
        
        files = [("images", (os.path.basename(img), open(img, "rb"), "image/jpeg")) for img in batch_image_paths]
        data = {}

        if captions:
          # Adjust captions for the current batch
            batch_captions = captions[i:i + MAX_IMAGES_PER_BATCH]
            data["captions"] = json.dumps(batch_captions)
            print("Captions:", batch_captions)

        try:
          response = requests.post(SERVER_URL_POST, files=files, data=data)
          response.raise_for_status()
        except requests.exceptions.RequestException as e:
          print(f"Error posting image batch: {e}")
          continue

        if response.status_code == 200:
            res_json = response.json()
            post_id = res_json.get("postId")
            image_ids = res_json.get("image_ids", [])
            
            all_post_ids.append(post_id)
            all_image_ids.extend(image_ids) #add this line
            print(f"Batch posted successfully! Post ID: {post_id}")
            print(f"Image IDs in this batch: {image_ids}")

        else:
            print(f"Error posting image batch: {response.text}")
        time.sleep(5)

    # Save all image IDs to ids.txt (outside the loop)
    if all_post_ids:
        with open(IDS_FILE, "w") as file:
            
            file.write("Post IDs:\n")
            for p_id in all_post_ids:
                file.write(f"{p_id}\n")

            file.write("\nImage IDs:\n")
            unique_image_ids = list(set(all_image_ids)) # remove duplicates.
            for img_id in unique_image_ids:
                file.write(f"{img_id}\n")

        print(f"All {len(unique_image_ids)} unique image IDs saved to {IDS_FILE}")
    else:
      print("No Images was able to upload")

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
