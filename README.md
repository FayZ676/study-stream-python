# zoom-transcription-summarizer-bot

# What is this?
Talk to your professor's Zoom recordings and get an instant summary of the lecture!

## To run locally
1. Run `pip install -r requirements.txt` to install dependencies.
2. Copy `.env.example` and rename to `.env`.
3. This project uses Selenium to scrape the lecture transcripts which requires Chrome Webdriver. Make sure you have Google Chrome downloaded and installed. Download the correct version of Chrome Webdriver from [here](https://chromedriver.chromium.org/downloads). Add the path for your `chromedriver` to your `.env` file.
4. This project also uses OpenAI's GPT-3.5 LLM model which requires a valid API key. Add your API key to the `.env` as well.
5. Run `python main.py` to start the bot.
6. Change `zoom_url` and `query` in `main.py` to ask your own questions to other lectures.

## Future Updates
- [ ] Add support for other scrapers. ChromeWebdriver is finicky. I recall using `requests` once to do the same thing much simpler.
- [ ] Add support for other models. GPT-3.5 LLM is expensive.
- [ ] Convert into a REST API (FastAPI is easy). Sucks to have to run the script every time you want to query.