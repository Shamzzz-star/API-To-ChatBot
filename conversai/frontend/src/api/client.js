import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Chat API
export const chatAPI = {
  sendMessage: async (message, sessionId = null) => {
    const response = await api.post('/api/chat/message', {
      message,
      session_id: sessionId,
    });
    return response.data;
  },

  getHistory: async (sessionId, limit = 50) => {
    const response = await api.get(`/api/chat/history/${sessionId}`, {
      params: { limit },
    });
    return response.data;
  },

  createSession: async () => {
    const response = await api.post('/api/chat/session/new');
    return response.data;
  },

  clearSession: async (sessionId) => {
    const response = await api.delete(`/api/chat/session/${sessionId}`);
    return response.data;
  },
};

// API Management
export const apiManagementAPI = {
  listAPIs: async (includeSystem = true) => {
    const response = await api.get('/api/apis/list', {
      params: { include_system: includeSystem },
    });
    return response.data;
  },

  getAPI: async (apiId) => {
    const response = await api.get(`/api/apis/${apiId}`);
    return response.data;
  },

  registerAPI: async (apiData) => {
    const response = await api.post('/api/apis/register', apiData);
    return response.data;
  },

  updateAPI: async (apiId, apiData) => {
    const response = await api.put(`/api/apis/${apiId}`, apiData);
    return response.data;
  },

  testAPI: async (apiId, testParams = {}) => {
    const response = await api.post(`/api/apis/${apiId}/test`, {
      test_params: testParams,
    });
    return response.data;
  },

  deleteAPI: async (apiId) => {
    const response = await api.delete(`/api/apis/${apiId}`);
    return response.data;
  },
};

// Health check
export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

export default api;
