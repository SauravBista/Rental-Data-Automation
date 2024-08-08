Zillow Rental Listings Scraper

Overview

This Python script scrapes rental listings from Zillow for a specified location (San Francisco, CA in this case) and uploads the data to a Google Form. The script uses requests and BeautifulSoup for web scraping and Selenium for automating the Google Form submission.

Features

    Scrapes rental listings: Extracts price, address, and link from Zillow rental listings.
    Uploads data to Google Form: Automatically fills out and submits a Google Form with the extracted data.

Installation
Prerequisites

    Python 3.x
    Google Chrome browser

Dependencies

Install the required Python libraries using pip:

pip install requests beautifulsoup4 selenium

WebDriver Setup

    Download ChromeDriver: Ensure that the version of ChromeDriver matches your Chrome browser version. Download it from ChromeDriver download page.

    Add ChromeDriver to PATH: Extract the chromedriver executable and add it to your system PATH or specify its location in the script.

Configuration

    Update Zillow URL: Modify the url variable in the script if you want to scrape rental listings from a different location or with different filters.

    Update Google Form URL: Replace the Google Form URL in the driver.get() method with your own form URL.

Usage

    Run the Script:

    python script.py

    This will start the scraping process and open Chrome to fill out the Google Form automatically.

    Check Outputs:
        The script will print the extracted prices, addresses, and links.
        Data will be submitted to the specified Google Form.

Code Explanation

    Web Scraping:
        Uses requests to fetch the Zillow rental listings page.
        Uses BeautifulSoup to parse the HTML and extract property details.

    Data Extraction:
        Functions extract_price(), extract_address(), and extract_link() handle the extraction of data from the HTML elements.

    Form Submission:
        Uses Selenium to automate the process of filling out and submitting the Google Form.

Contributing

If you’d like to contribute to this project, please fork the repository and submit a pull request with your changes.

License

This project is licensed under the MIT License - see the LICENSE file for details.
Contact

For any questions or feedback, please contact sauravbista10@gmail.com.
