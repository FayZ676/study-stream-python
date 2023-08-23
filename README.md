# zoom-transcription-summarizer-bot

## To run locally
1. Run `pip install -r requirements.txt` to install dependencies.
2. Copy `.env.example` and rename to `.env`.
3. This project uses Selenium to scrape the lecture transcripts which requires Chrome Webdriver. Make sure you have Google Chrome downloaded and installed. Download the correct version of Chrome Webdriver from [here](https://chromedriver.chromium.org/downloads). Add the path for your `chromedriver` to your `.env` file.
4. This project also uses OpenAI's GPT-3.5 LLM model which requires a valid API key. Add your API key to the `.env` as well.

## Future Updates
- [ ] Add support for other browsers. ChromeWebdriver is finicky.
- [ ] Add support for other models. GPT-3.5 LLM is expensive.
- [ ] Convert into a REST API (FastAPI is easy).