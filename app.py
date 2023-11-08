from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from main import (
    initialize_driver,
    extract_transcripts,
    join_transcripts,
    num_tokens_from_string,
    check_token_count,
    ask_question,
)


app = FastAPI()


class TranscriptContent(BaseModel):
    timestamp: str
    message: str


class TranscriptRequest(BaseModel):
    url: str


class TranscriptResponse(BaseModel):
    transcripts: List[TranscriptContent]


@app.get("/")
async def read_root():
    return {"message": "Welcome to the transcript processing API!"}


@app.post("/transcripts/", response_model=TranscriptResponse)
async def get_transcripts(transcript_request: TranscriptRequest):
    url = transcript_request.url
    driver = initialize_driver(os.getenv("CHROMEDRIVER_PATH"))
    transcript_json_list = extract_transcripts(driver, url)
    concatenated_messages = join_transcripts(transcript_json_list)
    num_tokens = num_tokens_from_string(concatenated_messages, "cl100k_base")
    check_token_count(num_tokens)
    return {"transcripts": transcript_json_list}


@app.post("/ask/", response_model=dict)
async def ask_questions(question_request: dict):
    concatenated_messages = question_request.get("transcripts")
    query = question_request.get("query")
    response = ask_question(concatenated_messages, query)
    return {"response": response}
