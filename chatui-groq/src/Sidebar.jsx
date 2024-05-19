import React from "react";

function Sidebar() {
  const sessions = ["Session 1", "Session 2", "Session 3"]; // Example sessions

  return (
      <div className="w-64 bg-slate-800 text-white p-4">
      
      <h2 className="font-bold text-lg mb-4"></h2>
      <ul>
        {sessions.map((session, index) => (
          <li key={index} className="mb-2">
            {session}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Sidebar;


/*



*/