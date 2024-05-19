import React from "react";
import { DisconnectOutlined } from "@ant-design/icons";
import { ApiOutlined } from "@ant-design/icons";
import { TbPlugConnectedX } from "react-icons/tb";
import { PiPlugsConnectedLight } from "react-icons/pi";

function ConnectionStatus({ isConnected }) {
  return (
    <>
      <div>
        {isConnected ? <PiPlugsConnectedLight /> : <TbPlugConnectedX />}
      </div>
    </>
  );
}

export default ConnectionStatus;
