import streamlit as st
import sys
import os
import json
import re
import time

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VideoMind AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;600;700&display=swap');

/* ── Root & Body ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Main background ── */
.stApp {
    background: #0d0f14;
    color: #e8eaf0;
}

/* ── Hide Streamlit branding ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Top Logo Bar ── */
.logo-bar {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 0 0 24px 0;
}
.logo-text {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 26px;
    font-weight: 700;
    background: linear-gradient(135deg, #a78bfa, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.5px;
}
.logo-badge {
    font-size: 11px;
    font-weight: 600;
    color: #a78bfa;
    background: rgba(167,139,250,0.12);
    border: 1px solid rgba(167,139,250,0.3);
    border-radius: 20px;
    padding: 2px 10px;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* ── URL Input Card ── */
.url-card {
    background: #13151d;
    border: 1px solid #1e2130;
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 24px;
}

/* ── Feature Tabs styling ── */
.stTabs [data-baseweb="tab-list"] {
    background: #13151d;
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
    border: 1px solid #1e2130;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 9px;
    color: #8891a8;
    font-weight: 500;
    font-size: 14px;
    padding: 8px 18px;
    border: none;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #7c3aed, #2563eb) !important;
    color: white !important;
    font-weight: 600;
}

/* ── Result cards ── */
.result-card {
    background: #13151d;
    border: 1px solid #1e2130;
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 16px;
    line-height: 1.7;
}
.result-card h4 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 13px;
    font-weight: 600;
    color: #a78bfa;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 0 0 12px 0;
}

/* ── Title banner ── */
.title-banner {
    background: linear-gradient(135deg, rgba(124,58,237,0.15), rgba(37,99,235,0.15));
    border: 1px solid rgba(124,58,237,0.25);
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 20px;
}
.video-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #e8eaf0;
    margin: 0;
}

/* ── Fact check chips ── */
.verdict-true {
    display: inline-block;
    background: rgba(34,197,94,0.15);
    color: #4ade80;
    border: 1px solid rgba(74,222,128,0.3);
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 12px;
    font-weight: 600;
}
.verdict-false {
    display: inline-block;
    background: rgba(239,68,68,0.15);
    color: #f87171;
    border: 1px solid rgba(248,113,113,0.3);
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 12px;
    font-weight: 600;
}
.verdict-mixed {
    display: inline-block;
    background: rgba(234,179,8,0.15);
    color: #facc15;
    border: 1px solid rgba(250,204,21,0.3);
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 12px;
    font-weight: 600;
}

/* ── Confidence bar ── */
.conf-bar-wrap { margin: 8px 0; }
.conf-bar-bg {
    background: #1e2130;
    border-radius: 999px;
    height: 6px;
    overflow: hidden;
    width: 100%;
}
.conf-bar-fill {
    height: 6px;
    border-radius: 999px;
    background: linear-gradient(90deg, #7c3aed, #60a5fa);
}

/* ── Quiz question card ── */
.quiz-card {
    background: #13151d;
    border: 1px solid #1e2130;
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 16px;
}
.quiz-card .q-num {
    font-size: 11px;
    font-weight: 700;
    color: #60a5fa;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 6px;
}
.quiz-card .q-text {
    font-size: 16px;
    font-weight: 600;
    color: #e8eaf0;
    margin-bottom: 14px;
    line-height: 1.5;
}

/* ── Chat bubbles ── */
.chat-user {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 14px;
}
.chat-user .bubble {
    background: linear-gradient(135deg, #7c3aed, #2563eb);
    color: white;
    border-radius: 18px 18px 4px 18px;
    padding: 12px 18px;
    max-width: 75%;
    font-size: 15px;
    line-height: 1.6;
}
.chat-ai {
    display: flex;
    justify-content: flex-start;
    margin-bottom: 14px;
}
.chat-ai .bubble {
    background: #13151d;
    border: 1px solid #1e2130;
    color: #e8eaf0;
    border-radius: 18px 18px 18px 4px;
    padding: 12px 18px;
    max-width: 75%;
    font-size: 15px;
    line-height: 1.6;
}
.avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    flex-shrink: 0;
    margin: 0 10px;
}
.avatar-ai {
    background: linear-gradient(135deg, #7c3aed, #2563eb);
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #0d0f14 !important;
    border-right: 1px solid #1e2130;
}
section[data-testid="stSidebar"] * {
    color: #e8eaf0;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #2563eb);
    color: white !important;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    font-size: 14px;
    padding: 10px 24px;
    transition: opacity 0.2s;
}
.stButton > button:hover {
    opacity: 0.88;
    border: none;
}

/* ── Text input ── */
.stTextInput > div > div > input,
.stTextArea textarea {
    background: #1a1d28 !important;
    border: 1px solid #2a2f45 !important;
    border-radius: 10px !important;
    color: #e8eaf0 !important;
    font-size: 15px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea textarea:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 2px rgba(124,58,237,0.2) !important;
}

/* ── Progress ── */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #7c3aed, #60a5fa) !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: #13151d !important;
    border: 1px solid #1e2130 !important;
    border-radius: 10px !important;
    color: #e8eaf0 !important;
}

/* ── Status pills ── */
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 12px;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 20px;
    background: rgba(96,165,250,0.12);
    color: #60a5fa;
    border: 1px solid rgba(96,165,250,0.25);
}

