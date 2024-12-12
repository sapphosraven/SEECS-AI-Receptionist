import React, { useState } from "react";

function ChatOverlay() {
  const [showHistory, setShowHistory] = useState(false);

  return (
    <div className="absolute top-0 left-0 w-full h-full flex flex-col justify-end items-start pointer-events-none">
      {/* History Panel */}
      {showHistory && (
        <div className="absolute top-0 left-0 w-1/5 h-full bg-blue-900 text-white flex flex-col items-center p-2 shadow-lg pointer-events-auto">
          <h3 className="text-lg font-bold text-center h-8 flex items-center justify-center">
            LOGO
          </h3>
          <div className="mt-5 flex flex-col w-full px-2">
            <div className="mb-2 p-2 bg-white/10 rounded cursor-pointer">
              AI: Hey! how are you doing?
            </div>
            <div className="mb-2 p-2 bg-white/10 rounded cursor-pointer">
              user: Great! Can you help me out?
            </div>
            <div className="mb-2 p-2 bg-white/10 rounded cursor-pointer">
              AI: Hey! how are you doing?
            </div>
            <div className="mb-2 p-2 bg-white/10 rounded cursor-pointer">
              user: Great! Can you help me out?
            </div>
          </div>
        </div>
      )}

      {/* Toggle Button */}
      <button
        className="absolute top-2 left-[22%] bg-blue-900 text-white px-4 py-2 rounded shadow-md cursor-pointer pointer-events-auto"
        onClick={() => setShowHistory(!showHistory)}
      >
        {showHistory ? "ICON" : "ICON"}
      </button>

      {/* Chat Input */}
      <div className="absolute bottom-5 left-1/2 transform -translate-x-1/2 w-3/5 h-12 flex items-center bg-white rounded-full shadow-md pointer-events-auto">
        <input
          type="text"
          placeholder="Type a message..."
          className="flex-1 h-full px-4 text-sm rounded-l-full border-none outline-none"
        />
        <button className="h-full px-5 bg-blue-900 text-white rounded-r-full text-sm cursor-pointer">
          Send
        </button>
      </div>
    </div>
  );
}

export default ChatOverlay;
