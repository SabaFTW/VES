import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:3001';

const api = axios.create({
  baseURL: API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add response interceptor for error handling
api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export default {
  // Chat endpoints
  createSession: () => api.post('/api/chat/session'),
  getChatHistory: (sessionId) => api.get(`/api/chat/history/${sessionId}`),
  sendChatMessage: (message, sessionId) =>
    api.post('/api/chat', { message, sessionId }),
  getSessions: () => api.get('/api/chat/sessions'),

  // Direct chat (for trivia/one-off messages without session management)
  chat: async (messages) => {
    // Create temporary session for one-off questions
    const sessionResponse = await api.post('/api/chat/session');
    const sessionId = sessionResponse.data.sessionId;

    // Get last message content (system + user message combined)
    const lastMessage = messages[messages.length - 1];
    const systemMessage = messages.find(m => m.role === 'system');

    // Combine system prompt with user message if exists
    let messageContent = lastMessage.content;
    if (systemMessage && systemMessage !== lastMessage) {
      messageContent = `${systemMessage.content}\n\n${lastMessage.content}`;
    }

    // Send message
    const response = await api.post('/api/chat', {
      message: messageContent,
      sessionId
    });

    return { data: { message: response.data.response, response: response.data.response } };
  },

  // Document endpoints
  getDocuments: (type = null) =>
    api.get('/api/documents', { params: { type } }),
  uploadDocument: (formData) =>
    api.post('/api/documents', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    }),
  deleteDocument: (id) => api.delete(`/api/documents/${id}`),

  // Anchor endpoints
  getAnchors: (type = null) =>
    api.get('/api/anchors', { params: { type } }),
  createAnchor: (data) => api.post('/api/anchors', data),
  updateAnchor: (id, data) => api.put(`/api/anchors/${id}`, data),
  deleteAnchor: (id) => api.delete(`/api/anchors/${id}`),

  // Health check
  health: () => api.get('/health'),

  // System/Provider endpoints
  getProviderInfo: () => api.get('/api/system/provider'),
  testProvider: () => api.get('/api/system/provider/test'),
  getModels: () => api.get('/api/system/models'),
  switchModel: (model) => api.post('/api/system/models/switch', { model })
};
