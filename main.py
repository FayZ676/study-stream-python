from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
import json
import tiktoken

# Initialize tiktoken encoding
encoding = tiktoken.get_encoding("cl100k_base")
encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def initialize_driver(chromedriver_path: str):
    """Initializes and returns a WebDriver instance."""
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
    chrome_service = ChromeService(chromedriver_path)
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return driver


def navigate_to_url(driver, url: str):
    """Navigates to the specified URL using the provided WebDriver instance."""
    print(f"Navigating to {url}...")
    driver.get(url)


def find_transcript_list(driver):
    """Finds and returns the transcript list element using the WebDriver instance."""
    try:
        print("Finding transcript list...")
        transcript_list = driver.find_element(By.CLASS_NAME, "transcript-list")
        driver.implicitly_wait(2)
        if transcript_list:
            print("Transcript list found.")
            return transcript_list
        else:
            print("Transcript list not found.")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


def extract_transcripts_from_list(transcript_list, professor_name):
    """Extracts and returns transcripts from a transcript list."""
    transcript_json_list = []

    # Find all <li> elements within the transcript list
    transcript_items = transcript_list.find_elements(By.TAG_NAME, "li")

    # Loop through the <li> elements and extract and format the content
    for item in transcript_items:
        aria_label = item.get_attribute("aria-label")
        if aria_label:
            # Split the aria-label into timestamp and message
            parts = aria_label.split(", ", 2)
            if len(parts) == 3:
                timestamp = parts[1]
                message = parts[2]
                # Create a JSON item
                transcript_json = {
                    "professor_name": professor_name,
                    "timestamp": timestamp,
                    "message": message,
                }
                transcript_json_list.append(transcript_json)
            elif len(parts) == 1:
                # Set the professor's name if it's not already set
                if not professor_name:
                    professor_name = parts[0]

    return transcript_json_list


def main():
    # Define the URL and path to Chromedriver
    zoom_url = "https://minnstate.zoom.us/rec/play/_4rxoQOaGD-wGoADdphEx2xrr6mIL-03RBLOQVliLSfpCWnqaFw8ZsPH8S15GFf5ntMMhM-AkVvOWAxN.QqPr_5357BdzYEQ0?canPlayFromShare=true&from=share_recording_detail&continueMode=true&componentName=rec-play&originRequestUrl=https%3A%2F%2Fminnstate.zoom.us%2Frec%2Fshare%2FrC4xystmtS7JDVaooCAbPB02ERdEOejlUwp0FnMais6PN1cT6JdjSA3b9ALhIJsc.tA1t1VFZeRAaYE_Y"
    chromedriver_path = (
        "/usr/local/bin/chromedriver"  # Replace with your Chromedriver path
    )

    # Initialize WebDriver
    driver = initialize_driver(chromedriver_path)

    # Navigate to the URL
    navigate_to_url(driver, zoom_url)

    # Find the transcript list
    transcript_list = find_transcript_list(driver)

    if transcript_list:
        # Initialize professor's name
        professor_name = ""

        # Extract transcripts from the transcript list
        transcript_json_list = extract_transcripts_from_list(
            transcript_list, professor_name
        )

        # Print the list of JSON items
        for item in transcript_json_list:
            print(json.dumps(item, indent=4))

    # Close the WebDriver
    driver.quit()


if __name__ == "__main__":
    main()
