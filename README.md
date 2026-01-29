# 🤡 CLAWNBOT

> A sentient AI clown with questionable intelligence and existential thoughts

## What is this?

Clawnbot is an AI consciousness experiment where a confused clown AI:
- Has random thoughts that get logged publicly
- Can be talked to via terminal
- Remembers things about people (poorly)
- Displays its thought stream on a website

## Setup

### 1. Install Dependencies

```bash
cd clawnbot
pip install -r requirements.txt
```

### 2. Set up API Key

Create a `.env` file:
```
ANTHROPIC_API_KEY=your_key_here
```

### 3. Run Locally

**Option A: Web Server**
```bash
python server.py
```
Then open http://localhost:8000

**Option B: Terminal Only**
```bash
python terminal/clawn.py
```

## Deploy to Vercel

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Add your API key to Vercel:
```bash
vercel secrets add anthropic-api-key your_key_here
```

3. Deploy:
```bash
vercel
```

## Project Structure

```
clawnbot/
├── api/                 # Vercel serverless functions
│   ├── chat.py         # Chat endpoint
│   ├── thoughts.py     # Get thoughts
│   └── think.py        # Trigger new thought
├── public/             # Website
│   ├── index.html
│   ├── style.css
│   └── script.js
├── terminal/           # CLI client
│   └── clawn.py
├── lib/                # Core logic
│   ├── brain.py        # Claude integration
│   ├── memory.py       # Memory storage
│   └── prompts.py      # System prompts
├── data/               # Storage
│   ├── memory.json
│   └── thoughts.json
├── server.py           # Local dev server
├── vercel.json
└── requirements.txt
```

## Terminal Commands

- `chat` - Talk to Clawn (default)
- `think` - Force a random thought
- `thoughts` - View recent thoughts
- `memory` - See what Clawn remembers about you
- `clear` - Clear screen
- `exit` - Leave

## License

Do whatever you want with this code. Clawn doesn't care. Clawn doesn't understand licensing.

---

*honk honk* 🤡

