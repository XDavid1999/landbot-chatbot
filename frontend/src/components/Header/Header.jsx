// Header.jsx
import React, { useState } from 'react';
import { Layout, Menu, Button, Drawer } from 'antd';
import { MenuOutlined, HomeOutlined, ApiOutlined, WechatFilled, GithubFilled } from '@ant-design/icons';
import { Link } from 'react-router-dom'; // Ensure you have react-router-dom installed
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
    {
      key: 'home',
      icon: <HomeOutlined />,
      label: <Link to="/">Home</Link>,
    },
    {
      key: 'api_test',
      icon: <ApiOutlined />,
      label: <Link to="/topics">API Test</Link>,
    },
    {
      key: 'chat',
      icon: <WechatFilled />,
      label: <Link to="/chats">Chat</Link>,
    },
    {
      key: 'docs',
      icon: <GithubFilled />,
      label: (
        <a href="https://github.com/XDavid1999/landbot-chatbot?tab=readme-ov-file" target="_blank" rel="noopener noreferrer">
          Docs
        </a>
      ),
    },
  ];

  return (
    <AntHeader className="header">
      <div className="header-content">
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
      </div>
      <Drawer
        title="Menu"
        placement="right"
        onClose={onClose}
        open={visible}
      >
        <Menu mode="vertical" items={menuItems} onClick={onClose} />
      </Drawer>
    </AntHeader>
  );
};

export default Header;
