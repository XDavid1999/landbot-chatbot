import React from 'react';
import { Layout, Typography, Space } from 'antd';
import './Footer.css';

const { Footer: AntFooter } = Layout;
const { Text, Link } = Typography;

const Footer = () => {
  return (
    <AntFooter className="footer">
      <Space size="middle">
        <Link href="#" className="footer-link">
            Landbot Challenge
        </Link>
      </Space>
      <div className="footer-text">
        <Text>© {new Date().getFullYear()} My Company. All rights reserved.</Text>
      </div>
    </AntFooter>
  );
};

export default Footer;
