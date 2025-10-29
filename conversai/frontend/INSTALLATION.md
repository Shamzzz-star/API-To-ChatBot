# ConversAI - Frontend Installation & Setup

Complete guide to setting up and running the React frontend for ConversAI.

## Prerequisites

Before starting, ensure you have:
- ✅ Node.js 18+ installed
- ✅ npm or yarn package manager
- ✅ Backend server configured and running on `http://localhost:8000`
- ✅ Git (optional, for cloning)

Check your Node.js version:
```powershell
node --version  # Should be 18.0.0 or higher
npm --version   # Should be 8.0.0 or higher
```

## Installation Steps

### Step 1: Navigate to Frontend Directory

```powershell
cd "d:\SEM 3\GENAI\API\conversai\frontend"
```

### Step 2: Install Dependencies

Install all required npm packages:

```powershell
npm install
```

This will install:
- **React 18.2**: UI framework
- **Vite 5.0**: Build tool and dev server  
- **Tailwind CSS 3.4**: Styling
- **Zustand 4.4**: State management
- **Axios 1.6**: HTTP client
- **React Markdown 9.0**: Markdown rendering
- **Lucide React**: Icons

**Expected output:**
```
added 250+ packages in 30s
```

### Step 3: Configure Environment

Copy the example environment file:

```powershell
copy .env.example .env
```

The `.env` file should contain:
```
VITE_API_URL=http://localhost:8000
```

> **Note:** If your backend runs on a different port, update `VITE_API_URL` accordingly.

### Step 4: Verify Installation

Check that all packages are installed:

```powershell
npm list --depth=0
```

You should see all dependencies listed without errors.

## Running the Development Server

### Start the Dev Server

```powershell
npm run dev
```

**Expected output:**
```
VITE v5.0.8  ready in 523 ms

➜  Local:   http://localhost:3000/
➜  Network: use --host to expose
➜  press h to show help
```

### Access the Application

Open your browser and navigate to:
```
http://localhost:3000
```

You should see the ConversAI chat interface with:
- ✅ Header with "ConversAI" branding
- ✅ Welcome message with example queries
- ✅ Chat input at the bottom
- ✅ "APIs" button in the top-right corner

## Testing the Application

### 1. Test Backend Connection

Before testing the frontend, ensure the backend is running:

```powershell
# In a separate terminal, navigate to backend
cd "d:\SEM 3\GENAI\API\conversai\backend"

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Start backend
python -m uvicorn app.main:app --reload
```

Backend should be running on `http://127.0.0.1:8000`

### 2. Send a Test Message

