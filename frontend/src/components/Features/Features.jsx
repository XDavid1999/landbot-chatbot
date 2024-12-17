// src/components/Features.jsx
import React from 'react';
import { Row, Col, Card, Typography } from 'antd';
import { AppstoreOutlined, RocketOutlined, SmileOutlined } from '@ant-design/icons';
import './Features.css';

const { Title } = Typography;

const featuresData = [
  {
    icon: <AppstoreOutlined />,
    title: 'Feature One',
    description: 'Description of feature one. It offers great benefits and value.',
  },
  {
    icon: <RocketOutlined />,
    title: 'Feature Two',
    description: 'Description of feature two. It accelerates your workflow.',
  },
  {
    icon: <SmileOutlined />,
    title: 'Feature Three',
    description: 'Description of feature three. It enhances user satisfaction.',
  },
];

const Features = () => {
  return (
    <section className="features-section">
      <Title level={2} className="features-title">
        Our Features
      </Title>
      <Row justify="center">
        {featuresData.map((feature, index) => (
          <Col xs={24} sm={12} md={8} key={index}>
            <Card className="feature-card" hoverable>
              <div className="feature-icon">{feature.icon}</div>
              <Card.Meta title={feature.title} description={feature.description} />
            </Card>
          </Col>
        ))}
      </Row>
    </section>
  );
};

export default Features;
