# Cat Lounge - ChatKit Demo

A virtual pet caretaker demo built with OpenAI ChatKit SDK.

## Features
- Chat with an AI assistant to care for a virtual cat
- Manage energy, happiness, and cleanliness stats
- Demonstrates ChatKit client-side tool calls

## Setup on Replit

1. **Import this repo** into Replit
2. **Add your OpenAI API key** in Secrets:
   - Go to "Secrets" (lock icon)
   - Add `OPENAI_API_KEY` with your key
3. **Click Run** - it will build the frontend and start the server

## Local Development

```bash
# Backend
cd backend
uv sync
uv run uvicorn app.main:app --reload --port 8000

# Frontend (in another terminal)
cd frontend
npm install
npm run dev
```

## Credits
Based on [OpenAI ChatKit Advanced Samples](https://github.com/openai/openai-chatkit-advanced-samples)
