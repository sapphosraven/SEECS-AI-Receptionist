import React, { useState, useContext } from "react";
import { AnimationContext } from "../App"; // Import the context

function ChatOverlay() {
  const [showHistory, setShowHistory] = useState(false);
  const [history, setHistory] = useState([]);
  const [input, setInput] = useState("");
  const [isWaitingForResponse, setIsWaitingForResponse] = useState(false);
  const [isMicActive, setIsMicActive] = useState(false);
  const { setIsThinking } = useContext(AnimationContext); // Access the context
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
    setHistory((prev) => [...prev, userMessage]);
    setInput("");
    setIsWaitingForResponse(true);

    const botResponse = await getChatbotResponse(input);
    setHistory((prev) => [...prev, botResponse]);
    setIsWaitingForResponse(false);
  };

  const handleMicClick = async () => {
    try {
      setIsMicActive(true);
      const response = await fetch("http://localhost:5000/api/run-stt", { method: "POST" });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      if (data.transcription) {
        console.log(data.transcription);
      }
      setIsThinking(true); // Trigger thinking animation on mic click

    } catch (error) {
      console.error("Error running STT:", error);
    } finally {
      setIsMicActive(false);
    }
  };

  return (
    <div className="absolute top-0 left-0 w-full h-full flex flex-col justify-end items-start pointer-events-none">
      <div
        className={`absolute top-0 left-0 h-full bg-white text-black flex flex-col items-center p-2 shadow-lg pointer-events-auto transition-transform duration-300 ${showHistory ? "translate-x-0" : "-translate-x-full"}`}
        style={{ width: "20%" }}
      >
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

      <button
        className={`absolute top-2 transition-transform duration-300 ${showHistory ? "translate-x-[80px]" : "translate-x-0"} bg-blue-900 text-white px-4 py-2 rounded shadow-md cursor-pointer pointer-events-auto`}
        style={{ left: "20px" }}
        onClick={() => setShowHistory(!showHistory)}
      >
        {showHistory ? "Close" : "Chat Log"}
      </button>

      <div
        className={`absolute bottom-5 transition-transform duration-300 left-1/2 transform ${showHistory ? "-translate-x-[35%]" : "-translate-x-1/2"} w-3/5 flex items-center gap-2 pointer-events-auto`}
      >
        <div className="flex-1 h-12 flex items-center bg-white rounded-full shadow-md">
          <input
            type="text"
            placeholder="Type a message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isWaitingForResponse}
            className="flex-1 h-full px-4 text-sm rounded-l-full border-none outline-none cursor-pointer"
          />
          <button
            onClick={handleSend}
            disabled={isWaitingForResponse}
            className="h-full px-5 bg-green-700 text-white rounded-r-full text-sm cursor-pointer disabled:opacity-50"
          >
            Send
          </button>
        </div>

        <button
          onClick={handleMicClick}
          className={`h-12 w-12 rounded-full flex items-center justify-center shadow-md cursor-pointer ${isMicActive ? "bg-yellow-500 animate-pulse" : "bg-red-500"}`}
        >
          {isMicActive ? (
            <div className="w-6 h-6 border-4 border-t-4 border-t-white border-red-500 rounded-full animate-spin"></div>
          ) : (
            <img src="../../public/textures/mic.png" alt="Mic" className="h-6 w-6" />
          )}
        </button>
      </div>
    </div>
  );
}

export default ChatOverlay;
