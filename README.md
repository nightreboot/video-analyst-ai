<<<<<<< HEAD
# video-analyst-ai
=======
# 🎬 VidMind — YouTube Video Analyser

> **AI-powered intelligence layer for any YouTube video or audio file.**  
> Transcribe → Summarise → Quiz → Fact-Check → Ask anything.  
> Available as a **Streamlit web app** and a **CLI tool**.

---

## 📸 UI Previews

### Streamlit App (`app.py`)

```
┌─────────────────────────────────────────────────────────────────────────┐
│ SIDEBAR                  │  MAIN AREA                                    │
│ ─────────────────────    │  ──────────────────────────────────────────   │
│ 🎬 VidMind               │  Analyse any YouTube video                    │
│                          │                                               │
│ ✅ Video processed       │  [ https://youtube.com/...  ] [ ⚡ Analyse ]  │
│                          │  [ ↺ Reset Session ] [ 🗑 Delete All ]        │
│ 🛠️ Analysis Tools        │  ─────────────────────────────────────────    │
│                          │                                               │
│ [📝 Summary         ]    │  ┌─────────────────────┐  ┌───────────────┐  │
│ [🧠 Quiz            ]    │  │  📺 YouTube Embed   │  │ 📊 Stats      │  │
│ [🔍 Fact Check      ]    │  │                     │  │  Results: 3   │  │
│ [✅ Action Items    ]    │  │  (live video here)  │  │  Q&A: 2       │  │
│ [🔑 Key Decisions   ]    │  │                     │  │  Quiz: 4      │  │
│ [❓ Open Questions  ]    │  └─────────────────────┘  └───────────────┘  │
│                          │                                               │
│ [↺ Reset] [🗑 Delete]    │  ┌── Tabs ─────────────────────────────────┐ │
│                          │  │ 📝Summary│🧠Quiz│🔍Fact│✅Actions│💬Ask │ │
│ Stack:                   │  ├─────────────────────────────────────────┤ │
│ Whisper · Mistral AI     │  │  • Bullet point result 1                │ │
│ LangChain · ChromaDB     │  │  • Bullet point result 2                │ │
│ NVIDIA NIM · Tavily      │  │  [📥 Download]  [🗑 Remove]             │ │
│                          │  └─────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

### Standalone Web UI (`index.html`)

```
┌────────────────────────────────────────────────────────────────┐
│  🎬 VidMind                          [↺ Reset]  [🗑 Clear All] │
├────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────┐     │
│  │  https://www.youtube.com/watch?v=...    [ ⚡ Analyse ]│     │
│  └──────────────────────────────────────────────────────┘     │
│  ┌──────────────────────┐  ┌─────────────────────────────┐   │
│  │  📺 YouTube Embed    │  │  [📝] [🧠] [🔍] [✅] [🔑]  │   │
│  └──────────────────────┘  └─────────────────────────────┘   │
│  📊 Results          [📋 Copy All] [🗑 Delete All]            │
│  ┌──────────────────────────────────────────────────────┐     │
│  │  📝 Summary                              [📋] [🗑]   │     │
│  └──────────────────────────────────────────────────────┘     │
└────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Features

| Feature | Description | Module |
|---------|-------------|--------|
| 📝 **Summary** | Bullet-point summary using chunked transcript | `summarized.py` |
| 🧠 **Quiz** | Auto-generated MCQ questions with answers | `Quize.py` |
| 🔍 **Fact Check** | Web-verified misinformation detection | `fake_cheking.py` |
| ✅ **Action Items** | Tasks, owners, deadlines from discussion | `prompting.py` |
| 🔑 **Key Decisions** | Important decisions made in the video | `prompting.py` |
| ❓ **Open Questions** | Unresolved topics needing follow-up | `prompting.py` |
| 💬 **Ask Questions** | RAG-powered Q&A over the video content | `vector_db.py` |
| 🎙️ **Transcription** | Whisper-based audio transcription | `transcribe.py` |

---

## 🏗️ Project Structure

```
vidmind/
│
├── main.py                      # 🎯 CLI entry point & pipeline orchestrator
├── app.py                       # 🌐 Streamlit web application
│
├── core/
│   ├── transcribe.py            # 🎙️ Whisper audio transcription
│   ├── summarized.py            # 📝 LangChain + Mistral summarisation
│   ├── prompting.py             # ✅ Action items, decisions, questions
│   ├── Quize.py                 # 🧠 MCQ quiz generation
│   ├── fake_cheking.py          # 🔍 Tavily-powered fact checking
│   └── vector_db.py             # 💾 ChromaDB + NVIDIA embeddings
│
├── utils/
│   └── you_tube_audio_processor.py  # 📥 yt-dlp download + audio chunking
│
├── index.html                   # 🖥️ Standalone HTML/JS web UI (no server needed)
├── README.md                    # 📖 Documentation
├── .env                         # 🔑 API keys (not committed)
└── requirements.txt             # 📦 Dependencies
```

