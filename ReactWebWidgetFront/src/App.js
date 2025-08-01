// App.js
import React, { useState } from "react";
import "./index.css";
import "./App.css";
import FloatingChatWidget from "./chatBot";

function App() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);

  return (
    <div className="App">
      <div className="relative z-50">
        {/* Floating Chat Button */}
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="fixed bottom-6 right-6 text-white rounded-full p-4 shadow-lg transition"
        >
          {isOpen ? (
            <span className="text-xl">✖</span>
          ) : (
            <img
              src={require("./images/chatIcon.png")}
              alt="Open Chat"
              className="w-6 h-6 widgetButton"
            />
          )}

        </button>

        {/* Chatbox always mounted */}
        <FloatingChatWidget
          visible={isOpen}
          onClose={() => setIsOpen(false)}
          messages={messages}
          setMessages={setMessages}
        />
      </div>
    </div>
  );
}

export default App;
