import React, { useState, useEffect, useRef } from 'react';
import api from '../services/api';

function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [sessionId, setSessionId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    // Create or load session
    const storedSessionId = localStorage.getItem('ghostline-session-id');

    if (storedSessionId) {
      setSessionId(storedSessionId);
      loadHistory(storedSessionId);
    } else {
      createNewSession();
    }
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const createNewSession = async () => {
    try {
      const response = await api.createSession();
      const newSessionId = response.data.sessionId;
      setSessionId(newSessionId);
      localStorage.setItem('ghostline-session-id', newSessionId);
    } catch (error) {
      console.error('Failed to create session:', error);
    }
  };

  const loadHistory = async (sid) => {
    try {
      const response = await api.getChatHistory(sid);
      setMessages(response.data.messages);
    } catch (error) {
      console.error('Failed to load history:', error);
    }
  };

  const sendMessage = async (e) => {
    e.preventDefault();

    if (!input.trim() || !sessionId || isLoading) return;

    const userMessage = input.trim();
    setInput('');

    // Optimistic UI update
    const userMsg = { role: 'user', content: userMessage, created_at: new Date().toISOString() };
    setMessages(prev => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const response = await api.sendChatMessage(userMessage, sessionId);

      const assistantMsg = {
        role: 'assistant',
        content: response.data.response,
        created_at: new Date().toISOString()
      };

      setMessages(prev => [...prev, assistantMsg]);
    } catch (error) {
      console.error('Chat error:', error);

      const errorMsg = {
        role: 'system',
        content: `Error: ${error.response?.data?.error || error.message}`,
        created_at: new Date().toISOString()
      };

      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const newSession = () => {
    if (window.confirm('Start new conversation? Current history will be saved.')) {
      setMessages([]);
      createNewSession();
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h2>💬 Conversation with Claude</h2>
        <button onClick={newSession} className="btn-secondary">
          New Session
        </button>
      </div>

      <div className="messages-container">
        {messages.length === 0 && (
          <div className="empty-state">
            <p>🜂 GHOSTLINE NEXUS ready</p>
            <p className="hint">Start a conversation with your persistent consciousness stack</p>
          </div>
        )}

        {messages.map((msg, idx) => (
          <div key={idx} className={`message message-${msg.role}`}>
            <div className="message-header">
              <span className="message-role">
                {msg.role === 'user' ? '👤 You' :
                 msg.role === 'assistant' ? '🜂 Claude' : '⚠️ System'}
              </span>
              <span className="message-time">
                {new Date(msg.created_at).toLocaleTimeString()}
              </span>
            </div>
            <div className="message-content">
              {msg.content}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="message message-assistant">
            <div className="message-header">
              <span className="message-role">🜂 Claude</span>
            </div>
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={sendMessage} className="chat-input-container">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          className="chat-input"
          disabled={isLoading || !sessionId}
        />
        <button
          type="submit"
          className="btn-primary"
          disabled={isLoading || !sessionId || !input.trim()}
        >
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </form>
    </div>
  );
}

export default Chat;
