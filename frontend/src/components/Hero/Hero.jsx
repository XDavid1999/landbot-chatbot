// src/components/Hero.jsx
import React from 'react';
import { Row, Col, Button, Typography } from 'antd';
import './Hero.css';

const { Title, Paragraph } = Typography;

const Hero = () => {
  return (
    <section className="hero-section">
      <Row justify="center" align="middle" className="hero-row">
        <Col xs={24} md={12} className="hero-content">
          <Title>Welcome to Our Product</Title>
          <Paragraph>
            Discover the features that make our product stand out. Join us today and transform your experience.
          </Paragraph>
          <Button type="primary" size="large">
            Get Started
          </Button>
        </Col>
      </Row>
    </section>
  );
};

export default Hero;