---

## ⚙️ Pipeline Architecture

```
YouTube URL / Local File
        │
        ▼
┌───────────────────┐
│  you_tube_audio   │  yt-dlp → WAV → mono 16kHz → 5-min chunks
│  _processor.py    │
└────────┬──────────┘
         │ audio chunks[]
         ▼
┌───────────────────┐
│  transcribe.py    │  Whisper base model (en / hi)
└────────┬──────────┘
         │ transcript string
         ▼
┌─────────────────────────────────────────┐
│             Parallel Analysis            │
│                                         │
│  summarized.py   → Title + Summary      │
│  prompting.py    → Actions/Decisions/Q  │
│  Quize.py        → MCQ Quiz (JSON)      │
│  fake_cheking.py → Fact-check + Tavily  │
│  vector_db.py    → ChromaDB + NVIDIA    │
└─────────────────────────────────────────┘
         │
         ▼
    dict result{}
         │
         ▼
   UI / CLI output
```

---

## 🖥️ UI Features & Buttons

### 🔘 Analysis Buttons
Each button triggers a specific AI analysis on the processed video:

| Button | What it does |
|--------|-------------|
| **📝 Summary** | Generates a professional bullet-point summary using Mistral AI |
| **🧠 Quiz** | Creates MCQ questions with A/B/C/D options; click to check answers |
| **🔍 Fact Check** | Runs each transcript chunk through Tavily web search + Mistral to detect misinformation |
| **✅ Action Items** | Extracts tasks with owner and deadline |
| **🔑 Key Decisions** | Lists decisions made during the video/meeting |
| **❓ Open Questions** | Surfaces unresolved topics for follow-up |

### 🔄 Control Buttons

| Button | Location | Behaviour |
|--------|----------|-----------|
| **↺ Reset Session** | Nav bar + sidebar + URL box | Clears URL, video player, all results, resets state |
| **🗑 Clear All** / **Delete All** | Nav bar + results header + sidebar | Removes all result cards from the page |
| **📋 Copy All** | Results header | Copies all result text to clipboard |
| **📋** (per card) | Each result card | Copies that result's text |
| **🗑** (per card) | Each result card | Deletes only that result card |

### 💬 Ask About the Video
Type any question into the textarea and click **Ask**. The system uses vector-store retrieval (ChromaDB + NVIDIA embeddings) to return the most relevant passages from the transcript.

---

## 🔧 Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourname/vidmind.git
cd vidmind
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

**`requirements.txt`:**

```
# UI
streamlit>=1.35.0

# Audio processing
openai-whisper
yt-dlp
pydub
ffmpeg-python

# LangChain stack
langchain
langchain-mistralai
langchain-chroma
langchain-nvidia-ai-endpoints
langchain-text-splitters
langchain-core
langchain-classic

# Fact-checking
tavily-python

# Data / infra
pydantic
chromadb
python-dotenv
```

### 4. Configure API keys

Create a `.env` file in the project root:

```env
MISTRAL_API_KEY=your_mistral_api_key_here
NVIDIA_API_KEY=your_nvidia_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

| Variable | Where to get it |
|----------|----------------|
| `MISTRAL_API_KEY` | [console.mistral.ai](https://console.mistral.ai) |
| `NVIDIA_API_KEY` | [build.nvidia.com](https://build.nvidia.com) |
| `TAVILY_API_KEY` | [tavily.com](https://tavily.com) |

### 5. Install FFmpeg (required for audio)

```bash
# Ubuntu / Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows — download from https://ffmpeg.org/download.html
```

---

## ▶️ Running the CLI

```bash
python main.py
```

```
Enter the URL or local path of the video/audio: https://www.youtube.com/watch?v=TLKxdTmk-zc

⏳ Processing...

