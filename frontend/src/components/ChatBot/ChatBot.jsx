// src/ChatBot.jsx
import React, { useState, useEffect, useRef, useCallback } from 'react';
import Core from '@landbot/core';
import { List, Input, Button, Typography, Spin, Alert } from 'antd';
import { SendOutlined } from '@ant-design/icons';
import './ChatBot.css';

const { Text } = Typography;

const ChatBot = ({ topicId, botToken, onConversationEnd }) => {
  const [messages, setMessages] = useState({});
  const [input, setInput] = useState('');
  const [config, setConfig] = useState(null);
  const [isTyping, setIsTyping] = useState(false);
  const [error, setError] = useState(null);
  const core = useRef(null);

  // Fetch the Landbot configuration based on botToken
  useEffect(() => {
    fetch(`https://landbot.online/v3/${botToken}/index.json`)
      .then((res) => {
        if (!res.ok) {
          throw new Error('Failed to fetch chatbot configuration.');
        }
        return res.json();
      })
      .then(setConfig)
      .catch((error) => {
        console.error('Error fetching config:', error);
        setError('Unable to load chatbot. Please try again later.');
      });
  }, [botToken]);

  // Initialize Landbot Core when config is available
  useEffect(() => {
    if (config) {
      try {
        core.current = new Core(config);
        const subscription = core.current.pipelines.$readableSequence.subscribe((data) => {
          if (data.type === 'typing') {
            setIsTyping(true);
          } else {
            setIsTyping(false);
            setMessages((prevMessages) => {
              const updatedMessages = {
                ...prevMessages,
                [data.key]: parseMessage(data),
              };

              // Check if the conversation has finished
              if (data.action === 'finish') {
                const conversation = conversationToString(updatedMessages);
                console.log('Conversation:', updatedMessages);
                onConversationEnd(conversation);
              }

              return updatedMessages;
            });
          }
        });

        core.current
          .init()
          .then((data) => {
            setMessages(parseMessages(data.messages));
          })
          .catch((error) => {
            console.error('Error initializing Landbot Core:', error);
            setError('Error initializing chatbot. Please try again later.');
          });

        // Cleanup function to unsubscribe and destroy Core
        return () => {
          if (subscription) subscription.unsubscribe();
          if (core.current) {
            core.current.destroy();
          }
        };
      } catch (error) {
        console.error('Error setting up Landbot Core:', error);
        setError('Error setting up chatbot. Please try again later.');
      }
    }
  }, [config, onConversationEnd]);

  // Scroll to the bottom whenever messages or typing state changes
  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  // Function to handle sending messages
  const submit = useCallback(() => {
    if (input.trim() !== '' && core.current) {
      core.current.sendMessage({ message: input.trim() });
      setInput('');
    }
  }, [input]);

  // Function to handle button clicks in dialog messages
  const handleButtonClick = (buttonText) => {
    if (core.current) {
      core.current.sendMessage({ message: buttonText });
    }
  };

  // Function to handle Enter key press
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      submit();
    }
  };

  // Convert conversation messages to a string
  const conversationToString = (messages) => {
    return Object.values(messages)
      .sort((a, b) => a.timestamp - b.timestamp)
      .map((msg) => `${msg.author === 'user' ? 'User' : 'Bot'}: ${msg.text}`)
      .join('\n');
  };

  return (
    <div className="chatbot-container">
      <div className="chatbot-header">
        <Text style={{ fontSize: 20 }} strong>
          🤖 {`Chatting about ${topicId}`}
          <small className="header-hint">Press (esc) to exit</small>
        </Text>
      </div>

      <div className="messages-container" id="chatbot-messages-container">
        {error ? (
          <Alert message="Error" description={error} type="error" showIcon />
        ) : (
          <>
            <List
              dataSource={Object.values(messages)
                .filter(messagesFilter)
                .sort((a, b) => a.timestamp - b.timestamp)}
              renderItem={(message) => (
                <List.Item
                  className={`chatbot-message ${
                    message.author === 'bot' ? 'bot-message' : 'user-message'
                  }`}
                >
                  <div className="message-content">
                    {message.type === 'text' && <Text>{message.text}</Text>}

                    {message.type === 'dialog' && (
                      <div className="dialog-message">
                        <Text>{message.text}</Text>
                        <div className="dialog-buttons">
                          {message.buttons &&
                            message.buttons.length > 0 &&
                            message.buttons.map((button, index) => (
                              <Button
                                key={index}
                                type="primary"
                                onClick={() => handleButtonClick(button)}
                                style={{ marginTop: 8, marginRight: 8 }}
                              >
                                {button}
                              </Button>
                            ))}
                        </div>
                      </div>
                    )}
                    {/* Add more message types as needed */}
                    <small className="message-hour">
                      {new Date(message.timestamp).toLocaleTimeString()}
                    </small>
                  </div>
                </List.Item>
              )}
            />
            {isTyping && (
              <div className="typing-indicator">
                <Spin size="small" /> <Text type="secondary">Bot is typing...</Text>
              </div>
            )}
          </>
        )}
      </div>

      <div className="input-container">
        <Input
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          suffix={
            <Button
              type="primary"
              icon={<SendOutlined />}
              onClick={submit}
              disabled={input.trim() === ''}
            />
          }
          aria-label="Chat message input"
        />
      </div>
    </div>
  );
};

// Helper function to parse individual messages
function parseMessage(data) {
  return {
    key: data.key,
    text: data.title || data.message || '',
    buttons: data.buttons || [],
    author: data.samurai !== undefined ? 'bot' : 'user',
    timestamp: data.timestamp || Date.now(),
    type: data.type || 'text',
    success: !String(data?.extra?.id).includes('error'),
  };
}

// Function to parse multiple messages
function parseMessages(messages) {
  return Object.values(messages).reduce((obj, next) => {
    obj[next.key] = parseMessage(next);
    return obj;
  }, {});
}

// Function to filter supported message types
function messagesFilter(data) {
  /** Support for basic message types */
  return ['text', 'dialog', 'image'].includes(data.type);
}

// Function to scroll the messages container to the bottom
function scrollToBottom() {
  const container = document.getElementById('chatbot-messages-container');
  if (container) {
    container.scrollTo({
      top: container.scrollHeight,
      behavior: 'smooth',
    });
  }
}

export default ChatBot;
