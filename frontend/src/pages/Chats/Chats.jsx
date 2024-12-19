import React, { useState, useEffect } from 'react';
import { Layout, List, Spin, message } from 'antd';
import {
  MailOutlined,
  SlackSquareOutlined,
  SendOutlined,
  PlayCircleOutlined,
} from '@ant-design/icons';
import axiosInstance from 'api/axiosInstance';
import ChatBot from '@components/ChatBot/ChatBot';
import './Chats.css';

const { Sider, Content } = Layout;

const iconMappings = {
  Email: <MailOutlined />,
  Slack: <SlackSquareOutlined />,
  Telegram: <SendOutlined />,
};

const ChatView = () => {
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState();
  const [selectedTopic, setSelectedTopic] = useState(null);

  useEffect(() => {
    const fetchTopics = async () => {
      try {
        const response = await axiosInstance.get('/dispatcher/topics');
        setTopics(response.data);
      } catch (err) {
        setError('Failed to fetch topics. Please try again later.');
        console.error(err);
      } finally {
        setLoading(false);
      }

      // Add event listener when component mounts
      window.addEventListener('keydown', handleKeyDown);

      // Remove event listener when component unmounts
      return () => {
        window.removeEventListener('keydown', handleKeyDown);
      };
    };

    fetchTopics();
  }, []);

  const handleKeyDown = (event) => {
    if (event.key === 'Escape') {
      setSelectedTopic(null);
    }
  };

  // Function to handle conversation end
  const handleConversationEnd = async (conversation) => {
    if (!selectedTopic) return;

    try {
      const endpoint = '/dispatcher/resolve/';
      await axiosInstance.post(endpoint, {
        topic_id: selectedTopic.name,
        description: conversation,
      });
      message.success(`Successfully sent conversation for ${selectedTopic.name}, to help you!`);
    } catch (err) {
      message.error(`Failed to sent conversation for ${selectedTopic.name}, to help you!`);
      console.error(err);
    } finally {
      setSelectedTopic(null);
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
        <p style={{ color: 'red' }}>{error}</p>
      </div>
    );
  }

  return (
    <Layout className="chat-layout">
      <Sider width={300} className="chat-sider">
        <List
          itemLayout="horizontal"
          dataSource={topics}
          renderItem={(topic) => (
            <List.Item
              className={`chat-topic ${selectedTopic?.name === topic.name ? 'selected' : ''}`}
              onClick={() => {
                setSelectedTopic(topic);
              }}
            >
              <List.Item.Meta
                avatar={iconMappings[topic.notification.method] || <SendOutlined />}
                title={<strong>{topic.name}</strong>}
                description={topic.description}
              />
            </List.Item>
          )}
        />
      </Sider>
      <Layout>
        <Content className="chat-content">
          {selectedTopic ? (
            <ChatBot
              className="chatbot"
              key={selectedTopic.name}
              topicId={selectedTopic.name}
              botToken={selectedTopic.secure_storage_token}
              onConversationEnd={handleConversationEnd}
            />
          ) : (
            <div style={{ textAlign: 'center', marginTop: '20%' }}>
              <h2>Select a chat from the left to start!</h2>
              <PlayCircleOutlined className="big-icon" />
            </div>
          )}
        </Content>
      </Layout>
    </Layout>
  );
};

export default ChatView;
