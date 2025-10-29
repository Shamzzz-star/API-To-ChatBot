import React, { useEffect, useRef } from 'react';
import MessageBubble from './MessageBubble';
import TypingIndicator from './TypingIndicator';
import { Sparkles } from 'lucide-react';

const ChatMessages = ({ messages, isLoading }) => {
  const messagesEndRef = useRef(null);
  
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };
  
  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);
  
  if (messages.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="text-center max-w-2xl">
          <div className="mb-6">
            <Sparkles className="w-16 h-16 text-primary-500 mx-auto mb-4" />
            <h2 className="text-3xl font-bold text-gray-800 mb-2">
              Welcome to ConversAI
            </h2>
            <p className="text-gray-600 text-lg">
              Your intelligent assistant for interacting with multiple APIs using natural language
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-8">
            <ExampleQuery text="What's the weather in Paris?" />
            <ExampleQuery text="Show me Bitcoin's price" />
            <ExampleQuery text="Latest news about AI" />
            <ExampleQuery text="Define quantum computing" />
          </div>
          
          <div className="mt-8 p-4 bg-white rounded-lg shadow-sm">
            <p className="text-sm text-gray-600">
              <strong className="text-primary-600">Try asking:</strong> Weather, Cryptocurrency prices, News, Dictionary definitions, Currency exchange, Random facts, and more!
            </p>
          </div>
        </div>
      </div>
    );
  }
  
  return (
    <div className="flex-1 overflow-y-auto p-4 custom-scrollbar">
      <div className="max-w-4xl mx-auto">
        {messages.map((message) => (
          <MessageBubble key={message.message_id} message={message} />
        ))}
        
        {isLoading && <TypingIndicator />}
        
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
};

const ExampleQuery = ({ text }) => {
  return (
    <div className="p-3 bg-white rounded-lg shadow-sm border border-gray-200 hover:border-primary-300 transition-colors cursor-pointer">
      <p className="text-sm text-gray-700">{text}</p>
    </div>
  );
};

export default ChatMessages;
