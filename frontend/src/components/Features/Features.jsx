// src/components/Features.jsx
import React, { useState, useEffect } from 'react';
import { Row, Col, Card, Typography, Spin } from 'antd';
import { MailOutlined, SlackSquareOutlined, SendOutlined } from '@ant-design/icons';
import './Features.css';
import axiosInstance from 'api/axiosInstance';

const { Title } = Typography;

const Features = () => {
  const [features, setFeatures] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const iconMappings = {
    "Email": <MailOutlined />,
    "Slack": <SlackSquareOutlined />,
    "Telegram": <SendOutlined />,
  };

  useEffect(() => {
    const fetchFeatures = async () => {
      try {
        const response = await axiosInstance.get('/dispatcher/topics');
        setFeatures(response.data);
      } catch (err) {
        setError('Failed to fetch features. Please try again later.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchFeatures();
  }, []);

  if (loading) {
    return (
      <div className="loading-container">
        <Spin size="large" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <Typography.Text type="danger">{error}</Typography.Text>
      </div>
    );
  }

  return (
    <section className="features-section">
      <Title level={2} className="features-title">
        Our Features
      </Title>
      <Row justify="center">
        {features.map((feature, index) => (
          <Col xs={24} sm={12} md={8} key={index}>
            <Card className="feature-card" hoverable>
              <div className="feature-icon">
                {iconMappings[feature.notification.method]}
              </div>
              <Card.Meta title={feature.name} description={feature.description} />
            </Card>
          </Col>
        ))}
      </Row>
    </section>
  );
};

export default Features;
