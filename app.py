import streamlit as st
import time
from dotenv import load_dotenv
from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarizer import summarize, generate_title
from core.extractor import extract_action_items, extract_key_decisions, extract_questions
from core.rag_engine import build_rag_chain, ask_question

load_dotenv()

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Vissora AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;800;900&family=Exo+2:wght@300;400;500;600&family=JetBrains+Mono:wght@300;400;500&display=swap');

/* ── Root Variables ── */
:root {
    --bg:           #03000d;
    --surface:      #08051a;
    --surface-2:    #0f0b22;
    --surface-3:    #160f2e;
    --border:       #1e1640;
    --border-glow:  #3d1a8c;

    /* Neons */
    --neon-purple:  #b44fff;
    --neon-cyan:    #00f5ff;
    --neon-pink:    #ff2d9b;
    --neon-green:   #00ff88;
    --neon-yellow:  #ffe600;
    --neon-orange:  #ff6a00;

    --accent:       #b44fff;
    --accent-2:     #00f5ff;
    --text:         #e8e0ff;
    --text-muted:   #6a5fa0;
    --success:      #00ff88;
    --warning:      #ffe600;
    --danger:       #ff2d9b;
}

/* ── Global Reset ── */
html, body, [class*="css"] {
    font-family: 'Exo 2', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

.stApp {
    background: var(--bg) !important;
}

/* Animated neon grid background */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background-image:
        linear-gradient(rgba(180, 79, 255, 0.06) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 245, 255, 0.04) 1px, transparent 1px);
    background-size: 50px 50px;
    pointer-events: none;
    z-index: 0;
    animation: gridShift 20s linear infinite;
}

@keyframes gridShift {
    0%   { background-position: 0 0, 0 0; }
    100% { background-position: 50px 50px, 50px 50px; }
}

/* Ambient neon glow blobs */
.stApp::after {
    content: '';
    position: fixed;
    top: -20%; left: -10%;
    width: 60%; height: 60%;
    background: radial-gradient(ellipse, rgba(180,79,255,0.08) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
    animation: blobDrift 15s ease-in-out infinite alternate;
}

@keyframes blobDrift {
    0%   { transform: translate(0, 0); }
    100% { transform: translate(8%, 5%); }
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #070415 0%, #0a0520 100%) !important;
    border-right: 1px solid var(--border-glow) !important;
    box-shadow: 4px 0 30px rgba(180,79,255,0.12) !important;
}

[data-testid="stSidebar"] * {
    color: var(--text) !important;
}

/* ── Headings ── */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Orbitron', monospace !important;
    color: var(--text) !important;
}

/* ── Hero Title ── */
.hero-title {
    font-family: 'Orbitron', monospace;
    font-size: clamp(1.8rem, 5vw, 3.2rem);
    font-weight: 900;
    line-height: 1.1;
    margin: 0;
    background: linear-gradient(135deg, #ffffff 0%, var(--neon-purple) 40%, var(--neon-cyan) 80%, var(--neon-pink) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    filter: drop-shadow(0 0 20px rgba(180,79,255,0.5));
    animation: titleGlow 3s ease-in-out infinite alternate;
}

@keyframes titleGlow {
    0%   { filter: drop-shadow(0 0 15px rgba(180,79,255,0.5)); }
    50%  { filter: drop-shadow(0 0 30px rgba(0,245,255,0.6)); }
    100% { filter: drop-shadow(0 0 20px rgba(255,45,155,0.5)); }
}

.hero-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: var(--neon-cyan);
    letter-spacing: 0.3em;
    text-transform: uppercase;
    margin-top: 0.6rem;
    text-shadow: 0 0 12px rgba(0,245,255,0.6);
}

/* ── Cards ── */
.card {
    background: linear-gradient(135deg, var(--surface) 0%, var(--surface-2) 100%);
    border: 1px solid var(--border-glow);
    border-radius: 16px;
    padding: 1.6rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
    box-shadow: 0 4px 24px rgba(180,79,255,0.08), inset 0 1px 0 rgba(255,255,255,0.04);
}

.card:hover {
    border-color: var(--neon-purple);
    box-shadow: 0 8px 40px rgba(180,79,255,0.2), 0 0 0 1px rgba(180,79,255,0.15), inset 0 1px 0 rgba(255,255,255,0.06);
    transform: translateY(-2px);
}

