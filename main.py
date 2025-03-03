import requests
from bs4 import BeautifulSoup
import time

def get_gorkhapatra_links():
    session = requests.Session()
    base_url = "https://gorkhapatraonline.com"
    main_url = base_url + "/categories/loksewa?page=1"
    
    start_time = time.time()
    try:
        response = session.get(main_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the main page: {e}")
        exit()
    print(f"Time to fetch main page: {time.time() - start_time:.2f} seconds")

    soup = BeautifulSoup(response.text, "html.parser")
    links_list = []

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

    print("\nFound the following links:")
    for idx, link in enumerate(links_list, 1):
        print(f"{idx}: {link}")

    selected_links = []
    while True:
        user_input = input(f"\nEnter the numbers of the links to scrape (e.g., 1,2,3), "
                        "or 'all' to scrape all: ").strip().lower()
        
        if user_input == 'all':
            selected_links = links_list
            break
        else:
            try:
                choices = [int(x) for x in user_input.split(',')]
                if all(1 <= choice <= len(links_list) for choice in choices):
                    selected_links = [links_list[choice - 1] for choice in choices]
                    break
                else:
                    print(f"Please enter numbers between 1 and {len(links_list)}.")
            except ValueError:
                print(f"Invalid input. Please enter 'all' or a comma-separated list of numbers between 1 and {len(links_list)}.")

    with open("output.txt", "w", encoding="utf-8") as file:
        for link in selected_links:
            print(f"\n🔗 Fetching content from: {link}")
            try:
                page_response = session.get(link)
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

def get_nepal_samacharpatra_links():
    session = requests.Session()
    base_url = "https://newsofnepal.com/loksewa"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.0.0"
    }

    start_time = time.time()
    try:
        response = session.get(base_url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the Nepal Samacharpatra page: {e}")
        return []
    print(f"Time to fetch main page: {time.time() - start_time:.2f} seconds")

    soup = BeautifulSoup(response.text, "html.parser")
    links_list = []

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

    print("\nFound the following links:")
    for idx, link in enumerate(links_list, 1):
        print(f"{idx}: {link}")

    selected_links = []
    while True:
        user_input = input(f"\nEnter the numbers of the links to scrape (e.g., 1,2,3), "
                        "or 'all' to scrape all: ").strip().lower()
        
        if user_input == 'all':
            selected_links = links_list
            break
        else:
            try:
                choices = [int(x) for x in user_input.split(',')]
                if all(1 <= choice <= len(links_list) for choice in choices):
                    selected_links = [links_list[choice - 1] for choice in choices]
                    break
                else:
                    print(f"Please enter numbers between 1 and {len(links_list)}.")
            except ValueError:
                print(f"Invalid input. Please enter 'all' or a comma-separated list of numbers between 1 and {len(links_list)}.")

    with open("output.txt", "w", encoding="utf-8") as file:
        for link in selected_links:
            print(f"\n🔗 Fetching content from: {link}")
            try:
                page_response = session.get(link, headers=headers)
                page_response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"Error fetching the page: {e}")
                continue

            page_soup = BeautifulSoup(page_response.text, "html.parser")

            blog_divs = page_soup.find_all("div", class_="post-entry")

            for blog_div in blog_divs:                
                paragraphs = blog_div.find_all("p")
                for p in paragraphs:
                    for br in p.find_all("br"):
                        br.replace_with("\n")
                    file.write(p.text.strip() + "\n\n")
                break

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