/* ── Divider ── */
hr { border-color: #1e2130 !important; }

/* ── Step indicators ── */
.step-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 0;
    border-bottom: 1px solid #1e2130;
}
.step-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    flex-shrink: 0;
}
.step-done { background: #4ade80; }
.step-active { background: #a78bfa; animation: pulse 1s infinite; }
.step-pending { background: #2a2f45; }
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}
</style>
""", unsafe_allow_html=True)


# ── Session State Init ─────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "processed": False,
        "processing": False,
        "pipeline_result": None,
        "current_url": "",
        "chat_history": [],
        "quiz_answers": {},
        "quiz_submitted": False,
        "error": None,
        "steps_done": [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ── Helpers ────────────────────────────────────────────────────────────────────
def extract_youtube_id(url: str):
    patterns = [
        r"(?:v=|youtu\.be/|embed/|shorts/)([A-Za-z0-9_-]{11})",
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    return None


def render_verdict_chip(verdict: str):
    v = verdict.lower()
    if any(w in v for w in ["true", "accurate", "correct", "real", "legit"]):
        return f'<span class="verdict-true">✓ {verdict}</span>'
    elif any(w in v for w in ["false", "fake", "mislead", "wrong", "incorrect"]):
        return f'<span class="verdict-false">✗ {verdict}</span>'
    else:
        return f'<span class="verdict-mixed">~ {verdict}</span>'


def parse_quiz_json(raw: str):
    questions = []
    blocks = raw.split("```")
    for block in blocks:
        block = block.strip().lstrip("json").strip()
        if not block.startswith("{"):
            continue
        try:
            data = json.loads(block)
            if "quiz" in data:
                questions.extend(data["quiz"])
        except Exception:
            pass
    # fallback: try full raw
    if not questions:
        try:
            clean = re.sub(r"```json|```", "", raw).strip()
            data = json.loads(clean)
            if "quiz" in data:
                questions = data["quiz"]
        except Exception:
            pass
    return questions


def run_pipeline(url: str):
    """Import and run the pipeline – wraps all errors."""
    sys.path.insert(0, "/app")  # adjust if your project root differs
    try:
        from utils.you_tube_audio_processor import all_audio_process
        from core.transcribe import transcribe_audio
        from core.summarized import summarize_text, title_generator
        from core.prompting import action_items, key_dicision, questions
        from core.Quize import Quize
        from core.fake_cheking import fake_detection
        from core.vector_db import vector_stores, load_db, retrivers

        steps = [
            ("🎵 Downloading & processing audio…", None),
            ("📝 Transcribing audio…", None),
            ("🏷️  Generating title…", None),
            ("📋 Summarizing…", None),
            ("✅ Extracting action items…", None),
            ("🔑 Extracting key decisions…", None),
            ("❓ Extracting open questions…", None),
            ("🧠 Generating quiz…", None),
            ("🔍 Running fact-check…", None),
            ("💾 Building vector store…", None),
        ]
        progress_bar = st.progress(0)
        status_text = st.empty()

        def step(i, msg):
            st.session_state.steps_done.append(msg)
            progress_bar.progress((i + 1) / len(steps))
            status_text.markdown(f'<div class="status-pill">⚡ {msg}</div>', unsafe_allow_html=True)
            time.sleep(0.1)

        step(0, steps[0][0])
        source = all_audio_process(url)

        step(1, steps[1][0])
        transcribe = transcribe_audio(source)

        step(2, steps[2][0])
        title = title_generator(transcribe)

        step(3, steps[3][0])
        summary = summarize_text(transcribe)

        step(4, steps[4][0])
        action_item = action_items(transcribe)

        step(5, steps[5][0])
        key_decisions = key_dicision(transcribe)

        step(6, steps[6][0])
        question = questions(transcribe)

        step(7, steps[7][0])
        quize = Quize(transcribe)

        step(8, steps[8][0])
        fake_checking = fake_detection(transcribe)

        step(9, steps[9][0])
        vector_stores(transcribe)
        vector_db = load_db()
        retriever = retrivers(vector_db)

        progress_bar.progress(1.0)
        status_text.empty()

        return {
            "title": title,
            "summary": summary,
            "action_item": action_item,
            "key_decision": key_decisions,
            "questions": question,
            "quize": quize,
            "fake_check": fake_checking,
            "retriever": retriever,
            "transcribe": transcribe,
        }, None

    except Exception as e:
        return None, str(e)


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="logo-bar">
        <span style="font-size:28px">🎬</span>
        <div>
            <div class="logo-text">VideoMind</div>
            <span class="logo-badge">AI</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔧 Features")

    features = [
        ("📝", "Transcription", "Whisper (local)"),
        ("📋", "Summarization", "Mistral AI"),
        ("✅", "Action Items", "Mistral AI"),
        ("🔑", "Key Decisions", "Mistral AI"),
        ("❓", "Open Questions", "Mistral AI"),
        ("🧠", "Quiz Generator", "Mistral AI"),
        ("🔍", "Fact Checker", "Tavily + Mistral"),
        ("💬", "Video Chat", "RAG + NVIDIA"),
    ]
    for icon, name, model in features:
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;align-items:center;
                    padding:8px 0;border-bottom:1px solid #1e2130;">
            <span style="font-size:14px;color:#e8eaf0;">{icon} {name}</span>
            <span style="font-size:11px;color:#60a5fa;background:rgba(96,165,250,0.1);
                         padding:2px 8px;border-radius:12px;">{model}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    if st.session_state.processed:
        st.markdown("### ⚙️ Actions")
        if st.button("🔄 Analyse New Video", use_container_width=True):
            for k in ["processed", "pipeline_result", "current_url",
                      "chat_history", "quiz_answers", "quiz_submitted", "error", "steps_done"]:
                st.session_state[k] = [] if k in ("chat_history", "steps_done", "quiz_answers") else False if k != "current_url" and k != "pipeline_result" and k != "error" else None
            st.session_state["current_url"] = ""
            st.session_state["processing"] = False
            st.rerun()

        # Transcript download
        if st.session_state.pipeline_result:
            transcript = st.session_state.pipeline_result.get("transcribe", "")
            if transcript:
                st.download_button(
                    "⬇️ Download Transcript",
                    data=transcript,
                    file_name="transcript.txt",
                    mime="text/plain",
                    use_container_width=True,
                )


# ── Main Area ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="logo-bar" style="padding-top:8px;">
    <span style="font-size:32px">🎬</span>
    <div>
        <span class="logo-text" style="font-size:30px;">VideoMind AI</span>
        &nbsp;&nbsp;<span class="logo-badge">Powered by Mistral · Whisper · NVIDIA</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── URL Input ──────────────────────────────────────────────────────────────────
if not st.session_state.processed and not st.session_state.processing:
    st.markdown('<div class="url-card">', unsafe_allow_html=True)
    st.markdown("##### 🔗 Enter a YouTube URL or local file path")
    col1, col2 = st.columns([5, 1])
    with col1:
        url_input = st.text_input(
            "url_input",
            placeholder="https://youtube.com/watch?v=... or /path/to/video.mp4",
            label_visibility="collapsed",
        )
    with col2:
        analyse_btn = st.button("Analyse ▶", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Video preview
    if url_input:
        vid_id = extract_youtube_id(url_input)
        if vid_id:
            st.markdown("##### 📺 Video Preview")
            st.video(f"https://www.youtube.com/watch?v={vid_id}")

    if analyse_btn and url_input:
        st.session_state.current_url = url_input
        st.session_state.processing = True
        st.rerun()


# ── Processing ─────────────────────────────────────────────────────────────────
if st.session_state.processing and not st.session_state.processed:
    url = st.session_state.current_url
    vid_id = extract_youtube_id(url)

    col_vid, col_prog = st.columns([1, 1])
    with col_vid:
        if vid_id:
            st.markdown("##### 📺 Processing")
            st.video(f"https://www.youtube.com/watch?v={vid_id}")
    with col_prog:
        st.markdown("##### ⚙️ Pipeline Status")
        result, err = run_pipeline(url)

    if err:
        st.session_state.error = err
        st.session_state.processing = False
        st.error(f"❌ Pipeline failed: {err}")
        st.stop()
    else:
        st.session_state.pipeline_result = result
        st.session_state.processed = True
        st.session_state.processing = False
        st.rerun()


# ── Results Dashboard ──────────────────────────────────────────────────────────
if st.session_state.processed and st.session_state.pipeline_result:
    res = st.session_state.pipeline_result
    url = st.session_state.current_url
    vid_id = extract_youtube_id(url)

    # Title banner
    st.markdown(f"""
    <div class="title-banner">
        <div style="font-size:12px;color:#a78bfa;font-weight:600;
                    letter-spacing:1px;text-transform:uppercase;margin-bottom:6px;">
            📌 Video Title
        </div>
        <div class="video-title">{res.get("title", "Untitled")}</div>
    </div>
    """, unsafe_allow_html=True)

    # Video + quick stats
    col_v, col_s = st.columns([3, 2])
    with col_v:
        if vid_id:
            st.video(f"https://www.youtube.com/watch?v={vid_id}")
        elif url and not url.startswith("http"):
            st.video(url)
    with col_s:
        st.markdown("##### 📊 Analysis Overview")
        transcript = res.get("transcribe", "")
        word_count = len(transcript.split()) if transcript else 0
        fact_results = res.get("fake_check") or []
        quiz_qs = parse_quiz_json(res.get("quize", ""))

        m1, m2, m3 = st.columns(3)
        m1.metric("Words", f"{word_count:,}")
        m2.metric("Quiz Qs", len(quiz_qs))
        m3.metric("Fact Checks", len(fact_results))

        st.markdown("---")
        st.markdown("**✅ Analysis complete!** All features ready.")
        st.markdown(f"""
        <div style="font-size:13px;color:#8891a8;margin-top:8px;">
            Transcription · Summary · Action Items · Key Decisions ·
            Open Questions · Quiz · Fact-Check · Video Chat — all ready below.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Feature Tabs ──────────────────────────────────────────────────────────
    tabs = st.tabs([
        "📋 Summary",
        "✅ Action Items",
        "🔑 Key Decisions",
        "❓ Questions",
        "🧠 Quiz",
        "🔍 Fact Check",
        "💬 Video Chat",
        "📄 Transcript",
    ])

    # ── Tab 1: Summary ─────────────────────────────────────────────────────────
    with tabs[0]:
        st.markdown("#### 📋 Meeting / Video Summary")
        st.markdown(f'<div class="result-card">{res.get("summary","No summary available.")}</div>',
                    unsafe_allow_html=True)

    # ── Tab 2: Action Items ────────────────────────────────────────────────────
    with tabs[1]:
        st.markdown("#### ✅ Action Items")
        st.markdown(f'<div class="result-card">{res.get("action_item","No action items found.")}</div>',
                    unsafe_allow_html=True)

    # ── Tab 3: Key Decisions ───────────────────────────────────────────────────
    with tabs[2]:
        st.markdown("#### 🔑 Key Decisions")
        st.markdown(f'<div class="result-card">{res.get("key_decision","No key decisions found.")}</div>',
                    unsafe_allow_html=True)

    # ── Tab 4: Questions ───────────────────────────────────────────────────────
    with tabs[3]:
        st.markdown("#### ❓ Open Questions")
        st.markdown(f'<div class="result-card">{res.get("questions","No open questions found.")}</div>',
                    unsafe_allow_html=True)

    # ── Tab 5: Quiz ────────────────────────────────────────────────────────────
    with tabs[4]:
        st.markdown("#### 🧠 Interactive Quiz")
        quiz_qs = parse_quiz_json(res.get("quize", ""))

        if not quiz_qs:
            st.info("No quiz questions could be parsed from the response.")
            with st.expander("📄 Raw Quiz Output"):
                st.text(res.get("quize", ""))
        else:
            if not st.session_state.quiz_submitted:
                st.markdown(f"**{len(quiz_qs)} questions** generated from the video content.")
                st.markdown("---")

                for i, q in enumerate(quiz_qs):
                    qtext = q.get("question", f"Question {i+1}")
                    opts  = q.get("options", [])
                    st.markdown(f"""
                    <div class="quiz-card">
                        <div class="q-num">Question {i+1} of {len(quiz_qs)}</div>
                        <div class="q-text">{qtext}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if opts:
                        choice = st.radio(
                            f"q_{i}",
                            opts,
                            key=f"quiz_q_{i}",
                            label_visibility="collapsed",
                        )
                        st.session_state.quiz_answers[i] = choice
                    st.markdown("")

                if st.button("📊 Submit Quiz", use_container_width=False):
                    st.session_state.quiz_submitted = True
                    st.rerun()
            else:
                correct = 0
                st.markdown("#### 📊 Quiz Results")
                for i, q in enumerate(quiz_qs):
                    qtext   = q.get("question", f"Q{i+1}")
                    correct_ans = q.get("correct_answer", "")
                    user_ans    = st.session_state.quiz_answers.get(i, "")
                    is_right = user_ans.strip().lower() == correct_ans.strip().lower()
                    if is_right:
                        correct += 1
                    icon  = "✅" if is_right else "❌"
                    color = "#4ade80" if is_right else "#f87171"
                    st.markdown(f"""
                    <div class="quiz-card" style="border-color:{'rgba(74,222,128,0.3)' if is_right else 'rgba(248,113,113,0.3)'};">
                        <div class="q-num">Q{i+1}</div>
                        <div class="q-text">{qtext}</div>
                        <div style="font-size:13px;color:{color};margin-top:4px;">
                            {icon} Your answer: <strong>{user_ans}</strong><br/>
                            {'✓ Correct!' if is_right else f'Correct answer: <strong>{correct_ans}</strong>'}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                pct = int(correct / len(quiz_qs) * 100) if quiz_qs else 0
                st.markdown("---")
                st.markdown(f"### Score: {correct}/{len(quiz_qs)} ({pct}%)")
                st.progress(pct / 100)
                if pct == 100:
                    st.success("🏆 Perfect score!")
                elif pct >= 70:
                    st.success("🎉 Great job!")
                elif pct >= 40:
                    st.warning("📚 Keep studying!")
                else:
                    st.error("💪 Review the video and try again.")

                if st.button("🔄 Retake Quiz"):
                    st.session_state.quiz_answers = {}
                    st.session_state.quiz_submitted = False
                    st.rerun()

    # ── Tab 6: Fact Check ──────────────────────────────────────────────────────
    with tabs[5]:
        st.markdown("#### 🔍 Fact-Check Results")
        fact_results = res.get("fake_check") or []
        if not fact_results:
            st.info("No fact-check results available.")
        else:
            for i, fc in enumerate(fact_results, 1):
                verdict    = getattr(fc, "verdict", "Unknown")
                confidence = getattr(fc, "confidence", 0)
                reason     = getattr(fc, "reason", "No reason provided.")

                chip = render_verdict_chip(verdict)
                st.markdown(f"""
                <div class="result-card">
                    <h4>Chunk {i}</h4>
                    <div style="margin-bottom:10px;">{chip}</div>
                    <div class="conf-bar-wrap">
                        <div style="display:flex;justify-content:space-between;
                                    font-size:12px;color:#8891a8;margin-bottom:4px;">
                            <span>Confidence</span><span>{confidence}%</span>
                        </div>
                        <div class="conf-bar-bg">
                            <div class="conf-bar-fill" style="width:{confidence}%;"></div>
                        </div>
                    </div>
                    <div style="font-size:14px;color:#c5cad8;margin-top:10px;line-height:1.7;">
                        {reason}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ── Tab 7: Chat ────────────────────────────────────────────────────────────
    with tabs[6]:
        st.markdown("#### 💬 Ask Anything About the Video")
        retriever = res.get("retriever")

        if retriever is None:
            st.warning("Vector retriever not available. Check NVIDIA API key in .env")
        else:
            # Chat history display
            chat_container = st.container()
            with chat_container:
                if not st.session_state.chat_history:
                    st.markdown("""
                    <div style="text-align:center;padding:40px 0;color:#4a5066;">
                        <div style="font-size:40px;margin-bottom:12px;">💬</div>
                        <div style="font-size:15px;">Ask anything about the video content.</div>
                        <div style="font-size:13px;margin-top:6px;">
                            e.g. "What was the main topic discussed?" or "Summarize the key points."
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    for msg in st.session_state.chat_history:
                        if msg["role"] == "user":
                            st.markdown(f"""
                            <div class="chat-user">
                                <div class="bubble">{msg["content"]}</div>
                                <div class="avatar" style="background:#2a2f45;">👤</div>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="chat-ai">
                                <div class="avatar avatar-ai">🤖</div>
                                <div class="bubble">{msg["content"]}</div>
                            </div>
                            """, unsafe_allow_html=True)

            st.markdown("---")
            col_q, col_send = st.columns([6, 1])
            with col_q:
                user_question = st.text_input(
                    "chat_input",
                    placeholder="Ask a question about the video…",
                    label_visibility="collapsed",
                    key="chat_input_box",
                )
            with col_send:
                send_btn = st.button("Send ➤", use_container_width=True)

            if send_btn and user_question.strip():
                with st.spinner("Searching video knowledge base…"):
                    docs = retriever.invoke(user_question)
                    context = "\n\n".join([d.page_content for d in docs])
                    answer  = context if context.strip() else "I couldn't find relevant information in the video."

                st.session_state.chat_history.append({"role": "user", "content": user_question})
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
                st.rerun()

            if st.session_state.chat_history:
                if st.button("🗑️ Clear Chat"):
                    st.session_state.chat_history = []
                    st.rerun()

    # ── Tab 8: Transcript ──────────────────────────────────────────────────────
    with tabs[7]:
        st.markdown("#### 📄 Full Transcript")
        transcript = res.get("transcribe", "")
        if transcript:
            st.text_area(
                "transcript_area",
                value=transcript,
                height=400,
                label_visibility="collapsed",
            )
            st.download_button(
                "⬇️ Download as .txt",
                data=transcript,
                file_name="transcript.txt",
                mime="text/plain",
            )
        else:
            st.info("No transcript available.")


# ── Empty state (first load) ──────────────────────────────────────────────────
if not st.session_state.processed and not st.session_state.processing:
    st.markdown("""
    <div style="text-align:center;padding:60px 20px;color:#4a5066;">
        <div style="font-size:56px;margin-bottom:16px;">🎬</div>
        <div style="font-family:'Space Grotesk',sans-serif;font-size:22px;
                    color:#8891a8;font-weight:600;margin-bottom:10px;">
            Paste a YouTube URL to get started
        </div>
        <div style="font-size:14px;color:#3a4055;max-width:480px;margin:0 auto;line-height:1.8;">
            VideoMind analyses any YouTube video or local recording —
            transcribes, summarises, extracts decisions & action items,
            generates a quiz, fact-checks claims, and lets you chat with the content.
        </div>
    </div>
    """, unsafe_allow_html=True)