==================================================
YouTube / Video Analyser
==================================================
1 — Title & Summary
2 — Action Items, Key Decisions & Open Questions
3 — Quiz
4 — Fake / Misinformation Check
5 — Ask Questions about the Video
Type 'exit' to quit
==================================================
Enter your choice (1-5 or exit):
```

---

## 🌐 Running the Streamlit App

```bash
streamlit run app.py
```

Then open **http://localhost:8501** in your browser.

### Streamlit UI — Features & Controls

| Element | Location | Behaviour |
|---------|----------|-----------|
| **⚡ Analyse** | Top URL row | Runs full pipeline on the entered URL |
| **↺ Reset Session** | Sidebar + top bar | Clears all state, results, video, URL |
| **🗑 Delete All** | Sidebar + top bar | Removes all generated results only |
| **📝 Summary** | Sidebar + Quick Launch | Generates bullet-point summary tab |
| **🧠 Quiz** | Sidebar + Quick Launch | Opens interactive MCQ quiz tab |
| **🔍 Fact Check** | Sidebar + Quick Launch | Shows verdict/confidence per chunk |
| **✅ Action Items** | Sidebar + Quick Launch | Extracts tasks with owners/deadlines |
| **🔑 Key Decisions** | Sidebar + Quick Launch | Lists decisions from the video |
| **❓ Open Questions** | Sidebar + Quick Launch | Shows unresolved follow-up topics |
| **💬 Ask** | Ask tab | Free-text Q&A with conversation history |
| **📥 Download** | Each result tab | Downloads result as `.txt` file |
| **🗑 Remove** (per tab) | Each result tab | Deletes only that specific result |

### Streamlit Tabs

| Tab | What you see |
|-----|-------------|
| **📝 Summary** | Bullet-point summary with download button |
| **🧠 Quiz** | Interactive MCQ — select answer → submit → see correct/wrong |
| **🔍 Fact Check** | Card per chunk: verdict badge, confidence %, reason |
| **✅ Actions** | Numbered action items with owner and deadline |
| **🔑 Decisions** | Key decisions as a numbered list |
| **❓ Questions** | Open questions for follow-up |
| **💬 Ask** | Multi-turn conversation history with the video content |

---

## 🖥️ Running the Standalone HTML UI

Simply open `index.html` in any modern browser — no server or Python required.

```bash
# Option A: Direct open
open index.html        # macOS
start index.html       # Windows

# Option B: Local server
python -m http.server 8080
# → visit http://localhost:8080
```

> **Note:** `index.html` is a standalone frontend demo. To wire it to the real Python pipeline, wrap `main.py`'s `pipeline()` in a FastAPI server and point the fetch calls at it.

---

## 🧩 Module Details

### `you_tube_audio_processor.py`
Downloads audio from YouTube using `yt-dlp`, converts to mono 16kHz WAV with `pydub`, and splits into 5-minute chunks for Whisper processing.

```python
all_audio_process("https://youtube.com/watch?v=...")
# → ["downloads/video_chunk_0.wav", "downloads/video_chunk_1.wav", ...]
```

### `transcribe.py`
Runs Whisper (`base` model) on each audio chunk. Supports English (`en`) and Hindi (`hi`).

```python
transcribe_audio(audio_chunks)
# → "Full transcript as a single string..."
```

### `summarized.py`
Splits transcript into 3000-token chunks, summarises each with Mistral, then combines into a final professional summary. Also generates a short meeting title.

### `prompting.py`
Three LangChain chains for extracting:
- Action items (task, owner, deadline)
- Key decisions
- Open/unresolved questions

### `Quize.py`
Returns structured JSON quiz:
```json
{
  "quiz": [
    {
      "question": "What model is used?",
      "options": ["A", "B", "C", "D"],
      "correct_answer": "B"
    }
  ]
}
```

### `fake_cheking.py`
For each 350-token chunk:
1. Searches web via Tavily
2. Feeds chunk + search results to Mistral
3. Returns `FactCheckResult(verdict, confidence, reason)`

### `vector_db.py`
Stores transcript in ChromaDB with NVIDIA `nv-embed-v1` embeddings. Exposes an MMR retriever for semantic question answering.

---

## 📋 Example Output

### Summary
```
• Framework processes YouTube videos end-to-end using open-source models.
• Whisper provides high-accuracy transcription for English and Hindi content.
• Mistral AI handles all NLP tasks: summarisation, QA generation, fact checking.
• ChromaDB stores embeddings locally for persistent retrieval.
• Full pipeline runs in under 3 minutes for a 30-minute video.
```

### Fact Check
```
[Chunk 1]
Verdict    : True
Confidence : 94%
Reason     : Confirmed by official Whisper documentation and benchmarks.

[Chunk 2]
Verdict    : Partial
Confidence : 67%
Reason     : The accuracy figure cited was based on limited test data.
```

---

## 🛠️ Roadmap

- [x] CLI pipeline (`main.py`)
- [x] Streamlit web app (`app.py`)
- [x] Standalone HTML/JS UI (`index.html`)
- [ ] FastAPI backend to connect HTML UI ↔ Python pipeline
- [ ] Real-time progress streaming via WebSocket / SSE
- [ ] Export results as PDF / DOCX
- [ ] Multi-language support beyond en/hi
- [ ] Playlist / batch URL processing
- [ ] User auth + saved history

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss.

---

## 📜 License

MIT License — see `LICENSE` for details.

---

## 🙏 Acknowledgements

- [OpenAI Whisper](https://github.com/openai/whisper) — speech-to-text
- [Mistral AI](https://mistral.ai) — LLM backbone
- [LangChain](https://langchain.com) — pipeline orchestration
- [ChromaDB](https://www.trychroma.com) — vector store
- [Tavily](https://tavily.com) — real-time web search for fact-checking
- [NVIDIA NIM](https://build.nvidia.com) — embeddings
- [Streamlit](https://streamlit.io) — web application framework

---

*Built with ❤️ using Python, Streamlit, LangChain, Whisper, and Mistral AI.*
>>>>>>> 940d91d (Initial commit)