/* Neon top edge line */
.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 2px;
    background: linear-gradient(90deg, transparent, var(--neon-purple), var(--neon-cyan), transparent);
    opacity: 0.7;
}

/* Animated corner accent */
.card::after {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 60px; height: 60px;
    background: radial-gradient(ellipse at top left, rgba(180,79,255,0.15), transparent 70%);
    pointer-events: none;
}

.card-title {
    font-family: 'Orbitron', monospace;
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--neon-cyan);
    text-shadow: 0 0 10px rgba(0,245,255,0.5);
    margin-bottom: 0.85rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.card-content {
    font-family: 'Exo 2', sans-serif;
    font-size: 0.875rem;
    line-height: 1.75;
    color: var(--text);
}

/* ── Accent Badge ── */
.badge {
    display: inline-flex;
    align-items: center;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    font-family: 'Orbitron', monospace;
}

.badge-purple {
    background: rgba(180,79,255,0.15);
    color: var(--neon-purple);
    border: 1px solid rgba(180,79,255,0.4);
    box-shadow: 0 0 12px rgba(180,79,255,0.2), inset 0 0 8px rgba(180,79,255,0.1);
    text-shadow: 0 0 8px rgba(180,79,255,0.8);
}
.badge-cyan {
    background: rgba(0,245,255,0.1);
    color: var(--neon-cyan);
    border: 1px solid rgba(0,245,255,0.35);
    box-shadow: 0 0 12px rgba(0,245,255,0.15), inset 0 0 8px rgba(0,245,255,0.08);
    text-shadow: 0 0 8px rgba(0,245,255,0.8);
}
.badge-green {
    background: rgba(0,255,136,0.1);
    color: var(--neon-green);
    border: 1px solid rgba(0,255,136,0.35);
    box-shadow: 0 0 12px rgba(0,255,136,0.15), inset 0 0 8px rgba(0,255,136,0.08);
    text-shadow: 0 0 8px rgba(0,255,136,0.8);
}

/* ── Input & Buttons ── */
.stTextInput > div > div > input,
.stSelectbox > div > div {
    background: var(--surface-2) !important;
    border: 1px solid var(--border-glow) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'JetBrains Mono', monospace !important;
    transition: all 0.25s ease !important;
}

.stTextInput > div > div > input:focus {
    border-color: var(--neon-purple) !important;
    box-shadow: 0 0 0 2px rgba(180,79,255,0.2), 0 0 20px rgba(180,79,255,0.15) !important;
}

.stButton > button {
    background: linear-gradient(135deg, #8b00e8 0%, #b44fff 50%, #6600cc 100%) !important;
    color: white !important;
    border: 1px solid rgba(180,79,255,0.5) !important;
    border-radius: 10px !important;
    font-family: 'Orbitron', monospace !important;
    font-weight: 700 !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.12em !important;
    padding: 0.65rem 1.5rem !important;
    transition: all 0.25s ease !important;
    text-transform: uppercase !important;
    box-shadow: 0 4px 20px rgba(180,79,255,0.35), inset 0 1px 0 rgba(255,255,255,0.15) !important;
    text-shadow: 0 0 10px rgba(255,255,255,0.4) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 35px rgba(180,79,255,0.55), 0 0 60px rgba(180,79,255,0.2) !important;
    border-color: var(--neon-cyan) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* Secondary button */
.stButton > button[kind="secondary"] {
    background: var(--surface-2) !important;
    border: 1px solid var(--border-glow) !important;
    box-shadow: none !important;
}

/* ── Progress / Status ── */
.status-bar {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.7rem 1rem;
    background: var(--surface-2);
    border-radius: 10px;
    margin: 0.35rem 0;
    border: 1px solid var(--border);
    font-size: 0.78rem;
    font-family: 'JetBrains Mono', monospace;
    transition: border-color 0.2s;
}

.status-bar:hover { border-color: var(--border-glow); }

.status-dot {
    width: 9px; height: 9px;
    border-radius: 50%;
    flex-shrink: 0;
}

.dot-active {
    background: var(--neon-purple);
    box-shadow: 0 0 10px var(--neon-purple), 0 0 20px rgba(180,79,255,0.5);
    animation: pulse 1.2s infinite;
}
.dot-done {
    background: var(--neon-green);
    box-shadow: 0 0 8px var(--neon-green);
}
.dot-pending { background: var(--border); }

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.5; transform: scale(0.8); }
}

