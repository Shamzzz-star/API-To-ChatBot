import React, { useState } from 'react';
import { Send, Loader2 } from 'lucide-react';

const ChatInput = ({ onSend, isLoading }) => {
  const [input, setInput] = useState('');
  
  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim() && !isLoading) {
      onSend(input.trim());
      setInput('');
    }
  };
  
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };
  
  return (
    <form onSubmit={handleSubmit} className="border-t border-gray-200 bg-white p-4">
      <div className="flex gap-2 items-end max-w-4xl mx-auto">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask me anything... (e.g., 'What's the weather in Tokyo?')"
          className="input-field"
          rows="2"
          disabled={isLoading}
          maxLength={1000}
        />
        
        <button
          type="submit"
          disabled={!input.trim() || isLoading}
          className="btn-primary flex items-center gap-2 px-6 shrink-0"
        >
          {isLoading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              <span>Sending</span>
            </>
          ) : (
            <>
              <Send className="w-5 h-5" />
              <span>Send</span>
            </>
          )}
        </button>
      </div>
      
      <div className="text-xs text-gray-500 mt-2 text-center max-w-4xl mx-auto">
        Press Enter to send • Shift+Enter for new line • {input.length}/1000 characters
      </div>
    </form>
  );
};

export default ChatInput;
