import React from 'react';
import { Bot, RefreshCw, Github } from 'lucide-react';

const Header = ({ onNewChat }) => {
  return (
    <header className="bg-white border-b border-gray-200 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 py-3 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-gradient-to-br from-primary-500 to-primary-600 p-2 rounded-lg shadow-md">
              <Bot className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-primary-600 to-primary-700 bg-clip-text text-transparent">
                ConversAI
              </h1>
              <p className="text-xs text-gray-500">Natural Language API Interaction</p>
            </div>
          </div>
          
          <div className="flex items-center gap-3">
            <button
              onClick={onNewChat}
              className="btn-secondary flex items-center gap-2"
            >
              <RefreshCw className="w-4 h-4" />
              <span>New Chat</span>
            </button>
            
            <a
              href="https://github.com/Shamzzz-star/CONVERSAI-API"
              target="_blank"
              rel="noopener noreferrer"
              className="p-2 text-gray-600 hover:text-gray-900 transition-colors"
              title="View on GitHub"
            >
              <Github className="w-5 h-5" />
            </a>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
