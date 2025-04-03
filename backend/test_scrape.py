import requests
from bs4 import BeautifulSoup

# URL of the GAF contractors page for the specified postal code and distance
url = 'https://www.gaf.com/en-us/roofing-contractors/residential?postalCode=10013&distance=25'

# Headers to mimic a browser visit (some websites block requests with missing or incorrect headers)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Send a GET request to the URL
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find('h1', class_='city-listing-masthead__heading').get_text(strip=True)
    print(title)

    # Write the retrieved HTML content to backend/output.html
    with open('backend/output.html', 'w', encoding='utf-8') as f:
        f.write(response.text)

    # Find all elements that contain contractor names
    # Note: The actual tag and class will depend on the website's HTML structure
    # For example, if contractor names are within <h3 class="contractor-name"> tags:
    contractor_elements = soup.find_all('li')
    
    # Extract and print the contractor names
    # for contractor in contractor_elements:
    #     print(contractor.get_text(strip=True))
else:
    print(f'Failed to retrieve the page. Status code: {response.status_code}')
