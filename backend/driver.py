from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

# Set up the WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

def get_contractors():
    try:
        target_url = 'https://www.gaf.com/en-us/roofing-contractors/residential?postalCode=10013&distance=25'
        driver.get(target_url)

        # Wait until the <article> tags are present
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'article'))
        )
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'h2'))
        )

        # Retrieve all <article> elements
        articles = driver.find_elements(By.TAG_NAME, 'article')

        # Iterate through each <article> element
        contractor_details = []

        for article in articles:
            try:
                # Extract contractor name
                name = article.find_element(By.CLASS_NAME, 'certification-card__heading').text

                # Extract contractor rating
                rating_element = article.find_element(By.CLASS_NAME, 'rating-stars')
                rating = rating_element.get_attribute('data-rating') if rating_element else 'No rating'

                # Extract contractor location
                location = article.find_element(By.CLASS_NAME, 'certification-card__city').text

                # Extract URL to contractor's page
                profile_url = article.find_element(By.TAG_NAME, 'a').get_attribute('href')

                # Extract href of <a> tag with class 'certification-card__image-link'
                profile_url = article.find_element(By.CLASS_NAME, 'certification-card__image-link').get_attribute('href')

                # Extract phone number
                phone = article.find_element(By.CLASS_NAME, 'phone').text

                contractor_details.append({
                    'name': name,
                    'rating': rating,
                    'location': location,
                    'profile_url': profile_url,
                    'phone': phone
                })
            except Exception as e:
                print(f"An error occurred: {e}")
                continue

        # Print the extracted contractor details
        for contractor in contractor_details:
            print(contractor)

    finally:    
        # Close the WebDriver
        driver.quit()

get_contractors()