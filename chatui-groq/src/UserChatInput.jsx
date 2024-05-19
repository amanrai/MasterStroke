import React, { useState } from "react";

function UserChatInput() {
  const [message, setMessage] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Message to send:", message);
    setMessage(""); // Clear message after sending
  };

  return (
    
    // <form onSubmit={handleSubmit} className="flex items-center border border-gray-300 rounded-lg overflow-hidden">
    <form onSubmit={handleSubmit} className="flex flex-grow rounded-lg bg-white bottom-0 left-0 right-0 px-2 py-2 ">
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="say something..."
        className="flex-1 p-2 text-lg border-none focus:ring-0"
      />
      <button
        type="submit"
        className="px-4 py-2 hover:scale-105 text-black">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" className="w-6 h-6">
          <path strokeLinecap="round" strokeLinejoin="round" d="M6 12 3.269 3.125A59.769 59.769 0 0 1 21.485 12 59.768 59.768 0 0 1 3.27 20.875L5.999 12Zm0 0h7.5" />
        </svg>
      </button>
    </form>
  );
}

export default UserChatInput;
