# ConversAI Frontend

React-based frontend for the ConversAI chatbot interface.

## Tech Stack

- **React 18.2**: UI framework
- **Vite 5.0**: Build tool and dev server
- **Tailwind CSS 3.4**: Utility-first CSS framework
- **Zustand**: Lightweight state management
- **Axios**: HTTP client
- **React Markdown**: Markdown rendering
- **Lucide React**: Icon library

## Prerequisites

- Node.js 18+ and npm/yarn
- Backend server running on `http://localhost:8000`

## Installation

1. Install dependencies:
```bash
npm install
```

2. Copy environment file:
```bash
cp .env.example .env
```

3. Configure the backend URL in `.env`:
```
VITE_API_URL=http://localhost:8000
```

## Development

Start the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:3000`

## Building for Production

Build the production bundle:
```bash
npm run build
```

Preview the production build:
```bash
npm run preview
```

## Features

### Main Chat Interface
- Real-time message exchange with the AI
- Markdown rendering for formatted responses
- Typing indicators
- Message metadata (API used, intent confidence, caching status)
- Auto-scrolling to latest message

### API Management Sidebar
- View all registered APIs
- Filter by category (Weather, Crypto, News, etc.)
- Check API status (Active/Inactive)
- Browse intent keywords for each API

### User Experience
- Responsive design (mobile + desktop)
- Smooth animations and transitions
- Loading states
- Error handling with retry
- Keyboard shortcuts (Enter to send, Shift+Enter for new line)
- Character counter

## Project Structure

```
frontend/
├── public/              # Static assets
├── src/
│   ├── api/            # API client and endpoints
│   │   └── client.js   # Axios instance + API methods
│   ├── components/     # React components
│   │   ├── Header.jsx
│   │   ├── Sidebar.jsx
│   │   ├── ChatMessages.jsx
│   │   ├── ChatInput.jsx
│   │   ├── MessageBubble.jsx
│   │   └── TypingIndicator.jsx
│   ├── store/          # State management
│   │   └── chatStore.js
│   ├── App.jsx         # Main app component
│   ├── main.jsx        # Entry point
│   └── index.css       # Global styles
├── index.html
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
└── package.json
```

## State Management

Using Zustand for global state:

### Chat Store (`chatStore.js`)
- `messages`: Array of conversation messages
- `sessionId`: Current chat session ID
- `isLoading`: Loading state for API calls
- `error`: Error messages

Actions:
- `sendMessage(message)`: Send user message and get response
- `loadHistory()`: Load conversation history
- `createNewSession()`: Start new chat session
- `clearChat()`: Clear current conversation

## API Integration

### Chat API (`/api/chat`)
- `POST /message`: Send message and get response
- `GET /history/:sessionId`: Get conversation history
- `POST /session/new`: Create new session
- `DELETE /session/:sessionId`: Clear session

### API Management (`/api/apis`)
- `GET /list`: List all registered APIs
- `GET /:apiId`: Get specific API details
- `POST /register`: Register new API
- `POST /:apiId/test`: Test API endpoint

## Customization

### Theme Colors
Edit `tailwind.config.js` to customize the color palette:
```js
theme: {
  extend: {
    colors: {
      primary: {
        // Your custom colors
      }
    }
  }
}
```

### API Proxy
Vite proxies `/api` requests to the backend. Configure in `vite.config.js`:
```js
server: {
  proxy: {
    '/api': 'http://localhost:8000'
  }
}
```

## Troubleshooting

### CORS Errors
Ensure backend has CORS enabled for `http://localhost:3000`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### API Connection Issues
1. Check backend is running on port 8000
2. Verify `VITE_API_URL` in `.env`
3. Check browser console for errors
4. Test backend health: `curl http://localhost:8000/health`

### Build Errors
Clear node_modules and reinstall:
```bash
rm -rf node_modules package-lock.json
npm install
```

## Performance Tips

1. **Code Splitting**: Vite automatically splits code
2. **Lazy Loading**: Components load on demand
3. **Caching**: Backend responses are cached
4. **Optimized Build**: Production build is minified and optimized

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## License

MIT License - See LICENSE file for details
