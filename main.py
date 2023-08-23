from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions

# Define the URL
url = "https://minnstate.zoom.us/rec/play/_4rxoQOaGD-wGoADdphEx2xrr6mIL-03RBLOQVliLSfpCWnqaFw8ZsPH8S15GFf5ntMMhM-AkVvOWAxN.QqPr_5357BdzYEQ0?canPlayFromShare=true&from=share_recording_detail&continueMode=true&componentName=rec-play&originRequestUrl=https%3A%2F%2Fminnstate.zoom.us%2Frec%2Fshare%2FrC4xystmtS7JDVaooCAbPB02ERdEOejlUwp0FnMais6PN1cT6JdjSA3b9ALhIJsc.tA1t1VFZeRAaYE_Y"

# Set up Selenium WebDriver with Chrome
chrome_options = ChromeOptions()
chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
chrome_service = ChromeService(
    "/usr/local/bin/chromedriver"
)  # Replace with the path to chromedriver

# Create the WebDriver instance
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Navigate to the URL
print(f"Navigating to {url}...")
driver.get(url)
try:
    print("Finding transcript list...")
    # Wait for the transcript list to load
    transcript_list = driver.find_element(By.CLASS_NAME, "transcript-list")
    driver.implicitly_wait(2)
    if transcript_list:
        print("Transcript list found.")
        print("Extracting transcript text...")
        # Find all <li> elements within the transcript list
        transcript_items = transcript_list.find_elements(By.TAG_NAME, "li")
        # Loop through the <li> elements and extract and print the content from aria-label
        for item in transcript_items:
            aria_label = item.get_attribute("aria-label")
            if aria_label:
                print(aria_label)
    else:
        print("Transcript list not found.")
except Exception as e:
    print(f"An error occurred: {str(e)}")

# Close the WebDriver
driver.quit()
