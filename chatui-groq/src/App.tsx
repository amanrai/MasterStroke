import React from "react";
import Sidebar from "./Sidebar.jsx";
import MainContent from "./MainContent.tsx";
import UserChatInput from "./UserChatInput.jsx";
import NewDrawer from "./NewDrawer.tsx";
import SettingsMenu from "./SettingsMenu.tsx";
import { SettingsProvider } from "./SettingsProvider.tsx";

const drawer_items = [
  {
    title: "New Session",
    action: "NewSession",
    type: "Button",
  },
  {
    title: "Your Previous Sessions",
    type: "list",
    source: "/sessions",
  },
  {
    title: "Settings",
    type: "Button",
    action: "showSettings",
  },
];

function App() {
  <SettingsProvider>
    <></>
  </SettingsProvider>;
  const [openDrawer, setOpenDrawer] = React.useState(false);
  const [openSettings, setOpenSettings] = React.useState(false);
  const [darkMode, setDarkMode] = React.useState(false);
  const [connectionStatus, setConnectionStatus] = React.useState(false);
  const [model, setModel] = React.useState("llama3-8b-8192");

  const setDrawerStatus = () => {
    setOpenDrawer(!openDrawer);
    console.log("Make Drawer Visible: " + openDrawer);
  };

  const setSettingsVisiblity = () => {
    setOpenSettings(!openSettings);
    console.log("Make Settings Visible: " + openSettings);
  };

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
    console.log("Dark Mode: " + darkMode);
  };

  const updateSetting = (setting, value) => {
    console.log("Updating Setting: " + setting + " to " + value);
  };

  return (
    <div>
      <div className="flex flex-row min-h-screen">
        {/* <Sidebar /> */}

        <NewDrawer visible={openDrawer} setDrawerClose={setDrawerStatus} />

        <SettingsMenu
          visible={openSettings}
          closeSettings={setSettingsVisiblity}
          propTemperature={0.9}
          propUseAgent={true}
          propUseWebSearch={true}
        ></SettingsMenu>

        <MainContent
          drawerSetter={setDrawerStatus}
          settingsSetter={setSettingsVisiblity}
          darkModeSetter={toggleDarkMode}
        />
      </div>
    </div>
  );
}

export default App;
