import React from "react";
import UserChatInput from "./UserChatInput";
import SettingsButton from "./SettingsButton";
import ChatDisplay from "./ChatDisplay";
import ConnectionStatus from "./ConnectionStatus";
import { PiHamburgerThin } from "react-icons/pi";
import "./MainContent.css";

interface MainScreenToggles {
  drawerSetter: () => void;
  settingsSetter: () => void;
  darkModeSetter: () => void;
}

function MainContent(toggles: MainScreenToggles) {
  const toggleDrawerStatus = () => {
    toggles.drawerSetter();
  };

  const toggleSettingsVisibility = () => {
    toggles.settingsSetter();
  };

  const toggleDarkMode = () => {
    toggles.darkModeSetter();
  };

  const header_bg = "bg-slate-100";
  const screen_bg = "bg-slate-100";

  return (
    <>
      <div className={"flex-grow h-screen " + screen_bg}>
        {/*This is the header */}
        <div className={"flex flex-row pt-5 pl-5 h-1/6 max-h-14 " + header_bg}>
          <button
            className="flex flex-grow w-1 h-full"
            onClick={() => toggleDrawerStatus()}
          >
            <PiHamburgerThin className="header-menu-button-left" />
          </button>
          {/* <h1 className="font-bold text-xl mb-4" style={{ flex: "9" }}>
            connected.
          </h1> */}
          <ConnectionStatus isConnected={true} />
          <SettingsButton onClick={toggleSettingsVisibility} />
        </div>

        {/*This is the chat area */}
        <div className="flex w-full h-5/6 items-center justify-center pt-2">
          <div className="flex w-1/5 h-full "></div>
          <div className="w-3/5 h-full">
            <ChatDisplay />
          </div>
          <div className="flex flex-grow w-1/5  h-full"></div>
        </div>

        {/* this is the input area */}
        <div className="flex w-full  items-center justify-center">
          <div className="flex flex-row w-1/5 "></div>
          <div className="w-3/5 pt-1  shadow-lg">
            <UserChatInput />
          </div>
          <div className="flex flex-grow w-1/5 "></div>
        </div>
      </div>
    </>
  );
}

export default MainContent;
