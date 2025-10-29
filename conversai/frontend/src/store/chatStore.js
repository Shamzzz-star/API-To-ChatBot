import { create } from 'zustand';
import { chatAPI } from '../api/client';

const useChatStore = create((set, get) => ({
  // State
  messages: [],
  sessionId: null,
  isLoading: false,
  error: null,
  
  // Actions
  sendMessage: async (message) => {
    const { sessionId, messages } = get();
    
    // Add user message immediately
    const userMessage = {
      message_id: Date.now().toString(),
      role: 'user',
      content: message,
      created_at: new Date().toISOString(),
    };
    
    set({ messages: [...messages, userMessage], isLoading: true, error: null });
    
    try {
      const response = await chatAPI.sendMessage(message, sessionId);
      
      // Add assistant response
      const assistantMessage = {
        message_id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.response,
        created_at: new Date().toISOString(),
        message_metadata: {
          intent: response.intent,
          api_used: response.api_used,
          cached: response.cached,
        },
      };
      
      set({
        messages: [...get().messages, assistantMessage],
        sessionId: response.session_id,
        isLoading: false,
      });
      
      return response;
    } catch (error) {
      const errorMessage = {
        message_id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `❌ Error: ${error.response?.data?.detail || error.message || 'Failed to get response'}`,
        created_at: new Date().toISOString(),
      };
      
      set({
        messages: [...get().messages, errorMessage],
        isLoading: false,
        error: error.message,
      });
      
      throw error;
    }
  },
  
  loadHistory: async () => {
    const { sessionId } = get();
    if (!sessionId) return;
    
    try {
      const history = await chatAPI.getHistory(sessionId);
      set({ messages: history, error: null });
    } catch (error) {
      set({ error: error.message });
    }
  },
  
  createNewSession: async () => {
    try {
      const response = await chatAPI.createSession();
      set({
        messages: [],
        sessionId: response.session_id,
        error: null,
      });
    } catch (error) {
      set({ error: error.message });
    }
  },
  
  clearChat: async () => {
    const { sessionId } = get();
    
    try {
      if (sessionId) {
        await chatAPI.clearSession(sessionId);
      }
      set({
        messages: [],
        sessionId: null,
        error: null,
      });
    } catch (error) {
      set({ error: error.message });
    }
  },
  
  clearError: () => set({ error: null }),
}));

export default useChatStore;
