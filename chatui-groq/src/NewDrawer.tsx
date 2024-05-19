import React from "react";
import { Button } from "antd";
import { Drawer } from "antd";

interface DrawerVisible {
  visible: boolean;
  setDrawerClose: () => void;
}

function NewDrawer(visibility: DrawerVisible) {
  return (
    <>
      <div>
        <Drawer
          title=""
          placement={"left"}
          closable={false}
          onClose={visibility.setDrawerClose}
          open={visibility.visible}
          key={"leftDrawer"}
        ></Drawer>
      </div>
    </>
  );
}

export default NewDrawer;
