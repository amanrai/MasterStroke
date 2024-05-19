import React from "react";
import { createContext, useState, useEffect } from "react";
import { getSettings } from "./apiInteractor";

export const SettingsContext = createContext({});

export const SettingsProvider = ({ children }) => {
  const [settings, setSettings] = useState({
    temperature: 0.9,
    useAgent: true,
    useWebSearch: true,
    model: "llama3-8b-8192",
    groq_api_key: "",
    brave_api_key: "",
  });

  useEffect(() => {
    getSettings().then((data) => {
      console.log(data);
      setSettings(data);
    });
  }, []);

  return (
    <SettingsContext.Provider value={{ settings, setSettings }}>
      {children}
    </SettingsContext.Provider>
  );
};
