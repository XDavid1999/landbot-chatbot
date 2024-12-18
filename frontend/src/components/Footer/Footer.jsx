import React from 'react';
import { Layout, Typography, Space } from 'antd';
import './Footer.css';

const { Footer: AntFooter } = Layout;
const { Link } = Typography;

const Footer = () => {
  return (
    <AntFooter className="footer">
      <Space size="middle">
        <Link href="#" className="footer-link">
            David Heredia
        </Link>
      </Space>
    </AntFooter>
  );
};

export default Footer;
