# 🍕 Pizza Chatbot with LLM and Voice Assistant

This project is a voice- and text-based pizza ordering chatbot built using a local large language model (LLM) — Mistral-Nemo-Instruct-2407 — integrated via `llama.cpp`. Users can interact through a web interface or using real-time voice commands to place structured pizza orders.

---

## 🚀 Features

- 🌐 FastAPI backend for chat interaction  
- 🧠 Local LLM integration with `llama.cpp`  
- 🎤 Voice support via Whisper (speech-to-text) and Porcupine (wake word detection)  
- 🤖 Hybrid intent classification using ML and rule-based logic  
- 🍕 Structured pizza order tracking (pizzas, toppings, extras, notes, address)  
- 💬 React-based frontend widget for web interaction  

---

## 📦 Project Structure

PizzaBot/

├── main.py                     # FastAPI app with message endpoint & voice assistant thread  
├── dialog_manager.py           # Manages structured order and user dialog state  
├── intent_classifier.py        # TF-IDF + RandomForest + rule-based fallback  
├── llm_agent.py                # Prompt construction and LLM interaction (via llama.cpp)  
├── realtime_voice_assistant.py # Wake word detection & Whisper integration  
├── menu.py                     # Dictionary with available pizzas, toppings, extras  
├── data.py                     # Training data for intent classification  
├── ReactWebWidgetFront/        # React web widget  
├── docs/                       # Project screenshots and diagrams, pdf report
└── README.md                   # Project overview and usage instructions

---

## 🛠️ Installation

Download local LLM model Mistral-Nemo-Instruct-2407-Q5_K_M.gguf and place it to the root folder

Clone repo:
```bash
git clone https://github.com/yourusername/pizza-chatbot
cd pizza-chatbot
pip install -r requirements.txt

Start FastAPI backend:# pizzachatbot
uvicorn main:app --reload

Start React web widget frontend:# pizzachatbot
npm install .
npm start

sample order format:
{
  "pizzas": ["Margherita"],
  "toppings": ["Onions", "Chili"],
  "extras": ["Cola"],
  "notes": "very spicy, vegan",
  "address": "Reuterstraße 49, Berlin"
}
Voice Assistant

Say “Jarvis” to activate the assistant. Requires microphone access and macOS (for say()).

🧠 Dialog Flow Overview
Here’s a simplified logic before turning it into a flowchart:

Start / Wake Word Detected (if voice)
⬇
User Input Received (text or voice)
⬇
Intent Classification
via combined_classify() (ML + rules + LLM fallback)
⬇
Prompt Generation & LLM Response
via generate_prompt() → get_response()
⬇
Dialog Manager Updates Order Based on Intent
"pizza", "topping", "extra", "note", "address"
⬇
Check if Order is Complete (has address)
If yes → confirmation
If no → ask for missing info
⬇
Bot Responds / Speaks Reply

Future Improvements

Add user authentication and order history
Support multiple languages
Improve fuzzy matching of menu items
Integrate payment and delivery tracking
