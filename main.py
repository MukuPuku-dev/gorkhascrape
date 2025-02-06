import requests
from bs4 import BeautifulSoup
import time

# Step 1: Scrape the main page to collect links
base_url = "https://gorkhapatraonline.com"
main_url = base_url + "/categories/loksewa"

try:
    response = requests.get(main_url)
    response.raise_for_status()  # Raise error for bad responses (4xx, 5xx)
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
        full_link = href if href.startswith("http") else base_url + href  # Ensure proper URL
        links_list.append(full_link)

# Step 2: Visit each link and extract <p> tags from <div class="blog-details"> without other classes
with open("output.txt", "w", encoding="utf-8") as file:
    for link in links_list:
        print(f"\n🔗 Fetching content from: {link}")
        try:
            page_response = requests.get(link)
            page_response.raise_for_status()  # Raise error for bad responses (4xx, 5xx)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the page: {e}")
            continue

        page_soup = BeautifulSoup(page_response.text, "html.parser")

        # Find all divs with class 'blog-details' and filter for the one with no other classes
        blog_divs = page_soup.find_all("div", class_="blog-details")

        for blog_div in blog_divs:
            if len(blog_div.get("class", [])) == 1 and blog_div.get("class")[0] == "blog-details":
                # This is the blog-details div we're looking for (with only the 'blog-details' class)
                paragraphs = blog_div.find_all("p")
                for p in paragraphs:
                    file.write(p.text.strip() + "\n\n")  # Save each paragraph's text content to file
                break  # Stop after processing the correct 'blog-details' div
        else:
            file.write(f"⚠️ No relevant 'blog-details' section found on: {link}\n\n")

        # Optional: Sleep for a brief period to avoid overloading the server
        # time.sleep(1)

print("Scraping completed!")
