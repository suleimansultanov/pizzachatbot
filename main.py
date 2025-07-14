from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Optional
from dialog_manager import DialogManager
from llm_agent import generate_prompt, get_response, classify_intent_with_llm
from fastapi.middleware.cors import CORSMiddleware
from intent_classifier import init, classify_intent, combined_classify

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend origin, e.g., "http://localhost:3000"
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, OPTIONS, etc.
    allow_headers=["*"],
)
dialog_manager = DialogManager()

class UserMessage(BaseModel):
    message: str


@app.post("/message")
async def message_handler(user_message: UserMessage):

    user_input = user_message.message
    prompt = generate_prompt(dialog_manager.order, user_input)
    intent = combined_classify(user_input)
    llm_reply = get_response(prompt)
    bot_response= ""
    if(llm_reply=="```"):
        bot_response = "Please provide clarrifications! it is hard to understand your needs"
    bot_response = dialog_manager.update(user_input, llm_reply, intent)
    return {
        "reply": bot_response,
        "order": dialog_manager.order
    }


