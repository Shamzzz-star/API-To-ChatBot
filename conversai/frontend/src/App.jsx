import React, { useState } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import ChatMessages from './components/ChatMessages';
import ChatInput from './components/ChatInput';
import useChatStore from './store/chatStore';
import { Menu } from 'lucide-react';

function App() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const { messages, isLoading, sendMessage, clearChat } = useChatStore();
  
  const handleSendMessage = async (message) => {
    try {
      await sendMessage(message);
    } catch (error) {
      console.error('Failed to send message:', error);
    }
  };
  
  const handleNewChat = async () => {
    if (window.confirm('Start a new conversation? Current chat will be cleared.')) {
      await clearChat();
    }
  };
  
  return (
    <div className="flex flex-col h-screen bg-gray-50">
      <Header onNewChat={handleNewChat} />
      
      <div className="flex-1 flex flex-col overflow-hidden relative">
        {/* Floating API button */}
        <button
          onClick={() => setIsSidebarOpen(!isSidebarOpen)}
          className="fixed bottom-20 right-4 z-30 bg-primary-600 hover:bg-primary-700 text-white p-3 rounded-full shadow-lg transition-all duration-300 hover:scale-110 md:hidden"
          title="View APIs"
        >
          <Menu className="w-6 h-6" />
        </button>
        
        {/* Desktop API button */}
        <button
          onClick={() => setIsSidebarOpen(!isSidebarOpen)}
          className="hidden md:block fixed top-20 right-4 z-30 btn-secondary"
        >
          <Menu className="w-5 h-5" />
          <span>APIs</span>
        </button>
        
        <ChatMessages messages={messages} isLoading={isLoading} />
        <ChatInput onSend={handleSendMessage} isLoading={isLoading} />
      </div>
      
      <Sidebar isOpen={isSidebarOpen} onClose={() => setIsSidebarOpen(false)} />
    </div>
  );
}

export default App;