/* ── Chat ── */
.chat-container {
    background: linear-gradient(135deg, var(--surface) 0%, var(--surface-2) 100%);
    border: 1px solid var(--border-glow);
    border-radius: 16px;
    padding: 1.4rem;
    max-height: 440px;
    overflow-y: auto;
    box-shadow: inset 0 2px 20px rgba(180,79,255,0.05);
    margin-bottom: 1rem;
}

.chat-msg {
    margin-bottom: 1.1rem;
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
}

.chat-label {
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    font-family: 'Orbitron', monospace;
}

.chat-bubble {
    display: inline-block;
    padding: 0.75rem 1.1rem;
    border-radius: 12px;
    font-size: 0.85rem;
    line-height: 1.65;
    max-width: 90%;
    font-family: 'Exo 2', sans-serif;
}

.user-label  {
    color: var(--neon-purple);
    text-shadow: 0 0 10px rgba(180,79,255,0.7);
}
.bot-label   {
    color: var(--neon-cyan);
    text-shadow: 0 0 10px rgba(0,245,255,0.7);
}

.user-bubble {
    background: linear-gradient(135deg, rgba(180,79,255,0.15), rgba(180,79,255,0.08));
    border: 1px solid rgba(180,79,255,0.35);
    align-self: flex-end;
    box-shadow: 0 2px 16px rgba(180,79,255,0.15);
}
.bot-bubble  {
    background: linear-gradient(135deg, rgba(0,245,255,0.1), rgba(0,245,255,0.05));
    border: 1px solid rgba(0,245,255,0.3);
    align-self: flex-start;
    box-shadow: 0 2px 16px rgba(0,245,255,0.1);
}

/* ── Divider ── */
hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, var(--border-glow), transparent) !important;
    margin: 1.8rem 0 !important;
}

/* ── Transcript box ── */
.transcript-box {
    background: var(--surface-2);
    border: 1px solid var(--border-glow);
    border-radius: 10px;
    padding: 1.3rem;
    font-size: 0.8rem;
    line-height: 1.85;
    max-height: 320px;
    overflow-y: auto;
    color: var(--text-muted);
    white-space: pre-wrap;
    word-break: break-word;
    font-family: 'JetBrains Mono', monospace;
    box-shadow: inset 0 2px 12px rgba(180,79,255,0.05);
}

/* ── Streamlit overrides ── */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--neon-purple), var(--neon-cyan)) !important;
    box-shadow: 0 0 10px rgba(180,79,255,0.5) !important;
}
.stSpinner > div {
    border-top-color: var(--neon-purple) !important;
    filter: drop-shadow(0 0 6px rgba(180,79,255,0.5));
}
[data-testid="stMarkdownContainer"] p { color: var(--text) !important; }
label { color: var(--text-muted) !important; font-size: 0.78rem !important; font-family: 'Exo 2', sans-serif !important; }

/* ── Alert / Info boxes ── */
.stAlert {
    background: rgba(180,79,255,0.08) !important;
    border: 1px solid rgba(180,79,255,0.3) !important;
    border-radius: 10px !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: var(--surface-2) !important;
    border: 1px solid var(--border-glow) !important;
    border-radius: 10px !important;
    color: var(--neon-cyan) !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 0.75rem !important;
}

/* scrollbar */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, var(--neon-purple), var(--neon-cyan));
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover { background: var(--neon-pink); }

/* ── Neon separator line utility ── */
.neon-line {
    height: 1px;
    background: linear-gradient(90deg, transparent 0%, var(--neon-purple) 30%, var(--neon-cyan) 70%, transparent 100%);
    box-shadow: 0 0 8px rgba(180,79,255,0.4);
    margin: 1.5rem 0;
}

