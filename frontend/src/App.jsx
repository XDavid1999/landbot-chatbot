import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Layout } from 'antd';
import Header from '@components/Header/Header';
import Footer from '@components/Footer/Footer';
import Landing from './pages/Landing/Landing';
import Features from '@components/Features/Features';
import Chats from './pages/Chats/Chats';

import './App.css'; // We'll create or update this next

const { Content } = Layout;

const App = () => {
  return (
    <Router>
      <Layout className="main-layout">
        <Header />
        <Content className="content">
          <Routes>
            <Route path="/topics" element={
              <Content className="content">
                <Features />
              </Content>
            } />
            <Route path="/chats" element={<Chats />} />
            <Route path="*" element={<Landing />} />
          </Routes>
        </Content>
        <Footer />
      </Layout>
    </Router>
  );
};

export default App;
