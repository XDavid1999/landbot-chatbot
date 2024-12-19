import React from 'react';
import { Link } from 'react-router-dom';
import { Button, Typography, Space } from 'antd';
import { ArrowRightOutlined } from '@ant-design/icons';
import './Landing.css'; // We'll create this CSS file for additional styles

const { Title, Paragraph } = Typography;

const Landing = () => {
  return (
    <div className="landing-container">
      <div className="overlay"></div>
      <Space direction="vertical" size="large" align="center" className="content">
        <Title className="main-title">Welcome to <span>LandBot Challenge</span></Title>
        <Paragraph className="subtitle">David Heredia</Paragraph>
        <Link to="/topics">
          <Button type="primary" size="large" className="login-button" icon={<ArrowRightOutlined />}>
            Get Started
          </Button>
        </Link>
      </Space>
    </div>
  );
};

export default Landing;
