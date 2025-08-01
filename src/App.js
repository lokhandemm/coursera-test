import React, { useState, useRef, useEffect } from 'react';
import styled, { createGlobalStyle } from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Bot, User, Lightbulb, Target, Palette, Share2, Sparkles } from 'lucide-react';
import axios from 'axios';

const GlobalStyle = createGlobalStyle`
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
  }
`;

const AppContainer = styled.div`
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
`;

const Header = styled.header`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  padding: 1rem 2rem;
  text-align: center;
`;

const Title = styled.h1`
  color: white;
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
`;

const Subtitle = styled.p`
  color: rgba(255, 255, 255, 0.8);
  font-size: 1.1rem;
  font-weight: 300;
`;

const ChatContainer = styled.div`
  flex: 1;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  padding: 2rem;
  display: flex;
  flex-direction: column;
`;

const MessagesContainer = styled.div`
  flex: 1;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 2rem;
  margin-bottom: 2rem;
  overflow-y: auto;
  max-height: 60vh;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
`;

const Message = styled(motion.div)`
  display: flex;
  margin-bottom: 1.5rem;
  align-items: flex-start;
  gap: 1rem;
`;

const MessageIcon = styled.div`
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  background: ${props => props.isUser ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' : 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'};
  color: white;
`;

const MessageContent = styled.div`
  flex: 1;
  background: ${props => props.isUser ? 'rgba(102, 126, 234, 0.1)' : 'rgba(255, 255, 255, 0.8)'};
  padding: 1rem 1.5rem;
  border-radius: 18px;
  border: 1px solid ${props => props.isUser ? 'rgba(102, 126, 234, 0.2)' : 'rgba(0, 0, 0, 0.1)'};
  white-space: pre-line;
  line-height: 1.6;
`;

const StepsList = styled.ol`
  margin: 1rem 0;
  padding-left: 1.5rem;
  
  li {
    margin: 0.5rem 0;
    line-height: 1.6;
  }
`;

const NamesList = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin: 1rem 0;
`;

const NameCard = styled.div`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem;
  border-radius: 12px;
  text-align: center;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s;
  
  &:hover {
    transform: translateY(-2px);
  }
`;

const LogoPrompt = styled.div`
  background: rgba(102, 126, 234, 0.1);
  border: 2px dashed rgba(102, 126, 234, 0.3);
  padding: 1.5rem;
  border-radius: 12px;
  margin: 1rem 0;
  font-family: monospace;
  font-size: 0.9rem;
  line-height: 1.6;
`;

const SocialMediaContent = styled.div`
  background: rgba(245, 87, 108, 0.1);
  border-left: 4px solid #f5576c;
  padding: 1.5rem;
  border-radius: 12px;
  margin: 1rem 0;
`;

const IdeasGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin: 1rem 0;
`;

const IdeaCard = styled.div`
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
  padding: 1.5rem;
  border-radius: 12px;
  font-size: 0.9rem;
  line-height: 1.5;
`;

const InputContainer = styled.div`
  display: flex;
  gap: 1rem;
  background: rgba(255, 255, 255, 0.95);
  padding: 1.5rem;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
`;

const BusinessIdeaInput = styled.input`
  flex: 1;
  padding: 1rem;
  border: 2px solid rgba(102, 126, 234, 0.2);
  border-radius: 12px;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.2s;
  
  &:focus {
    border-color: #667eea;
  }
  
  &::placeholder {
    color: rgba(0, 0, 0, 0.5);
  }
`;

const MessageInput = styled.input`
  flex: 2;
  padding: 1rem;
  border: 2px solid rgba(102, 126, 234, 0.2);
  border-radius: 12px;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.2s;
  
  &:focus {
    border-color: #667eea;
  }
  
  &::placeholder {
    color: rgba(0, 0, 0, 0.5);
  }
`;

const SendButton = styled.button`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  transition: transform 0.2s;
  
  &:hover {
    transform: translateY(-2px);
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }
`;

const QuickActions = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin: 1rem 0;
  justify-content: center;
`;

const QuickActionButton = styled.button`
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  padding: 0.75rem 1.5rem;
  border-radius: 25px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
  transition: all 0.2s;
  backdrop-filter: blur(10px);
  
  &:hover {
    background: rgba(255, 255, 255, 0.3);
    transform: translateY(-2px);
  }
