import requests
from bs4 import BeautifulSoup
import time


def get_gorkhapatra_links():
    
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
def get_nepal_samacharpatra_links():
    base_url = "https://newsofnepal.com/loksewa/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the Nepal Samacharpatra page: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    links_list = []

    # Find all 'div' with class 'card uk-card uk-card-small uk-card-default'
    cards = soup.find_all("div", class_="card uk-card uk-card-small uk-card-default")

    for card in cards:
        text_element = card.find("a", class_="uk-heading-bullet")
        if text_element and "वस्तुगत सामग्री" in text_element.get_text():
            link_tag = card.find("a", href=True)
            if link_tag:
                href = link_tag["href"]
                full_link = href if href.startswith("http") else "https://newsofnepal.com" + href
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
                page_response = requests.get(link, headers=headers)
                page_response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"Error fetching the page: {e}")
                continue

            page_soup = BeautifulSoup(page_response.text, "html.parser")

            blog_divs = page_soup.find_all("div", class_="post-entry")

            for blog_div in blog_divs:                
                paragraphs = blog_div.find_all("p")
                for p in paragraphs:
                    # Replace <br> tags with new line characters
                    for br in p.find_all("br"):
                        br.replace_with("\n")
                    file.write(p.text.strip() + "\n\n")
                break
            


# Ask the user which site to scrape
print("Select the website to scrape:")
print("1. Gorkhapatra Online")
print("2. Nepal Samacharpatra")

choice = input("Enter 1 or 2: ").strip()

if choice == "1":
    links = get_gorkhapatra_links()
elif choice == "2":
    links = get_nepal_samacharpatra_links()
else:
    print("Invalid choice! Exiting...")
    exit()

print("Scraping completed!")