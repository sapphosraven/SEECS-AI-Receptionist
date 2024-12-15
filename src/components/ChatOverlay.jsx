import React, { useState } from "react";

function ChatOverlay() {
  const [showHistory, setShowHistory] = useState(false);
  const [history, setHistory] = useState([]); // Stores chat history
  const [input, setInput] = useState(""); // Input value
  const [isWaitingForResponse, setIsWaitingForResponse] = useState(false); // Tracks if waiting for response

  // Simulates chatbot response (replace with actual API call if needed)
  const getChatbotResponse = (userMessage) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve(`AI: Response to '${userMessage}'`);
      }, 1000); // Simulate 1s delay
    });
  };

  const handleSend = async () => {
    if (!input.trim() || isWaitingForResponse) return;

    const userMessage = `User: ${input}`;
    setHistory((prev) => [...prev, userMessage]); // Add user message to history
    setInput(""); // Clear input
    setIsWaitingForResponse(true); // Block further input

    // Fetch chatbot response
    const botResponse = await getChatbotResponse(input);
    setHistory((prev) => [...prev, botResponse]); // Add bot response to history
    setIsWaitingForResponse(false); // Allow further input
  };

  return (
    <div className="absolute top-0 left-0 w-full h-full flex flex-col justify-end items-start pointer-events-none">
      {/* History Panel */}
      {showHistory && (
        <div className="absolute top-0 left-0 w-1/5 h-full bg-white text-white flex flex-col items-center p-2 shadow-lg pointer-events-auto">
          <img className="" src="../../public/textures/nust-seecs.png">
          </img>
          <div className="mt-5 flex flex-col w-full px-2 overflow-y-auto">
            {history.map((message, index) => (
              <div
                key={index}
                className={`mb-2 p-2 rounded cursor-pointer text-sm max-w-[90%] ${message.startsWith("User:") ? "bg-blue-500 text-white self-end" : "bg-gray-200 text-black self-start"}`}
              >
                {message.replace("User: ", "").replace("AI: ", "")}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Toggle Button */}
      <button
        className="absolute top-2 left-[22%] bg-blue-900 text-white px-4 py-2 rounded shadow-md cursor-pointer pointer-events-auto"
        onClick={() => setShowHistory(!showHistory)}
      >
        {showHistory ? "Close" : "Open"}
      </button>

      {/* Chat Input */}
      <div className="absolute bottom-5 left-1/2 transform -translate-x-1/2 w-3/5 h-12 flex items-center bg-white rounded-full shadow-md pointer-events-auto">
        <input
          type="text"
          placeholder="Type a message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={isWaitingForResponse}
          className="flex-1 h-full px-4 text-sm rounded-l-full border-none outline-none cursor-default"
        />
        <button
          onClick={handleSend}
          disabled={isWaitingForResponse}
          className="h-full px-5 bg-green-700 text-white rounded-r-full text-sm cursor-pointer disabled:opacity-50"
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default ChatOverlay;
