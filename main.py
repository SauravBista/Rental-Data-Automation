import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

import time

# Initialize lists to store extracted data
price_list = []
address_list = []
link_list = []

# Define the headers to mimic a real browser request
header = {
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0"
}

# URL of the Zillow rental listings page
url = 'https://www.zillow.com/san-francisco-ca/rentals/?searchQueryState=%7B%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22north%22%3A37.96828106438242%2C%22south%22%3A37.70690253072065%2C%22east%22%3A-122.1370419633789%2C%22west%22%3A-122.67674533251953%7D%2C%22mapZoom%22%3A11%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22price%22%3A%7B%22min%22%3Anull%2C%22max%22%3A872627%7D%2C%22mp%22%3A%7B%22min%22%3Anull%2C%22max%22%3A3000%7D%2C%22beds%22%3A%7B%22min%22%3A1%2C%22max%22%3Anull%7D%7D%2C%22isListVisible%22%3Atrue%2C%22category%22%3A%22cat1%22%2C%22usersSearchTerm%22%3A%22San%20Francisco%2C%20CA%22%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22pagination%22%3A%7B%7D%7D'

# Function to extract price, handling possible formatting issues
def extract_price(price_tag):
    if price_tag:
        return price_tag.get_text().split('+')[0].strip()  # Extract price and remove any trailing text
    return 'N/A'  # Return 'N/A' if no price is found

# Function to extract address
def extract_address(address_tag):
    if address_tag:
        return address_tag.get_text()  # Extract the text content of the address tag
    return 'N/A'  # Return 'N/A' if no address is found

# Function to extract link and ensure it is a complete URL
def extract_link(link_tag):
    if link_tag:
        link = link_tag.get('href')
        # Construct full URL if the link is relative
        if link and not link.startswith('http'):
            return f'https://www.zillow.com{link}'
    return 'N/A'  # Return 'N/A' if no link is found

# Send HTTP GET request to the Zillow page
response = requests.get(url, headers=header)
if response.status_code != 200:
    raise Exception(f'Failed to load page {url}')  # Raise an error if the page fails to load

# Parse the HTML content of the page
website = response.text
soup = BeautifulSoup(website, 'html.parser')

# Find the <ul> element that contains the list of properties
ul = soup.find("ul", class_="List-c11n-8-102-0__sc-1smrmqp-0 StyledSearchListWrapper-srp-8-102-0__sc-1ieen0c-0 kquqgw gLCZxh photo-cards")
if ul:
    # Find all <li> elements within the <ul>
    listings = ul.find_all('li', class_='ListItem-c11n-8-102-0__sc-13rwu5a-0 StyledListCardWrapper-srp-8-102-0__sc-wtsrtn-0 hKdzLV kgwlbT')

    for listing in listings:
        # Extract price, address, and link from each listing
        price = extract_price(listing.find('span', class_='PropertyCardWrapper__StyledPriceLine-srp-8-102-0__sc-16e8gqd-1 vjmXt'))
        address = extract_address(listing.find('address', {"data-test": "property-card-addr"}))
        link = extract_link(listing.find('a', {"data-test": "property-card-link"}))

        # Append the extracted data to corresponding lists if available
        if price and address and link:
            price_list.append(price)
            address_list.append(address)
            link_list.append(link)
else:
    print('No listings found.')

# Initialize the Chrome WebDriver for interacting with the Google Form
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)  # Keep browser open after script finishes

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Open the Google Form
driver.get('https://forms.gle/JFyR4aDinPKdvn3T6')
time.sleep(3)  # Wait for the form to load

# Iterate through the lists and fill out the form for each entry
length_of_list = len(price_list)
for a in range(length_of_list):
    # Locate form fields and submit button
    first_question = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    second_question = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    third_question = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')

    # Fill the form with the data
    first_question.send_keys(address_list[a])
    second_question.send_keys(price_list[a])
    third_question.send_keys(link_list[a])
    submit_button.click()
    time.sleep(3)  # Wait for submission to complete

    # Refill the form for the next entry
    refill_the_form = driver.find_element(By.XPATH, value='/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    refill_the_form.click()
    time.sleep(3)  # Wait for form to be cleared
