import React from 'react';
import ReactMarkdown from 'react-markdown';

const MessageBubble = ({ message }) => {
  const isUser = message.role === 'user';
  const metadata = message.message_metadata;
  
  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };
  
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4 animate-fadeIn`}>
      <div className={`flex flex-col ${isUser ? 'items-end' : 'items-start'} max-w-[80%]`}>
        <div className={isUser ? 'message-user' : 'message-assistant'}>
          <div className="markdown-content">
            <ReactMarkdown>{message.content}</ReactMarkdown>
          </div>
        </div>
        
        <div className="flex items-center gap-2 mt-1 text-xs text-gray-500">
          <span>{formatTime(message.created_at)}</span>
          
          {metadata?.api_used && (
            <>
              <span>•</span>
              <span className="text-primary-600 font-medium">
                {metadata.api_used}
              </span>
            </>
          )}
          
          {metadata?.cached && (
            <>
              <span>•</span>
              <span className="text-green-600 flex items-center gap-1">
                <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M3 12v3c0 1.657 3.134 3 7 3s7-1.343 7-3v-3c0 1.657-3.134 3-7 3s-7-1.343-7-3z" />
                  <path d="M3 7v3c0 1.657 3.134 3 7 3s7-1.343 7-3V7c0 1.657-3.134 3-7 3S3 8.657 3 7z" />
                  <path d="M17 5c0 1.657-3.134 3-7 3S3 6.657 3 5s3.134-3 7-3 7 1.343 7 3z" />
                </svg>
                Cached
              </span>
            </>
          )}
          
          {metadata?.intent?.confidence && (
            <>
              <span>•</span>
              <span title={`Intent: ${metadata.intent.intent}`}>
                {Math.round(metadata.intent.confidence * 100)}% confident
              </span>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default MessageBubble;
