from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import tiktoken
import os
import openai
from dotenv import load_dotenv
import time

# Load environment variables from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


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
    # if the url is prefixed by https://mediaspace.minnstate.edu/ store the string captionList and class
    # if the url is prefixed by https://minnstate.zoom.us/ store the string transcript-list and class
    print(f"Navigating to {url}...")
    # Depending on whether the url is prefixed by minnstate or
    # mediaspace, store the target elemtents in a list.
    driver.get(url)

    play_video(driver)


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


# This will extract the transcripts from minnstate links
def extract_transcripts_from_minnstate(transcript_list, professor_name):
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


#  This will extract the transcripts from mediaspace links
def extract_transcripts_from_mediaspace(transcript_list, professor_name):
    return


# This will parse the url prefix and call the appropriate scraping function
def extract_transcripts():
    return


def join_transcripts(transcript_json_list):
    """Joins the messages from a list of transcripts."""
    return " ".join([item["message"] for item in transcript_json_list])


def check_token_count(num_tokens: int):
    if num_tokens > 12000:
        print(
            "Error: The transcript is too long.\nThe model can only take 12,000 tokens and the transcript is {num_tokens} tokens."
        )
        return
    else:
        pass


def query_transcripts(concatenated_messages: str, query: str):
    """Queries the transcripts for a specific term."""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {
                "role": "user",
                "content": concatenated_messages + "\n\n" + query,
            },
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    response = response.choices[0].message.content
    return response


def ask_question(concatenated_messages):
    """Allows the user to ask a question and get a response."""
    while True:
        print("\nOptions:")
        print("1. Ask a question")
        print("2. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            query = input("Enter your question: ")
            response = query_transcripts(concatenated_messages, query)
            print(response)
        elif choice == "2":
            break
        else:
            print("Invalid choice. Please select 1 to ask a question or 2 to exit.")


# ------------------------- MEDIASPACE FUNCTIONS START -------------------------


def find_transcript_list_mediaspace(driver):
    """Finds and returns the transcript list element using the WebDriver instance."""
    try:
        # Find the parent div element by class name
        print("Finding transcript list...")
        transcript_list = driver.find_element(
            By.CLASS_NAME, "captionList__transcript-wrapper___Omf8T"
        )

        # Get the outer HTML content of the transcript list parent element
        transcript_list_html = transcript_list.get_attribute("outerHTML")

        # # export the html to a file for debugging
        # with open("transcript_list.html", "w") as f:
        #     f.write(transcript_list_html)

        if transcript_list_html:
            print("Transcript list found.")
            print("TRANSCRIPT LIST HTML TYPE: ", type(transcript_list_html))
            return transcript_list_html
        else:
            print("Transcript list not found.")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


def extract_transcripts_from_mediaspace(transcript_list_html):
    """Extracts and returns transcripts from a transcript list."""
    transcript_json_list = []

    # Find all <div> elements with class "caption__caption___v5MZY" within the transcript list
    transcript_items = transcript_list_html.find_elements(
        By.CLASS_NAME, "caption__caption___v5MZY"
    )

    # Loop through the <div> elements and extract and format the content
    for item in transcript_items:
        aria_label = item.get_attribute("aria-label")
        if aria_label:
            # Split the aria-label into timestamp and message
            parts = aria_label.split(" ", 1)
            if len(parts) == 2:
                timestamp = parts[0]
                message = parts[1]
                # Create a JSON item
                transcript_json = {
                    "timestamp": timestamp,
                    "message": message,
                }
                transcript_json_list.append(transcript_json)

    print("TRANSCRIPTION JSON LIST:", transcript_json_list)

    return transcript_json_list


# Clicks the play button on the video to load the transcripts
def play_video(driver):
    # click the play button using the xpath
    play_button = driver.find_element(
        By.XPATH,
        "/html/body/div[1]/div[2]/div[5]/div[2]/div[2]/div[1]/div/div/div/div/div[2]/div[1]/div[3]/div[1]/div[3]/button/div/i",
    )
    play_button.click()

    # Wait for 10 seconds or until the class "caption__caption___v5MZY" is found
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "caption__caption___v5MZY"))
    )

    with open("raw_after.html", "w") as f:
        f.write(driver.page_source)


# ------------------------- MEDIASPACE FUNCTIONS END -------------------------


def main():
    # Define the URL and path to Chromedriver
    zoom_url = "https://minnstate.zoom.us/rec/play/_4rxoQOaGD-wGoADdphEx2xrr6mIL-03RBLOQVliLSfpCWnqaFw8ZsPH8S15GFf5ntMMhM-AkVvOWAxN.QqPr_5357BdzYEQ0?canPlayFromShare=true&from=share_recording_detail&continueMode=true&componentName=rec-play&originRequestUrl=https%3A%2F%2Fminnstate.zoom.us%2Frec%2Fshare%2FrC4xystmtS7JDVaooCAbPB02ERdEOejlUwp0FnMais6PN1cT6JdjSA3b9ALhIJsc.tA1t1VFZeRAaYE_Y"
    mediaspace_url = "https://mediaspace.minnstate.edu/media/Biodiversity/1_etpkqwi2"
    chromedriver_path = os.getenv("CHROMEDRIVER_PATH")

    # Initialize WebDriver
    driver = initialize_driver(chromedriver_path)

    # Navigate to the URL
    navigate_to_url(driver, mediaspace_url)

    # Find the transcript list
    transcript_list_html = find_transcript_list_mediaspace(driver)

    # # Extract transcripts from the transcript list
    # transcript_json_list = extract_transcripts_from_mediaspace(transcript_list_html)

    # # Concatenate all "message" fields and count tokens
    # concatenated_messages = join_transcripts(transcript_json_list)
    # num_tokens = num_tokens_from_string(concatenated_messages, "cl100k_base")
    # check_token_count(num_tokens)

    # # Interactive menu for asking questions
    # ask_question(concatenated_messages)

    # ---------------------------------------------

    # if transcript_list:
    #     # Initialize professor's name
    #     professor_name = ""

    #     # Extract transcripts from the transcript list
    #     transcript_json_list = extract_transcripts_from_minnstate(
    #         transcript_list, professor_name
    #     )

    #     # Concatenate all "message" fields and count tokens
    #     concatenated_messages = join_transcripts(transcript_json_list)
    #     num_tokens = num_tokens_from_string(concatenated_messages, "cl100k_base")
    #     check_token_count(num_tokens)

    #     # Interactive menu for asking questions
    #     ask_question(concatenated_messages)

    # Close the WebDriver
    driver.quit()


if __name__ == "__main__":
    main()