/* ── Section heading style ── */
.section-heading {
    font-family: 'Orbitron', monospace;
    font-size: 1rem;
    font-weight: 700;
    color: var(--text);
    letter-spacing: 0.08em;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.section-heading::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--border-glow), transparent);
}
</style>
""", unsafe_allow_html=True)

# ─── Session State Init ──────────────────────────────────────────────────────────
for key, default in {
    "result": None,
    "chat_history": [],
    "processing": False,
    "pipeline_done": False,
    "pipeline_steps": {},
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ─── Helpers ────────────────────────────────────────────────────────────────────
def step_status(steps: dict, key: str) -> str:
    s = steps.get(key, "pending")
    if s == "active":  return "dot-active"
    if s == "done":    return "dot-done"
    return "dot-pending"

def render_step_bar(label: str, key: str, icon: str):
    css = step_status(st.session_state.pipeline_steps, key)
    st.markdown(f"""
    <div class="status-bar">
        <div class="status-dot {css}"></div>
        <span>{icon} {label}</span>
    </div>""", unsafe_allow_html=True)

# ─── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('''
    <div style="padding:0.5rem 0 1rem">
        <div class="hero-title" style="font-size:1.5rem;line-height:1.2">🎬 VISSORA<br><span style="color:var(--neon-cyan);font-size:1rem;-webkit-text-fill-color:var(--neon-cyan);filter:none">AI</span></div>
        <div class="hero-sub" style="margin-top:0.4rem">Video Intelligence</div>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown('<div class="neon-line"></div>', unsafe_allow_html=True)

    st.markdown('<span class="badge badge-purple">⚡ Input Source</span>', unsafe_allow_html=True)
    source = st.text_input("YouTube URL or File Path", placeholder="https://youtube.com/watch?v=... or /path/to/file.mp4")

    language = st.selectbox("Language", ["english", "hinglish"], index=0)

    run_btn = st.button("⚡  ANALYSE", use_container_width=True)

    if st.session_state.pipeline_done:
        st.markdown('<div class="neon-line"></div>', unsafe_allow_html=True)
        st.markdown('<span class="badge badge-green">✦ Pipeline Status</span>', unsafe_allow_html=True)
        for step, icon, label in [
            ("audio",      "🔊", "Audio Processing"),
            ("transcript", "📝", "Transcription"),
            ("title",      "🏷️", "Title Generation"),
            ("summary",    "📋", "Summarisation"),
            ("extract",    "🔍", "Extraction"),
            ("rag",        "🧠", "RAG Engine"),
        ]:
            render_step_bar(label, step, icon)

# ─── Main Area ──────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">AI Video Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">◈ Transcribe &nbsp;·&nbsp; Summarise &nbsp;·&nbsp; Chat with your meetings</div>', unsafe_allow_html=True)
st.markdown('<div class="neon-line"></div>', unsafe_allow_html=True)

# ── Run Pipeline ────────────────────────────────────────────────────────────────
if run_btn:
    if not source.strip():
        st.error("Please enter a YouTube URL or file path.")
    else:
        st.session_state.pipeline_done = False
        st.session_state.result = None
        st.session_state.chat_history = []
        st.session_state.pipeline_steps = {}

        progress_placeholder = st.empty()

        def update_step(key, state):
            st.session_state.pipeline_steps[key] = state

        try:
            with progress_placeholder.container():
                st.info("⚙️ Pipeline running — see sidebar for live status…")

            update_step("audio", "active")
            chunks = process_input(source)
            update_step("audio", "done")

            update_step("transcript", "active")
            transcript = transcribe_all(chunks, language)
            update_step("transcript", "done")

            update_step("title", "active")
            title = generate_title(transcript)
            update_step("title", "done")

            update_step("summary", "active")
            summary = summarize(transcript)
            update_step("summary", "done")

            update_step("extract", "active")
            action_items  = extract_action_items(transcript)
            decisions     = extract_key_decisions(transcript)
            questions     = extract_questions(transcript)
            update_step("extract", "done")

            update_step("rag", "active")
            rag_chain = build_rag_chain(transcript)
            update_step("rag", "done")

            st.session_state.result = {
                "title": title,
                "transcript": transcript,
                "summary": summary,
                "action_items": action_items,
                "key_decisions": decisions,
                "open_questions": questions,
                "rag_chain": rag_chain,
            }
            st.session_state.pipeline_done = True
            progress_placeholder.success("✅ Analysis complete!")
            time.sleep(0.5)
            progress_placeholder.empty()
            st.rerun()

        except Exception as e:
            for k in ["audio","transcript","title","summary","extract","rag"]:
                if st.session_state.pipeline_steps.get(k) == "active":
                    st.session_state.pipeline_steps[k] = "pending"
            progress_placeholder.error(f"❌ Error: {e}")

# ── Results ──────────────────────────────────────────────────────────────────────
if st.session_state.result:
    r = st.session_state.result

    # Title banner
    st.markdown(f"""
    <div class="card">
        <div class="card-title">📌 Session Title</div>
        <div style="font-family:'Orbitron',monospace;font-size:1.3rem;font-weight:700;background:linear-gradient(135deg,#fff,var(--neon-purple));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">
            {r['title']}
        </div>
    </div>""", unsafe_allow_html=True)

    # Top row: summary + transcript
    col1, col2 = st.columns([3, 2], gap="medium")

    with col1:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">📋 Summary</div>
            <div class="card-content">{r['summary']}</div>
        </div>""", unsafe_allow_html=True)

    with col2:
        with st.expander("📝 Full Transcript", expanded=False):
            st.markdown(f'<div class="transcript-box">{r["transcript"]}</div>', unsafe_allow_html=True)

    # Second row: action items | decisions | questions
    c1, c2, c3 = st.columns(3, gap="medium")

    with c1:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">✅ Action Items</div>
            <div class="card-content">{r['action_items']}</div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">🔑 Key Decisions</div>
            <div class="card-content">{r['key_decisions']}</div>
        </div>""", unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">❓ Open Questions</div>
            <div class="card-content">{r['open_questions']}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="neon-line"></div>', unsafe_allow_html=True)

    # ── RAG Chat ──────────────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">💬 Chat with your Meeting</div>', unsafe_allow_html=True)

    # Chat history display
    if st.session_state.chat_history:
        chat_html = '<div class="chat-container">'
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                chat_html += f"""
                <div class="chat-msg" style="align-items:flex-end">
                    <span class="chat-label user-label">You</span>
                    <div class="chat-bubble user-bubble">{msg['content']}</div>
                </div>"""
            else:
                chat_html += f"""
                <div class="chat-msg" style="align-items:flex-start">
                    <span class="chat-label bot-label">🤖 Assistant</span>
                    <div class="chat-bubble bot-bubble">{msg['content']}</div>
                </div>"""
        chat_html += '</div>'
        st.markdown(chat_html, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="card" style="text-align:center;padding:2rem">
            <div style="font-size:2rem;margin-bottom:0.5rem">💬</div>
            <div style="color:var(--text-muted);font-size:0.85rem">Ask anything about your meeting transcript</div>
        </div>""", unsafe_allow_html=True)

    # Chat input
    chat_col1, chat_col2 = st.columns([5, 1], gap="small")
    with chat_col1:
        user_input = st.text_input("Your question", placeholder="What were the main decisions made?", label_visibility="collapsed")
    with chat_col2:
        send_btn = st.button("Send →", use_container_width=True)

    if send_btn and user_input.strip():
        with st.spinner("Thinking…"):
            answer = ask_question(r["rag_chain"], user_input.strip())
        st.session_state.chat_history.append({"role": "user",      "content": user_input.strip()})
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.rerun()

    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat", type="secondary"):
            st.session_state.chat_history = []
            st.rerun()