In the frontend (http://localhost:3000):

1. Type a message in the chat input:
   ```
   What's the weather in Paris?
   ```

2. Click "Send" or press Enter

3. You should see:
   - Your message appears immediately
   - Typing indicator (3 animated dots)
   - AI response with weather information
   - API metadata (which API was used, cached status)

### 3. Test API Sidebar

1. Click the "APIs" button in the top-right
2. Sidebar should slide in from the right
3. You should see all 8 registered APIs:
   - OpenWeatherMap (Weather)
   - CoinGecko (Crypto)
   - NewsAPI (News)
   - Free Dictionary API
   - ExchangeRate-API
   - API Ninjas (Facts)
   - Wikipedia
   - GitHub

### 4. Test New Chat

1. Click "New Chat" in the header
2. Confirm the prompt
3. Chat should clear and reset

## Building for Production

### Create Production Build

```powershell
npm run build
```

This creates an optimized build in the `dist/` folder:
- ✅ Minified JavaScript
- ✅ Optimized CSS
- ✅ Tree-shaken dependencies
- ✅ Code-split chunks

**Expected output:**
```
vite v5.0.8 building for production...
✓ 45 modules transformed.
dist/index.html                  0.46 kB
dist/assets/index-abc123.css     8.92 kB │ gzip: 2.34 kB
dist/assets/index-def456.js    142.57 kB │ gzip: 45.82 kB
✓ built in 2.35s
```

### Preview Production Build

```powershell
npm run preview
```

Access at `http://localhost:4173`

### Deploy Production Build

The `dist/` folder contains all files needed for deployment. You can:

1. **Static Hosting** (Netlify, Vercel, GitHub Pages):
   - Upload the `dist/` folder

2. **Custom Server** (Nginx, Apache):
   - Copy `dist/` contents to web root
   - Configure SPA routing (all routes → index.html)

3. **Docker** (see main README for Docker setup)

## Troubleshooting

### Issue: Port 3000 Already in Use

**Error:**
```
Port 3000 is in use, trying another one...
```

**Solution 1 - Use Different Port:**
```powershell
npm run dev -- --port 3001
```

**Solution 2 - Kill Process on Port 3000:**
```powershell
# Find process using port 3000
netstat -ano | findstr :3000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

### Issue: CORS Error

**Error in Browser Console:**
```
Access to XMLHttpRequest at 'http://localhost:8000/api/chat/message' 
from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Solution:**

Check backend CORS configuration in `backend/app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Restart the backend after changes.

### Issue: Module Not Found

**Error:**
```
Cannot find module 'zustand' or its corresponding type declarations
```

**Solution:**
```powershell
# Delete node_modules and reinstall
Remove-Item -Recurse -Force node_modules
Remove-Item package-lock.json
npm install
```

### Issue: Vite Build Fails

**Error:**
```
Transform failed with 1 error
```

**Solution:**
```powershell
# Clear Vite cache
Remove-Item -Recurse -Force node_modules/.vite

# Rebuild
npm run dev
```

### Issue: Backend Not Responding

**Symptoms:**
- Messages not sending
- Loading indicator stays forever
- Console shows network errors

**Solution:**

1. Check backend is running:
   ```powershell
   curl http://localhost:8000/health
   ```

2. Check backend logs for errors

3. Verify `.env` has correct `VITE_API_URL`

4. Check browser Network tab for failed requests

### Issue: Blank Page

**Symptoms:**
- White screen
- No errors in console
- `index.html` loads but nothing renders

**Solution:**

1. Check browser console for JavaScript errors

2. Verify `main.jsx` is being loaded:
   ```powershell
   # Check if build is corrupted
   npm run build
   npm run preview
   ```

3. Clear browser cache (Ctrl+Shift+Delete)

4. Try incognito mode

## Development Tips

### Hot Module Replacement (HMR)

Vite provides instant updates without full page reload:
- ✅ Save a component → see changes immediately
- ✅ CSS changes apply instantly
- ✅ State is preserved during updates

### Browser DevTools

Open DevTools (F12) to:
- **Console**: View logs and errors
- **Network**: Monitor API calls
- **React DevTools**: Inspect component state
- **Application**: Check localStorage/sessionStorage

### Recommended VS Code Extensions

Install for better development experience:
```
- ESLint
- Tailwind CSS IntelliSense
- ES7+ React/Redux/React-Native snippets
- Auto Rename Tag
- Prettier
```

### Keyboard Shortcuts

- `Ctrl+C`: Stop dev server
- `Ctrl+Shift+R`: Hard refresh browser (bypass cache)
- `F12`: Open browser DevTools
- `Ctrl+K`: Clear terminal

## Performance Optimization

### 1. Enable Production Mode

Always use production build for deployment:
```powershell
npm run build
```

### 2. Analyze Bundle Size

```powershell
npm run build -- --mode analyze
```

### 3. Lazy Load Components

For large components, use React.lazy():
```jsx
const Sidebar = React.lazy(() => import('./components/Sidebar'));
```

### 4. Enable Compression

On your server, enable gzip/brotli compression for:
- `.js` files
- `.css` files
- `.html` files

## Next Steps

1. ✅ Frontend is running on http://localhost:3000
2. ✅ Backend is running on http://localhost:8000
3. ✅ Test all chat features
4. ✅ Test API sidebar
5. ✅ Try different queries (weather, crypto, news, etc.)
6. 📝 Customize theme in `tailwind.config.js`
7. 📝 Add custom APIs via API Management
8. 📝 Deploy to production

## Support

If you encounter issues:

1. **Check Logs**: Browser console + terminal output
2. **Verify Versions**: Node.js 18+, npm 8+
3. **Check Backend**: Must be running on port 8000
4. **Clear Cache**: `npm cache clean --force`
5. **Reinstall**: Delete `node_modules`, run `npm install`

## Additional Resources

- [React Documentation](https://react.dev)
- [Vite Documentation](https://vitejs.dev)
- [Tailwind CSS Docs](https://tailwindcss.com)
- [Zustand Guide](https://github.com/pmndrs/zustand)
- [Axios Documentation](https://axios-http.com)

---

**Frontend Ready!** 🎉 You can now interact with ConversAI through the beautiful React interface.
