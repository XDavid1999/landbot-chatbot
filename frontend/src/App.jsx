// src/App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Layout } from 'antd';
import Header from './components/Header/Header';
import Footer from './components/Footer/Footer';
import Landing from './pages/Landing/Landing';
import Hero from './components/Hero/Hero';
import Features from './components/Features/Features';

import './App.css'; // We'll create or update this next

const { Content } = Layout;

const App = () => {
  return (
    <Router>
      <Layout className="main-layout">
        <Header />
        <Content className="content">
          <Routes>
            <Route path="/" element={
              <Content className="content">
                <Hero />
                <Features />
                </Content>
            } />
            <Route path="*" element={<Landing />} />
          </Routes>
        </Content>
        <Footer />
      </Layout>
    </Router>
  );
};

export default App;
