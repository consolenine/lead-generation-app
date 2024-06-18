import csv
import json
import re


def validate_contact(contact):
    if (
        len(contact["links"]["free"]) == 0
        and len(contact["links"]["paid"]) == 0
        and len(contact["email"]) == 0
        and len(contact["phone"]) == 0
    ):
        return False
    return True


def extract_contacts(description):
    contacts = {
        "links": {"free": set(), "paid": set(), "others": set()},
        "email": set(),
        "phone": set(),
    }

    # Regex pattern to match URLs
    url_pattern = r'https?://?\S+(?=")'
    # Find all URLs in the description
    urls = re.findall(url_pattern, description)
    # Exclude Spotify links
    urls = [url for url in urls if "spotify.com" not in url]

    # Categorize URLs
    free_keywords = [
        "toneden",
        "imus",
        "soundplate",
        "dailyplaylists",
        "submi" "forms",
        "pitch",
    ]
    paid_keywords = ["ko-fi", "submithub", "sbmt.to"]

    free_urls = [
        url for url in urls if any(keyword in url for keyword in free_keywords)
    ]
    paid_urls = [
        url for url in urls if any(keyword in url for keyword in paid_keywords)
    ]
    others_urls = [url for url in urls if url not in free_urls and url not in paid_urls]

    contacts["links"]["free"].update(free_urls)
    contacts["links"]["paid"].update(paid_urls)
    contacts["links"]["others"].update(others_urls)

    # Regex pattern to match email addresses
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    # Find all email addresses in the description
    emails = re.findall(email_pattern, description)
    contacts["email"].update(emails)

    # Regex pattern to match phone numbers
    phone_pattern = r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b"
    # Find all phone numbers in the description
    phones = re.findall(phone_pattern, description)
    contacts["phone"].update(phones)

    return contacts


def process_csv(file_path):
    results = {}
    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            artist_id = row["artist_id"]
            playlist_description = row["playlist_description"]
            # Extract contacts from playlist description
            contacts = extract_contacts(playlist_description)
            # If artist_id already exists in results, extend the existing list of contacts with the new contacts found in the current row
            if artist_id in results:
                results[artist_id]["contacts"].extend(contacts)
            # If artist_id does not exist in results, create a new entry
            else:
                results[artist_id] = {"artist_id": artist_id, "contacts": contacts}

    # Remove artists without any contacts
    results = {k: v for k, v in results.items() if v["contacts"]}

    # Remove duplicates from the list of contacts
    for artist_info in results.values():
        artist_info["contacts"] = list(set(artist_info["contacts"]))

    return list(results.values())


def filterLeads():
    file_path = "playlists.csv"
    results = process_csv(file_path)
    # Convert results to JSON format
    json_data = json.dumps(results, indent=4)

    # Write JSON data to a file
    output_file_path = "output.json"
    with open(output_file_path, "w") as output_file:
        output_file.write(json_data)

    print(f"JSON data has been written to {output_file_path}")
    return json_data


if __name__ == "__main__":
    filterLeads()
