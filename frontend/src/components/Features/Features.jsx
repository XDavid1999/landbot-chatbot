import React, { useState, useEffect } from 'react';
import { Row, Col, Card, Typography, Spin, message, Input } from 'antd';
import { MailOutlined, SlackSquareOutlined, SendOutlined } from '@ant-design/icons';
import './Features.css';
import axiosInstance from 'api/axiosInstance';

const { Title } = Typography;

const Features = () => {
  const [features, setFeatures] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [actionLoading, setActionLoading] = useState(false); // State for click action loading
  const [description, setDescription] = useState(''); // New state for textbox

  // Mapping for feature icons
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

  // Function to handle card click
  const handleCardClick = async (featureName) => {
    if (!description) {
      message.error('Please enter a description.');
      return;
    }

    const endpoint = "/dispatcher/resolve/";
    setActionLoading(true);
    try {
      const response = await axiosInstance.post(endpoint, {
        "topic_id": featureName,
        "description": description,
      });
      message.success(`Successfully executed ${featureName}`);
      
      // Optionally, clear the textbox after a successful request
      setDescription('');
    } catch (err) {
      message.error(`Failed to execute ${featureName}.`);
      console.error(err);
    } finally {
      setActionLoading(false);
    }
  };

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
        Testing Topics
      </Title>
      
      {/* Textbox for Description */}
      <div>
        <Input.TextArea
          rows={4}
          placeholder="Enter description..."
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          required
        />
      </div>
      
      <Row justify="center" gutter={[16, 16]}>
        {features.map((feature, index) => (
          <Col xs={24} sm={12} md={8} key={index}>
            <Card
              className="feature-card"
              hoverable
              onClick={() => handleCardClick(feature.name)}
              loading={actionLoading}
            >
              <div className="feature-icon">
                {iconMappings[feature.notification.method] || <SendOutlined />}
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
