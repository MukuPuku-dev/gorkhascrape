import requests
from bs4 import BeautifulSoup
import time

# Step 1: Scrape the main page to collect links
base_url = "https://gorkhapatraonline.com"
main_url = base_url + "/categories/loksewa?page=1"

try:
    response = requests.get(main_url)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Error fetching the main page: {e}")
    exit()

soup = BeautifulSoup(response.text, "html.parser")
links_list = []

# Find all 'div' with class 'item-img'
items = soup.find_all("h2", class_="item-title")

for item in items:
    link_tag = item.find("a")
    if link_tag and "लोक सेवा विशेष वस्तुगत" in link_tag.get_text():
        href = link_tag.get("href")
        full_link = href if href.startswith("http") else base_url + href
        links_list.append(full_link)

if not links_list:
    print("No links found to scrape.")
    exit()

# Display available links with numbers
print("\nFound the following links:")
for idx, link in enumerate(links_list, 1):
    print(f"{idx}: {link}")

# Get user selection
selected_links = []
while True:
    user_input = input(f"\nEnter the number of the link to scrape (1-{len(links_list)}), "
                       "or 'all' to scrape all: ").strip().lower()
    
    if user_input == 'all':
        selected_links = links_list
        break
    elif user_input.isdigit():
        choice = int(user_input)
        if 1 <= choice <= len(links_list):
            selected_links = [links_list[choice - 1]]
            break
        else:
            print(f"Please enter a number between 1 and {len(links_list)}.")
    else:
        print(f"Invalid input. Please enter 'all' or a number between 1 and {len(links_list)}.")

# Step 2: Visit selected links and extract content
with open("output.txt", "w", encoding="utf-8") as file:
    for link in selected_links:
        print(f"\n🔗 Fetching content from: {link}")
        try:
            page_response = requests.get(link)
            page_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the page: {e}")
            continue

        page_soup = BeautifulSoup(page_response.text, "html.parser")

        blog_divs = page_soup.find_all("div", class_="blog-details")

        for blog_div in blog_divs:
            if len(blog_div.get("class", [])) == 1 and blog_div.get("class")[0] == "blog-details":
                paragraphs = blog_div.find_all("p")
                for p in paragraphs:
                    file.write(p.text.strip() + "\n\n")
                break
        else:
            file.write(f"⚠️ No relevant 'blog-details' section found on: {link}\n\n")

        # Optional: Sleep to avoid overloading the server
        # time.sleep(1)

print("Scraping completed!")