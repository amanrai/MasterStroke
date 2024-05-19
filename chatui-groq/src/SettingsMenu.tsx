import React, { useContext } from "react";
import { Button } from "antd";
import { Drawer } from "antd";
import type { MenuProps } from "antd";
import { Select, Space } from "antd";
import { Form, Input, InputNumber, Switch } from "antd";
import type { InputNumberProps } from "antd";
import { SettingsContext, SettingsProvider } from "./SettingsProvider.tsx";

type MenuItem = Required<MenuProps>["items"][number];

interface settingsMenuProperties {
  visible: boolean;
  propUseAgent: boolean;
  propUseWebSearch: boolean;
  propTemperature: number;
  closeSettings: () => void;
  // updateSetting(setting: string, value: string): void;
}

const items: MenuItem = [{}];

function SettingsMenu(inputs: settingsMenuProperties) {
  
  const settings = React.useContext(SettingsContext);

  
  const _updateSetting = (setting: string, value: string) => {
    // inputs.updateSetting(setting, value);
  };

  const chooseModel = (value: string) => {
    _updateSetting("model", value);
    console.log("Chose Model: " + value);
  };

  const setTemperature: InputNumberProps["onChange"] = (value) => {
    _updateSetting("temperature", value.toString());
    console.log("New Temperature: " + value);
  };

  const updateGroqAPIKey = (value) => {
    console.log("Groq API Key: " + value);
  };

  const updateBraveAPIKey = (value) => {
    console.log("Brave API Key: " + value);
  };

  const changeAgentBehaviour = (value) => {
    console.log("Agent Behaviour: " + value);
  };

  const changeWebSearchBehaviour = (value) => {
    console.log("Web Search Behaviour: " + value);
    inputs.propUseWebSearch = value;
  };
  return (
    <>
      <SettingsProvider>
        <div>
          <Drawer
            title="Settings"
            placement={"right"}
            closable={false}
            onClose={inputs.closeSettings}
            open={inputs.visible}
            key={"settingsDrawer"}
          >
            <Form layout="vertical">
              <Form.Item name="model" label="Model">
                <Select
                  defaultValue={settings.model}
                  onChange={chooseModel}
                  style={{ width: 250, alignContent: "right" }}
                  options={[
                    { value: "llama3-8b-8192", label: "Llama 3 8b" },
                    { value: "llama3-70b-8192", label: "Llama 3 70b" },
                    { value: "Gemma-7b-It", label: "Gemma 7b" },
                  ]}
                ></Select>
              </Form.Item>
              <Form.Item name="temperature" label="Temperature">
                <InputNumber
                  min={0.01}
                  max={2.0}
                  defaultValue={0.9}
                  step={0.1}
                  onChange={setTemperature}
                />
              </Form.Item>
              <Form.Item name="GroqAPIKey" label="Groq API Key">
                <Input onChange={updateGroqAPIKey} />
              </Form.Item>
              <Form.Item name="behaviour" label="Behaviour">
                <Space direction="vertical">
                  <Switch
                    checkedChildren="Use An Agent"
                    unCheckedChildren="Do Not Use An Agent"
                    defaultChecked
                    style={{ width: 250 }}
                    onChange={changeAgentBehaviour}
                  />
                  <Switch
                    checkedChildren="Use Web Search"
                    unCheckedChildren="Do Not Use Web Search"
                    {...(inputs.propUseWebSearch
                      ? { defaultChecked: true }
                      : {})}
                    style={{ width: 250 }}
                    onChange={changeWebSearchBehaviour}
                  />
                  {inputs.propUseWebSearch ? (
                    <Form.Item
                      name="braveAPIKey"
                      label="Brave API Key (for search)"
                    >
                      <Input onChange={updateBraveAPIKey} />
                    </Form.Item>
                  ) : null}
                </Space>
              </Form.Item>
            </Form>
          </Drawer>
        </div>
      </SettingsProvider>
    </>
  );
}
export default SettingsMenu;
