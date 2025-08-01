import { useState, useRef, useEffect } from "react";

export default function FloatingChatWidget({ visible, onClose, messages, setMessages }) {

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const endOfMessagesRef = useRef(null); // 👈 Реф для автоскролла

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMsg = input;
    setMessages(prev => [...prev, { sender: "user", text: userMsg }]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:9000/message", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMsg })
      });
      const data = await res.json();
      setMessages(prev => [...prev, { sender: "ai", text: data.reply }]);
    } catch (error) {
      setMessages(prev => [...prev, { sender: "ai", text: "⚠️ Ошибка соединения с AI." }]);
    } finally {
      setLoading(false);
    }
  };


  // 👇 Скролл вниз после каждого обновления сообщений
  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  return (
    <div className={`main-block w-full fixed bottom-5 right-5 h-[50%] rounded-3xl shadow-2xl overflow-hidden font-sans z-50 transition-all duration-300 transform ${
      visible ? "opacity-100 scale-100 pointer-events-auto" : "opacity-0 scale-95 pointer-events-none"
    }`}>
      {/* Header */}
      <div className="bg-white border border-grey-200 text-black p-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <img src={require("./images/chatLogo.jpeg")} alt="logo" className="w-6 h-6 rounded-full logorounded" />
          <div className="text-lg font-semibold leading-tight">
            Pizza Assistant
          </div>
        </div>
        <button
          onClick={onClose}
          className="pxpadding10 text-black text-xl font-bold leading-none margin-bottom4"
          aria-label="Close chat"
        >
          ×
        </button>
      </div>

      {/* Message Box */}
      <div className="bg-white p-4 h-64 overflow-y-auto space-y-2 text-sm font-familymain">
        {messages.length === 0 && (
          <div className="bg-gray-100 text-gray-800 p-3 rounded-xl">
            Hi I am pizza chat asistant, how can i help you? 
          </div>
        )}
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`p-2 rounded-xl max-w-[50%] ${
              msg.sender === "user"
                ? "bg-gray-100 text-right ml-auto"
                : "bg-gray-100 mr-auto"
            }`}
          >
            {msg.text}
          </div>
        ))}
        {loading && <div className="text-gray-400">✍️ Typing...</div>}
        <div ref={endOfMessagesRef} /> {/* 👈 Скролл-маркер */}
      </div>

      {/* Input Section */}
      <div className="bg-white px-4 pb-4 pt-2 flex gap-2">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === "Enter" && sendMessage()}
          placeholder="Ask pizza assitant for help..."
          className="flex-1 border border-gray-200 rounded-xl px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
        />
        <button
          onClick={sendMessage}
          className="pxpadding10 text-small bg-black text-white px-4 py-2 font-medium rounded-xl hover:opacity-90 transition"
        >
          <span style={{fontSize: 10}}>Send</span>
        </button>
      </div>
    </div>
  );
}