`;

function App() {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [businessIdea, setBusinessIdea] = useState('');
  const [businessName, setBusinessName] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async (message = inputMessage) => {
    if (!message.trim() && !businessIdea.trim()) return;

    const userMessage = {
      id: Date.now(),
      text: message,
      isUser: true,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await axios.post('/api/chat', {
        message: message,
        business_idea: businessIdea,
        business_name: businessName
      });

      const botMessage = {
        id: Date.now() + 1,
        text: response.data.message,
        isUser: false,
        timestamp: new Date(),
        type: response.data.type,
        data: response.data.data
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error. Please try again.',
        isUser: false,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuickAction = (action) => {
    sendMessage(action);
  };

  const handleNameSelect = (name) => {
    setBusinessName(name);
    sendMessage(`I like the name "${name}". Can you create a logo for it?`);
  };

  const renderMessageContent = (message) => {
    if (message.type === 'steps' && message.data) {
      return (
        <>
          <div>{message.text}</div>
          <StepsList>
            {message.data.map((step, index) => (
              <li key={index}>{step}</li>
            ))}
          </StepsList>
        </>
      );
    }

    if (message.type === 'names' && message.data) {
      return (
        <>
          <div>{message.text}</div>
          <NamesList>
            {message.data.map((name, index) => (
              <NameCard key={index} onClick={() => handleNameSelect(name)}>
                {name}
              </NameCard>
            ))}
          </NamesList>
        </>
      );
    }

    if (message.type === 'logo_prompt' && message.data) {
      return (
        <>
          <div>{message.text}</div>
          <LogoPrompt>{message.data}</LogoPrompt>
        </>
      );
    }

    if (message.type === 'social_media' && message.data) {
      return (
        <>
          <div>{message.text}</div>
          <SocialMediaContent>
            <h4 style={{ marginBottom: '1rem', color: '#f5576c' }}>{message.data.format}</h4>
            <div>{message.data.content}</div>
          </SocialMediaContent>
        </>
      );
    }

    if (message.type === 'ideas' && message.data) {
      return (
        <>
          <div>{message.text}</div>
          <IdeasGrid>
            {message.data.map((idea, index) => (
              <IdeaCard key={index}>{idea}</IdeaCard>
            ))}
          </IdeasGrid>
        </>
      );
    }

    return message.text;
  };

  return (
    <>
      <GlobalStyle />
      <AppContainer>
        <Header>
          <Title>
            <Bot size={32} />
            Small Business Assistant
          </Title>
          <Subtitle>Your one-stop solution for turning business ideas into reality</Subtitle>
        </Header>

        <ChatContainer>
          <MessagesContainer>
            <AnimatePresence>
              {messages.map((message) => (
                <Message
                  key={message.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  transition={{ duration: 0.3 }}
                >
                  <MessageIcon isUser={message.isUser}>
                    {message.isUser ? <User size={20} /> : <Bot size={20} />}
                  </MessageIcon>
                  <MessageContent isUser={message.isUser}>
                    {renderMessageContent(message)}
                  </MessageContent>
                </Message>
              ))}
            </AnimatePresence>
            {isLoading && (
              <Message
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
              >
                <MessageIcon>
                  <Bot size={20} />
                </MessageIcon>
                <MessageContent>
                  <div>Thinking... 🤔</div>
                </MessageContent>
              </Message>
            )}
            <div ref={messagesEndRef} />
          </MessagesContainer>

          {messages.length === 0 && (
            <QuickActions>
              <QuickActionButton onClick={() => handleQuickAction('Give me steps to start a coffee shop')}>
                <Target size={16} />
                Business Steps
              </QuickActionButton>
              <QuickActionButton onClick={() => handleQuickAction('Suggest names for my business')}>
                <Sparkles size={16} />
                Name Ideas
              </QuickActionButton>
              <QuickActionButton onClick={() => handleQuickAction('Create a LinkedIn post')}>
                <Share2 size={16} />
                Social Media
              </QuickActionButton>
              <QuickActionButton onClick={() => handleQuickAction('Give me innovative ideas')}>
                <Lightbulb size={16} />
                Innovation
              </QuickActionButton>
              <QuickActionButton onClick={() => handleQuickAction('Create a logo')}>
                <Palette size={16} />
                Logo Design
              </QuickActionButton>
            </QuickActions>
          )}

          <InputContainer>
            <BusinessIdeaInput
              type="text"
              placeholder="Your business idea (e.g., coffee shop, online tutoring, handmade jewelry)"
              value={businessIdea}
              onChange={(e) => setBusinessIdea(e.target.value)}
            />
            <MessageInput
              type="text"
              placeholder="Ask me anything about your business..."
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            />
            <SendButton onClick={() => sendMessage()} disabled={isLoading}>
              <Send size={20} />
              Send
            </SendButton>
          </InputContainer>
        </ChatContainer>
      </AppContainer>
    </>
  );
}

export default App;