else:
    # Empty state
    st.markdown("""
    <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding:5rem 2rem;text-align:center">
        <div style="font-size:4.5rem;margin-bottom:1.2rem;filter:drop-shadow(0 0 20px rgba(180,79,255,0.6))">🎬</div>
        <div style="font-family:'Orbitron',monospace;font-size:1.5rem;font-weight:800;background:linear-gradient(135deg,#fff,var(--neon-purple),var(--neon-cyan));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:0.6rem">
            READY TO ANALYSE
        </div>
        <div style="color:var(--text-muted);font-size:0.85rem;max-width:400px;line-height:1.8;font-family:'Exo 2',sans-serif">
            Paste a YouTube URL or local file path in the sidebar, choose your language, and hit <strong style="color:var(--neon-purple)">ANALYSE</strong> to unlock your meeting insights.
        </div>
        <div style="margin-top:2.5rem;display:flex;gap:1rem;flex-wrap:wrap;justify-content:center">
            <span class="badge badge-purple">⚡ Transcription</span>
            <span class="badge badge-cyan">◈ Summarisation</span>
            <span class="badge badge-green">✦ RAG Chat</span>
        </div>
        <div style="margin-top:3rem;width:100%;max-width:420px;height:1px;background:linear-gradient(90deg,transparent,var(--neon-purple),var(--neon-cyan),transparent);box-shadow:0 0 12px rgba(180,79,255,0.3)"></div>
    </div>""", unsafe_allow_html=True)