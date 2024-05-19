import React from 'react';
import { IoSettingsOutline } from "react-icons/io5";
import "./MainContent.css"

function SettingsButton({ onClick }) {
  return (
    <button
      onClick={onClick}
      className="px-5 rounded-full stroke:gray hover:scale-110 hover:stroke-black pb-5">
      <IoSettingsOutline />
    </button>
  );
}

export default SettingsButton;
