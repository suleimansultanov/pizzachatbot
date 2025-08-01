from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Optional
from dialog_manager import DialogManager
from llm_agent import generate_prompt, get_response, classify_intent_with_llm
from fastapi.middleware.cors import CORSMiddleware
from intent_classifier import init, classify_intent, combined_classify
from realtime_voice_assistant import detect_wake_word, capture_text, speak
import threading

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
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
    
    if llm_reply.strip() == "```":
        bot_response = "Please provide clarifications! It is hard to understand your needs."
    else:
        bot_response = dialog_manager.update(user_input, llm_reply, intent)
    print(dialog_manager.order)
    return {
        "reply": bot_response,
        "order": dialog_manager.order
    }

# Фоновая задача для голосового ассистента
def background_voice_loop():
    print("🔔 Waiting for wake word...")
    detect_wake_word()
    speak("Hello! How can I help you?")

    while True:
        user_message = capture_text()
        if user_message.lower() in ["exit", "stop", "goodbye"]:
            speak("Goodbye!")
            break

        if not user_message:
            continue  # skip empty input

        print(f"You said: {user_message}")
        prompt = generate_prompt(dialog_manager.order, user_message)
        intent = combined_classify(user_message)
        reply = get_response(prompt)
        print(f"Intent: {intent}")
        print(f"Bot: {reply}")
        print(dialog_manager.order)
        if reply.strip() == "```":
            reply = "Please provide clarifications! It is hard to understand your needs."

        dialog_manager.update(user_message, reply, intent)
        speak(reply)

        

# Запуск фоновой задачи при старте FastAPI
@app.on_event("startup")
def start_background_voice_assistant():
    thread = threading.Thread(target=background_voice_loop, daemon=True)
    thread.start()


