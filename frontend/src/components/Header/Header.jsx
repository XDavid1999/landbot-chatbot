import React, { useState } from 'react';
import { Layout, Menu, Button, Drawer } from 'antd';
import { MenuOutlined } from '@ant-design/icons';
import './Header.css';

const { Header: AntHeader } = Layout;

const Header = () => {
  const [visible, setVisible] = useState(false);

  const showDrawer = () => {
    setVisible(true);
  };

  const onClose = () => {
    setVisible(false);
  };

  const menuItems = [
  ];

  return (
    <AntHeader className="header">
      <img src="/icon.png" alt="Landbot" className="logo" />
      <div className="title">Landbot Challenge</div>
      <div className="desktop-menu">
        <Menu theme="dark" mode="horizontal" items={menuItems} />
      </div>
      <Button
        type="text"
        icon={<MenuOutlined />}
        onClick={showDrawer}
        className="mobile-menu-button"
      />
      <Drawer placement="right" onClose={onClose} open={visible}>
        <Menu mode="vertical" items={menuItems} onClick={onClose} />
      </Drawer>
    </AntHeader>
  );
};

export default Header;
