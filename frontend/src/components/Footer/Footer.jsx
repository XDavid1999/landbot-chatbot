// src/components/Footer.jsx
import React from 'react';
import { Layout, Typography, Space } from 'antd';
import { FacebookOutlined, TwitterOutlined, InstagramOutlined } from '@ant-design/icons';
import './Footer.css';

const { Footer: AntFooter } = Layout;
const { Text, Link } = Typography;

const Footer = () => {
  return (
    <AntFooter className="footer">
      <Space size="middle">
        <Link href="#" className="footer-link">
          Privacy Policy
        </Link>
        <Link href="#" className="footer-link">
          Terms of Service
        </Link>
        <Link href="#" className="footer-link">
          Contact Us
        </Link>
      </Space>
      <div className="social-icons">
        <FacebookOutlined />
        <TwitterOutlined />
        <InstagramOutlined />
      </div>
      <div className="footer-text">
        <Text>© {new Date().getFullYear()} My Company. All rights reserved.</Text>
      </div>
    </AntFooter>
  );
};

export default Footer;
