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

├── main.py # FastAPI app with message endpoint & voice assistant thread
├── dialog_manager.py # Manages structured order and user dialog state
├── intent_classifier.py # TF-IDF + RandomForest + rule-based fallback
├── llm_agent.py # Prompt construction and LLM interaction (via llama.cpp)
├── realtime_voice_assistant.py # Wake word detection & Whisper integration
├── menu.py # Dictionary with available pizzas, toppings, extras
├── data.py # Training data for intent classification
├── frontend/ # React web widget (not included here)
└── README.md
---

## 🛠️ Installation

1. Clone this repo:
```bash
git clone https://github.com/yourusername/pizza-chatbot
cd pizza-chatbot
pip install -r requirements.txt

Start FastAPI backend:# pizzachatbot
uvicorn main:app --reload
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

Future Improvements

Add user authentication and order history
Support multiple languages
Improve fuzzy matching of menu items
Integrate payment and delivery tracking
