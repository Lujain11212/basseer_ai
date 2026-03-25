"""
بصير AI – لوحة المراقبة والتحليلات v4 — Dark Premium UI (Refined)
Basseer AI – Dashboard v4 (Dark Theme, Professional Icons)

ثلاث واجهات:
  1. إدخال الاستبيان — Survey Entry
  2. الباحث الميداني — Field Researcher
  3. لوحة الجهة المشرفة — Authority Dashboard
"""
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json

st.set_page_config(
    page_title="بصير AI – الحارس الدلالي",
    page_icon="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%233b82f6'><path d='M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4z'/></svg>",
    layout="wide",
    initial_sidebar_state="collapsed",
)

API = "http://127.0.0.1:8000"

# ══════════════════════════════════════════════════════════
# DARK PREMIUM CSS THEME — v4 Refined
# ══════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ── Design Tokens ── */
:root {
  --bg-base:       #0b0f1c;
  --bg-surface:    rgba(255,255,255,0.055);
  --bg-surface-hv: rgba(255,255,255,0.085);
  --bg-glass:      rgba(255,255,255,0.06);
  --glass-border:  rgba(255,255,255,0.10);
  --glass-blur:    blur(16px);

  --text-primary:  #f1f5f9;
  --text-secondary:#94a3b8;
  --text-muted:    #64748b;

  --blue:    #3b82f6;
  --sky:     #38bdf8;
  --emerald: #34d399;
  --amber:   #fbbf24;
  --red:     #f87171;
  --violet:  #a78bfa;
  --pink:    #f472b6;

  --green-glow:  rgba(52,211,153,0.18);
  --amber-glow:  rgba(251,191,36,0.18);
  --red-glow:    rgba(248,113,113,0.18);
  --blue-glow:   rgba(59,130,246,0.18);
  --violet-glow: rgba(167,139,250,0.18);

  --radius-sm: 10px;
  --radius-md: 14px;
  --radius-lg: 18px;
  --radius-xl: 24px;

  --shadow-glass: 0 8px 32px rgba(0,0,0,0.35);
  --shadow-glow:  0 0 24px rgba(59,130,246,0.15);

  /* Dropdown dark theme */
  --dd-bg:       #13192e;
  --dd-border:   rgba(255,255,255,0.13);
  --dd-text:     #f1f5f9;
  --dd-hover:    rgba(59,130,246,0.22);
  --dd-selected: rgba(59,130,246,0.35);
}

/* ── Base ── */
* { box-sizing: border-box; }

html, body, [class*="css"],
h1,h2,h3,h4,h5,h6,p,span,div,label,button,.stMarkdown {
    font-family: 'IBM Plex Sans Arabic', 'Tajawal', 'Inter', sans-serif !important;
    color: var(--text-primary);
}

/* ── Global Background ── */
.stApp,
.stApp > div,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"] {
    background: linear-gradient(135deg, #0b0f1c 0%, #111827 45%, #1a1040 75%, #0c1a2e 100%) !important;
    min-height: 100vh;
}

/* subtle grid overlay */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(255,255,255,0.015) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.015) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
}

.main .block-container {
    max-width: 1440px;
    padding-top: 0.6rem;
    padding-bottom: 3rem;
    padding-left: 1.5rem;
    padding-right: 1.5rem;
    position: relative;
    z-index: 1;
}

.rtl {
    direction: rtl;
    text-align: right;
}

/* ═══════════════════════════════════════
   HEADER — centered, elegant, focal point
   ═══════════════════════════════════════ */
.main-header {
    background: linear-gradient(135deg,
        rgba(30,41,59,0.95) 0%,
        rgba(15,23,42,0.98) 40%,
        rgba(30,27,75,0.95) 70%,
        rgba(12,26,46,0.98) 100%);
    backdrop-filter: var(--glass-blur);
    -webkit-backdrop-filter: var(--glass-blur);
    border: 1px solid var(--glass-border);
    padding: 2rem 2.4rem 1.8rem;
    border-radius: var(--radius-xl);
    margin-bottom: 1.2rem;
    box-shadow: var(--shadow-glass), inset 0 1px 0 rgba(255,255,255,0.07);
    position: relative;
    overflow: hidden;
}
.main-header::before {
    content: '';
    position: absolute;
    top: -60%;
    right: -8%;
    width: 480px;
    height: 480px;
    background: radial-gradient(circle, rgba(56,189,248,0.12) 0%, transparent 65%);
    border-radius: 50%;
    pointer-events: none;
}
.main-header::after {
    content: '';
    position: absolute;
    bottom: -60%;
    left: -8%;
    width: 380px;
    height: 380px;
    background: radial-gradient(circle, rgba(167,139,250,0.10) 0%, transparent 65%);
    border-radius: 50%;
    pointer-events: none;
}

/* centered title block */
.header-center {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    position: relative;
    z-index: 1;
    gap: 0.5rem;
}
.header-icon-wrap {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 52px;
    height: 52px;
    border-radius: 14px;
    background: linear-gradient(135deg, rgba(59,130,246,0.25) 0%, rgba(99,102,241,0.22) 100%);
    border: 1px solid rgba(99,102,241,0.35);
    box-shadow: 0 0 24px rgba(59,130,246,0.20);
    margin-bottom: 0.3rem;
}
.header-title {
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.025em;
    line-height: 1.2;
    background: linear-gradient(90deg, #f1f5f9 0%, #93c5fd 50%, #a5b4fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
}
.header-subtitle {
    font-size: 0.88rem;
    color: #94a3b8;
    font-weight: 400;
    text-align: center;
    max-width: 540px;
    line-height: 1.6;
}
.header-badges {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.55rem;
    margin-top: 0.3rem;
    flex-wrap: wrap;
}
.header-badge {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.13);
    border-radius: 20px;
    padding: 0.28rem 0.85rem;
    font-size: 0.76rem;
    color: #93c5fd;
    font-weight: 600;
    backdrop-filter: blur(8px);
    white-space: nowrap;
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
}
.header-badge.live {
    color: #6ee7b7;
    border-color: rgba(52,211,153,0.25);
}

/* ── SECTION HEADERS ── */
.section-header {
    direction: rtl;
    text-align: right;
    padding: 0.3rem 0 0.5rem;
    margin: 1.2rem 0 0.7rem;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
}
.section-header h3 {
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-header .subtitle {
    font-size: 0.77rem;
    color: var(--text-muted);
    margin-top: 0.25rem;
}

/* ── GLASS CARDS (base) ── */
.glass-card {
    background: var(--bg-glass);
    backdrop-filter: var(--glass-blur);
    -webkit-backdrop-filter: var(--glass-blur);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-glass);
    transition: transform 0.18s ease, box-shadow 0.18s ease, background 0.18s ease;
}
.glass-card:hover {
    background: var(--bg-surface-hv);
    transform: translateY(-2px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.45);
}

/* ── KPI CARDS ── */
.kpi-card {
    background: rgba(255,255,255,0.055);
    backdrop-filter: var(--glass-blur);
    -webkit-backdrop-filter: var(--glass-blur);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: var(--radius-md);
    padding: 1.15rem 1rem 1rem;
    text-align: center;
    box-shadow: 0 4px 24px rgba(0,0,0,0.30);
    direction: rtl;
    transition: transform 0.18s ease, box-shadow 0.18s ease, background 0.18s ease;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(255,255,255,0.03) 0%, transparent 60%);
    pointer-events: none;
}
.kpi-card:hover {
    transform: translateY(-3px);
    background: rgba(255,255,255,0.08);
    box-shadow: 0 8px 32px rgba(0,0,0,0.40);
}
.kpi-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 0.3rem;
    width: 36px;
    height: 36px;
}
.kpi-icon svg { width: 22px; height: 22px; }
.kpi-value {
    font-size: 1.85rem;
    font-weight: 900;
    margin: 0.2rem 0 0.15rem;
    line-height: 1;
    letter-spacing: -0.03em;
    color: #f1f5f9;
}
.kpi-label {
    font-size: 0.68rem;
    color: var(--text-muted);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.kpi-sub  { font-size: 0.65rem; color: var(--text-muted); margin-top: 0.1rem; }
.kpi-bar  {
    height: 3px;
    border-radius: 2px;
    margin-top: 0.7rem;
    background: rgba(255,255,255,0.08);
    overflow: hidden;
}
.kpi-bar-fill { height: 100%; border-radius: 2px; }

/* ── FORM GROUP CARD ── */
.form-group {
    background: rgba(255,255,255,0.05);
    backdrop-filter: var(--glass-blur);
    -webkit-backdrop-filter: var(--glass-blur);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: var(--radius-md);
    padding: 1.2rem 1.2rem 0.9rem;
    margin-bottom: 0.85rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.25);
}
.form-group-label {
    font-size: 0.72rem;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.07em;
    direction: rtl;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.45rem;
}
.form-group-label svg { width: 14px; height: 14px; flex-shrink: 0; }

/* ── WARNING CARDS ── */
.warning-card {
    background: rgba(248,113,113,0.10);
    border-right: 3px solid #f87171;
    border-left: none;
    border-top: 1px solid rgba(248,113,113,0.20);
    border-bottom: 1px solid rgba(248,113,113,0.20);
    padding: 0.7rem 1rem 0.7rem 0.8rem;
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    margin: 0.4rem 0;
    direction: rtl;
    font-size: 0.88rem;
    line-height: 1.6;
    color: #fca5a5;
    backdrop-filter: blur(8px);
}
.warning-card.medium {
    background: rgba(251,191,36,0.10);
    border-right-color: #fbbf24;
    border-top-color:   rgba(251,191,36,0.20);
    border-bottom-color:rgba(251,191,36,0.20);
    color: #fde68a;
}
.warning-card.low {
    background: rgba(59,130,246,0.10);
    border-right-color: #60a5fa;
    border-top-color:   rgba(59,130,246,0.20);
    border-bottom-color:rgba(59,130,246,0.20);
    color: #93c5fd;
}

/* ── RECOMMENDATION CARDS ── */
.rec-card {
    background: rgba(52,211,153,0.09);
    border-right: 3px solid #34d399;
    border-top: 1px solid rgba(52,211,153,0.20);
    border-bottom: 1px solid rgba(52,211,153,0.20);
    padding: 0.7rem 1rem 0.7rem 0.8rem;
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    margin: 0.4rem 0;
    direction: rtl;
    font-size: 0.88rem;
    line-height: 1.6;
    color: #6ee7b7;
    backdrop-filter: blur(8px);
}
.rec-card.system {
    background: rgba(167,139,250,0.09);
    border-right-color: #a78bfa;
    border-top-color:   rgba(167,139,250,0.20);
    border-bottom-color:rgba(167,139,250,0.20);
    color: #c4b5fd;
}

/* ── SCORE DISPLAY ── */
.score-high   { background: rgba(52,211,153,0.10);  border: 1px solid rgba(52,211,153,0.30);  color: #34d399; }
.score-medium { background: rgba(251,191,36,0.10);  border: 1px solid rgba(251,191,36,0.30);  color: #fbbf24; }
.score-low    { background: rgba(248,113,113,0.10); border: 1px solid rgba(248,113,113,0.30); color: #f87171; }
@keyframes score-in {
    from { opacity: 0; transform: scale(0.88) translateY(8px); }
    to   { opacity: 1; transform: scale(1)    translateY(0);   }
}
.score-display {
    animation: score-in 0.4s cubic-bezier(0.34,1.56,0.64,1);
    text-align: center;
    padding: 1.4rem 1.2rem;
    border-radius: var(--radius-lg);
    margin: 0.5rem 0;
    direction: rtl;
    backdrop-filter: var(--glass-blur);
}

/* ── HEALTH BADGES ── */
.health-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.22rem 0.75rem;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
    margin: 0.1rem;
}
.health-ok   { background: rgba(52,211,153,0.18);  color: #6ee7b7; border: 1px solid rgba(52,211,153,0.3); }
.health-warn { background: rgba(251,191,36,0.18);  color: #fde68a; border: 1px solid rgba(251,191,36,0.3); }
.health-off  { background: rgba(248,113,113,0.18); color: #fca5a5; border: 1px solid rgba(248,113,113,0.3); }

/* ── STATUS PILLS ── */
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
}
.pill-pending    { background: rgba(251,191,36,0.18);  color: #fde68a; border:1px solid rgba(251,191,36,0.3); }
.pill-confirmed  { background: rgba(52,211,153,0.18);  color: #6ee7b7; border:1px solid rgba(52,211,153,0.3); }
.pill-escalated  { background: rgba(248,113,113,0.18); color: #fca5a5; border:1px solid rgba(248,113,113,0.3); }
.pill-reviewed   { background: rgba(59,130,246,0.18);  color: #93c5fd; border:1px solid rgba(59,130,246,0.3); }
.pill-correction { background: rgba(167,139,250,0.18); color: #c4b5fd; border:1px solid rgba(167,139,250,0.3); }

/* ── SCORE BADGE ── */
.score-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    padding: 0.22rem 0.7rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 700;
}
.score-badge.high   { background: rgba(52,211,153,0.18);  color: #34d399; border:1px solid rgba(52,211,153,0.3); }
.score-badge.medium { background: rgba(251,191,36,0.18);  color: #fbbf24; border:1px solid rgba(251,191,36,0.3); }
.score-badge.low    { background: rgba(248,113,113,0.18); color: #f87171; border:1px solid rgba(248,113,113,0.3); }

/* ── DETAIL PANEL ── */
.detail-panel {
    background: rgba(255,255,255,0.05);
    backdrop-filter: var(--glass-blur);
    -webkit-backdrop-filter: var(--glass-blur);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: var(--radius-lg);
    padding: 1.3rem 1.4rem;
    direction: rtl;
    margin: 1rem 0;
    box-shadow: 0 4px 20px rgba(0,0,0,0.30);
    color: var(--text-primary);
}

/* ── SETUP BOX ── */
.setup-box {
    background: rgba(56,189,248,0.08);
    backdrop-filter: var(--glass-blur);
    border: 1px solid rgba(56,189,248,0.22);
    border-radius: var(--radius-lg);
    padding: 1.4rem;
    direction: rtl;
    margin: 1rem 0;
    box-shadow: 0 4px 20px rgba(0,0,0,0.25);
    color: var(--text-primary);
}

/* ── DEMO TIP ── */
.demo-tip {
    background: rgba(167,139,250,0.10);
    border: 1px solid rgba(167,139,250,0.25);
    border-radius: var(--radius-md);
    padding: 0.75rem 1.1rem;
    direction: rtl;
    font-size: 0.83rem;
    color: #c4b5fd;
    margin-bottom: 0.9rem;
    backdrop-filter: blur(8px);
    display: flex;
    align-items: flex-start;
    gap: 0.6rem;
}
.demo-tip svg { width: 16px; height: 16px; flex-shrink: 0; margin-top: 1px; }

/* ── INFO CHIPS ── */
.info-row {
    display: flex;
    gap: 0.45rem;
    flex-wrap: wrap;
    direction: rtl;
    margin: 0.5rem 0;
}
.info-chip {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 20px;
    padding: 0.2rem 0.75rem;
    font-size: 0.77rem;
    color: var(--text-secondary);
    font-weight: 500;
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
}
.info-chip svg { width: 12px; height: 12px; }

/* ── DIVIDER ── */
.section-divider {
    height: 1px;
    background: linear-gradient(to left, transparent, rgba(255,255,255,0.10), transparent);
    margin: 2rem 0;
    border: none;
}

/* ── EMPTY STATE ── */
.empty-state {
    text-align: center;
    padding: 3.5rem 1rem;
    direction: rtl;
}
.empty-state .empty-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 1rem;
    width: 64px;
    height: 64px;
    border-radius: 18px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
}
.empty-state .empty-icon svg { width: 32px; height: 32px; color: #64748b; }
.empty-state .empty-title { font-size: 1rem; font-weight: 700; color: var(--text-secondary); }
.empty-state .empty-desc  { font-size: 0.82rem; margin-top: 0.4rem; color: var(--text-muted); }

/* ── LIVE DOT ── */
@keyframes pulse-dot {
    0%, 100% { opacity:1; transform:scale(1); }
    50%       { opacity:0.4; transform:scale(1.35); }
}
.live-dot {
    display: inline-block;
    width: 7px;
    height: 7px;
    background: #34d399;
    border-radius: 50%;
    animation: pulse-dot 2s ease-in-out infinite;
    flex-shrink: 0;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: rgba(255,255,255,0.05);
    backdrop-filter: var(--glass-blur);
    border-radius: var(--radius-md);
    padding: 4px;
    border: 1px solid rgba(255,255,255,0.09);
}
.stTabs [data-baseweb="tab"] {
    border-radius: var(--radius-sm);
    padding: 0.55rem 1.1rem;
    font-weight: 600;
    font-size: 0.9rem;
    color: var(--text-muted) !important;
    transition: all 0.15s ease;
    background: transparent;
}
.stTabs [aria-selected="true"] {
    background: rgba(59,130,246,0.20) !important;
    color: #93c5fd !important;
    box-shadow: 0 0 0 1px rgba(59,130,246,0.35) !important;
}

/* ── BUTTONS ── */
.stButton > button {
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    transition: all 0.15s ease !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    background: rgba(255,255,255,0.07) !important;
    color: var(--text-primary) !important;
}
.stButton > button:hover {
    background: rgba(255,255,255,0.12) !important;
    border-color: rgba(255,255,255,0.20) !important;
    transform: translateY(-1px) !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #1d4ed8, #4f46e5) !important;
    border: 1px solid rgba(99,102,241,0.50) !important;
    color: white !important;
    box-shadow: 0 4px 16px rgba(79,70,229,0.40) !important;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #2563eb, #6366f1) !important;
    box-shadow: 0 6px 20px rgba(79,70,229,0.55) !important;
}

/* ══════════════════════════════════════════════════════════
   INPUT FIELDS — Premium dark SaaS style
   Targets: text_input, number_input, selectbox, textarea
   ══════════════════════════════════════════════════════════ */

/* ── Shared input variable overrides ── */
:root {
  --input-bg:          #0f1629;
  --input-bg-hover:    #141d35;
  --input-bg-focus:    #101828;
  --input-border:      rgba(99,130,180,0.22);
  --input-border-hover:rgba(99,130,180,0.40);
  --input-border-focus:rgba(59,130,246,0.65);
  --input-text:        #e8edf5;
  --input-placeholder: rgba(148,163,184,0.45);
  --input-glow-focus:  0 0 0 3px rgba(59,130,246,0.14), 0 2px 8px rgba(0,0,0,0.40);
  --input-shadow:      0 2px 8px rgba(0,0,0,0.35);
  --input-radius:      12px;
}

/* ── Wrapper containers ── */
.stTextInput > div,
.stNumberInput > div,
.stSelectbox > div {
    background: transparent !important;
}

/* ── Inner container (the visible box) ── */
.stTextInput > div > div,
.stNumberInput > div > div,
.stSelectbox > div > div {
    background: var(--input-bg) !important;
    border: 1px solid var(--input-border) !important;
    border-radius: var(--input-radius) !important;
    box-shadow: var(--input-shadow) !important;
    transition: border-color 0.18s ease, box-shadow 0.18s ease, background 0.18s ease !important;
}
.stTextInput > div > div:hover,
.stNumberInput > div > div:hover,
.stSelectbox > div > div:hover {
    background: var(--input-bg-hover) !important;
    border-color: var(--input-border-hover) !important;
}
.stTextInput > div > div:focus-within,
.stNumberInput > div > div:focus-within {
    background: var(--input-bg-focus) !important;
    border-color: var(--input-border-focus) !important;
    box-shadow: var(--input-glow-focus) !important;
}

/* ── Actual <input> elements ── */
.stTextInput input,
.stTextInput input[type="text"],
.stTextInput input[type="password"],
.stNumberInput input,
.stNumberInput input[type="number"],
textarea {
    background: transparent !important;
    background-color: transparent !important;
    color: var(--input-text) !important;
    -webkit-text-fill-color: var(--input-text) !important;
    border: none !important;
    border-radius: var(--input-radius) !important;
    caret-color: #60a5fa !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.01em;
    outline: none !important;
    box-shadow: none !important;
}

/* Raw input fallback (catches any missed types) */
input[type="text"],
input[type="number"],
input[type="password"],
input[type="search"],
input[type="email"] {
    background: var(--input-bg) !important;
    background-color: var(--input-bg) !important;
    color: var(--input-text) !important;
    -webkit-text-fill-color: var(--input-text) !important;
    border: 1px solid var(--input-border) !important;
    border-radius: var(--input-radius) !important;
    caret-color: #60a5fa !important;
}
input[type="text"]:hover,
input[type="number"]:hover,
input[type="password"]:hover {
    border-color: var(--input-border-hover) !important;
}
input[type="text"]:focus,
input[type="number"]:focus,
input[type="password"]:focus {
    border-color: var(--input-border-focus) !important;
    box-shadow: var(--input-glow-focus) !important;
    outline: none !important;
}

/* Chrome autofill — kill the white flash */
input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus,
input:-webkit-autofill:active {
    -webkit-text-fill-color: var(--input-text) !important;
    -webkit-box-shadow: 0 0 0px 1000px var(--input-bg) inset !important;
    box-shadow: 0 0 0px 1000px var(--input-bg) inset !important;
    transition: background-color 5000s ease-in-out 0s;
    caret-color: #60a5fa !important;
}

/* ── Placeholder text ── */
::placeholder,
input::placeholder,
textarea::placeholder {
    color: var(--input-placeholder) !important;
    opacity: 1 !important;
    font-weight: 400 !important;
}

/* ══════════════════════════════════════════════════════════
   NUMBER INPUT — aggressive dark override (all DOM layers)
   ══════════════════════════════════════════════════════════ */

/* Layer 1: stNumberInput root + every child div */
.stNumberInput,
.stNumberInput > div,
.stNumberInput > div > div,
.stNumberInput > div > div > div,
.stNumberInput [data-testid="stNumberInput"],
.stNumberInput [data-testid="stNumberInput"] > div,
.stNumberInput [data-testid="stNumberInput"] > div > div {
    background: var(--input-bg) !important;
    background-color: var(--input-bg) !important;
}

/* Layer 2: BaseUI input containers (the culprit for white bg) */
.stNumberInput [data-baseweb="input"],
.stNumberInput [data-baseweb="base-input"],
.stNumberInput [data-baseweb="form-control"],
.stNumberInput [class*="InputContainer"],
.stNumberInput [class*="inputContainer"] {
    background: var(--input-bg) !important;
    background-color: var(--input-bg) !important;
    border: 1px solid var(--input-border) !important;
    border-radius: var(--input-radius) !important;
    box-shadow: var(--input-shadow) !important;
    transition: border-color 0.18s ease, box-shadow 0.18s ease !important;
}
.stNumberInput [data-baseweb="input"]:hover,
.stNumberInput [data-baseweb="base-input"]:hover {
    border-color: var(--input-border-hover) !important;
    background: var(--input-bg-hover) !important;
}
.stNumberInput [data-baseweb="input"]:focus-within,
.stNumberInput [data-baseweb="base-input"]:focus-within {
    border-color: var(--input-border-focus) !important;
    box-shadow: var(--input-glow-focus) !important;
    background: var(--input-bg-focus) !important;
}

/* Layer 3: The actual <input type="number"> element */
.stNumberInput input,
.stNumberInput input[type="number"],
.stNumberInput [data-baseweb="input"] input,
.stNumberInput [data-baseweb="base-input"] input,
[data-testid="stNumberInput"] input,
[data-testid="stNumberInput"] input[type="number"] {
    background: transparent !important;
    background-color: transparent !important;
    color: #e8edf5 !important;
    -webkit-text-fill-color: #e8edf5 !important;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    caret-color: #60a5fa !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    text-align: left !important;
}

/* Layer 4: Spinner +/- buttons */
.stNumberInput button,
.stNumberInput [data-testid="stNumberInputStepDown"],
.stNumberInput [data-testid="stNumberInputStepUp"],
[data-testid="stNumberInput"] button {
    background: rgba(255,255,255,0.06) !important;
    background-color: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    border-radius: 8px !important;
    color: #94a3b8 !important;
    fill: #94a3b8 !important;
    transition: all 0.15s ease !important;
    box-shadow: none !important;
}
.stNumberInput button:hover,
.stNumberInput [data-testid="stNumberInputStepDown"]:hover,
.stNumberInput [data-testid="stNumberInputStepUp"]:hover {
    background: rgba(59,130,246,0.20) !important;
    border-color: rgba(59,130,246,0.40) !important;
    color: #93c5fd !important;
    fill: #93c5fd !important;
}
.stNumberInput button svg,
.stNumberInput [data-testid="stNumberInputStepDown"] svg,
.stNumberInput [data-testid="stNumberInputStepUp"] svg {
    fill: currentColor !important;
    color: inherit !important;
}

/* Layer 5: hide browser default number spinners */
.stNumberInput input[type="number"]::-webkit-inner-spin-button,
.stNumberInput input[type="number"]::-webkit-outer-spin-button,
[data-testid="stNumberInput"] input[type="number"]::-webkit-inner-spin-button,
[data-testid="stNumberInput"] input[type="number"]::-webkit-outer-spin-button {
    -webkit-appearance: none !important;
    margin: 0 !important;
}
.stNumberInput input[type="number"],
[data-testid="stNumberInput"] input[type="number"] {
    -moz-appearance: textfield !important;
}

/* ── Textarea ── */
textarea {
    background: var(--input-bg) !important;
    background-color: var(--input-bg) !important;
    border: 1px solid var(--input-border) !important;
    border-radius: var(--input-radius) !important;
    resize: vertical;
}
textarea:hover { border-color: var(--input-border-hover) !important; }
textarea:focus {
    border-color: var(--input-border-focus) !important;
    box-shadow: var(--input-glow-focus) !important;
    outline: none !important;
}

/* ══════════════════════════════════════════════════════════
   SELECT / DROPDOWN — exhaustive dark override (all layers)
   ══════════════════════════════════════════════════════════ */

/* ── TRIGGER BOX: the closed select control ── */
.stSelectbox > div > div,
.stSelectbox [data-baseweb="select"],
.stSelectbox [data-baseweb="select"] > div,
[data-baseweb="select"],
[data-baseweb="select"] > div {
    background:    var(--input-bg) !important;
    background-color: var(--input-bg) !important;
    border: 1px solid var(--input-border) !important;
    border-radius: var(--input-radius) !important;
    box-shadow:    var(--input-shadow) !important;
    color:         var(--input-text) !important;
    transition: border-color 0.18s ease, box-shadow 0.18s ease, background 0.18s ease !important;
    min-height: 42px !important;
}
.stSelectbox > div > div:hover,
.stSelectbox [data-baseweb="select"] > div:hover,
[data-baseweb="select"] > div:hover {
    background:    var(--input-bg-hover) !important;
    background-color: var(--input-bg-hover) !important;
    border-color:  var(--input-border-hover) !important;
}
.stSelectbox [data-baseweb="select"][aria-expanded="true"] > div,
[data-baseweb="select"][aria-expanded="true"] > div,
[data-baseweb="select"]:focus-within > div {
    border-color:  var(--input-border-focus) !important;
    box-shadow:    var(--input-glow-focus) !important;
    background:    var(--input-bg-focus) !important;
}

/* Every descendant inside the trigger: force light text, no white bg */
[data-baseweb="select"] *,
[data-baseweb="select"] span,
[data-baseweb="select"] p,
[data-baseweb="select"] div:not([data-baseweb="popover"]) {
    color: var(--input-text) !important;
    background: transparent !important;
    background-color: transparent !important;
}

/* Placeholder text inside the trigger */
[data-baseweb="select"] [class*="placeholder"],
[data-baseweb="select"] [aria-placeholder] {
    color: var(--input-placeholder) !important;
}

/* The chevron / arrow icon */
[data-baseweb="select"] svg {
    color: #64748b !important;
    fill:  #64748b !important;
    flex-shrink: 0 !important;
}

/* ── POPOVER PORTAL — the floating panel rendered at body root ── */
/* Targets both the portal wrapper AND every div inside it */
body > div[data-baseweb="popover"],
body > div > div[data-baseweb="popover"],
[data-baseweb="popover"] {
    background: #0c1222 !important;
    background-color: #0c1222 !important;
    border: 1px solid rgba(79,120,190,0.30) !important;
    border-radius: var(--input-radius) !important;
    box-shadow:
        0 20px 60px rgba(0,0,0,0.75),
        0 0 0 1px rgba(59,130,246,0.10),
        inset 0 1px 0 rgba(255,255,255,0.04) !important;
    backdrop-filter: blur(28px) !important;
    -webkit-backdrop-filter: blur(28px) !important;
    overflow: hidden !important;
}

/* Inner wrapper divs inside the popover */
[data-baseweb="popover"] > div,
[data-baseweb="popover"] > div > div {
    background: #0c1222 !important;
    background-color: #0c1222 !important;
    border-radius: var(--input-radius) !important;
}

/* ── MENU / LIST CONTAINER ── */
[data-baseweb="menu"],
ul[data-baseweb="menu"],
div[data-baseweb="menu"],
[role="listbox"],
ul[role="listbox"],
div[role="listbox"] {
    background: #0c1222 !important;
    background-color: #0c1222 !important;
    border-radius: calc(var(--input-radius) - 2px) !important;
    padding: 5px !important;
    margin: 0 !important;
}

/* Every div/li inside the menu — nuke any white bg */
[data-baseweb="menu"] *,
[role="listbox"] * {
    background-color: transparent !important;
}

/* ── OPTION ITEMS ── */
[role="option"],
[data-baseweb="menu"] li,
ul[data-baseweb="menu"] li,
div[data-baseweb="menu"] li {
    background: transparent !important;
    background-color: transparent !important;
    color: #ccd6eb !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    padding: 0.5rem 0.85rem !important;
    border-radius: 8px !important;
    margin: 1px 2px !important;
    cursor: pointer !important;
    transition: background 0.12s ease, color 0.12s ease !important;
    border: none !important;
    outline: none !important;
}

/* Text content inside each option */
[role="option"] *,
[role="option"] span,
[role="option"] div,
[role="option"] p {
    color: #ccd6eb !important;
    background: transparent !important;
    background-color: transparent !important;
}

/* ── HOVER STATE ── */
[role="option"]:hover,
[data-baseweb="menu"] li:hover,
ul[data-baseweb="menu"] li:hover {
    background: rgba(59,130,246,0.16) !important;
    background-color: rgba(59,130,246,0.16) !important;
    color: #93c5fd !important;
}
[role="option"]:hover *,
[role="option"]:hover span,
[role="option"]:hover div {
    color: #93c5fd !important;
}

/* ── SELECTED STATE ── */
[role="option"][aria-selected="true"],
[aria-selected="true"] {
    background: rgba(59,130,246,0.22) !important;
    background-color: rgba(59,130,246,0.22) !important;
    color: #60a5fa !important;
    border-left: 2px solid #3b82f6 !important;
    padding-left: calc(0.85rem - 2px) !important;
}
[aria-selected="true"] *,
[aria-selected="true"] span,
[aria-selected="true"] div {
    color: #60a5fa !important;
}

/* ── KEYBOARD-FOCUSED / HIGHLIGHTED ITEM ── */
[data-highlighted="true"],
[role="option"][data-highlighted="true"],
[data-baseweb="menu"] li:focus,
[role="option"]:focus {
    background: rgba(59,130,246,0.13) !important;
    background-color: rgba(59,130,246,0.13) !important;
    color: #93c5fd !important;
    outline: none !important;
}

/* ── STSELECTBOX full-width wrapper fix ── */
.stSelectbox {
    position: relative;
}
.stSelectbox > div > div > div {
    background: transparent !important;
    background-color: transparent !important;
}

/* ── SCROLLBAR INSIDE DROPDOWN ── */
[data-baseweb="menu"]::-webkit-scrollbar,
[role="listbox"]::-webkit-scrollbar {
    width: 5px !important;
}
[data-baseweb="menu"]::-webkit-scrollbar-track,
[role="listbox"]::-webkit-scrollbar-track {
    background: transparent !important;
}
[data-baseweb="menu"]::-webkit-scrollbar-thumb,
[role="listbox"]::-webkit-scrollbar-thumb {
    background: rgba(99,130,180,0.30) !important;
    border-radius: 4px !important;
}
[data-baseweb="menu"]::-webkit-scrollbar-thumb:hover,
[role="listbox"]::-webkit-scrollbar-thumb:hover {
    background: rgba(99,130,180,0.50) !important;
}

/* ── StSelectbox outer wrapper fix ── */
.stSelectbox label,
.stNumberInput label,
.stTextInput label {
    color: var(--text-secondary) !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.01em !important;
    margin-bottom: 0.3rem !important;
}

/* ── LABELS ── */
label, .stWidgetLabel, [data-testid="stWidgetLabel"] {
    color: var(--text-secondary) !important;
    font-size: 0.82rem !important;
}

/* ── METRICS ── */
div[data-testid="metric-container"] {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: var(--radius-md) !important;
    padding: 0.9rem 1rem !important;
    backdrop-filter: var(--glass-blur) !important;
}
div[data-testid="metric-container"] label {
    color: var(--text-muted) !important;
}
div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    color: var(--text-primary) !important;
}

/* ── ALERTS ── */
div[data-testid="stAlert"] {
    border-radius: var(--radius-md) !important;
    backdrop-filter: blur(8px) !important;
}
div[data-testid="stAlert"][data-baseweb="notification"] {
    background: rgba(251,191,36,0.10) !important;
    border-color: rgba(251,191,36,0.25) !important;
}

/* ── DATAFRAME ── */
.stDataFrame,
[data-testid="stDataFrame"] > div {
    border-radius: var(--radius-md) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    background: rgba(255,255,255,0.04) !important;
}
[data-testid="stDataFrame"] iframe {
    border-radius: var(--radius-md) !important;
}

/* ── EXPANDER ── */
.streamlit-expanderHeader,
[data-testid="stExpander"] summary {
    background: rgba(255,255,255,0.05) !important;
    border-radius: var(--radius-sm) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: var(--text-primary) !important;
    font-weight: 600 !important;
    padding: 0.7rem 1rem !important;
}
[data-testid="stExpander"] summary:hover {
    background: rgba(255,255,255,0.08) !important;
}
[data-testid="stExpander"] > div > div {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-top: none !important;
    border-radius: 0 0 var(--radius-sm) var(--radius-sm) !important;
    padding: 0.8rem 1rem !important;
}

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background: rgba(11,15,28,0.96) !important;
    backdrop-filter: var(--glass-blur) !important;
    border-right: 1px solid rgba(255,255,255,0.08) !important;
}
section[data-testid="stSidebar"] * { color: var(--text-primary); }

/* ── SPINNER ── */
.stSpinner > div { border-top-color: #60a5fa !important; }

/* ── RADIO ── */
.stRadio [data-testid="stWidgetLabel"] { color: var(--text-secondary) !important; }
.stRadio label { color: var(--text-secondary) !important; }
.stRadio div[data-testid="stMarkdownContainer"] p { color: var(--text-secondary) !important; }

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: rgba(255,255,255,0.03); }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.12); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.20); }

/* ── GLOBAL TEXT SAFETY NET ── */
body, p, span, div, label {
    color: #f0f4ff;
}
.kpi-card, .score-display, .section-header, .stMarkdown {
    color: #f0f4ff;
}
.text-muted, .kpi-label { color: #9fb3d9; }
.kpi-value { color: #ffffff; opacity: 1; }
table, th, td { color: #f0f4ff; }

/* force icons inherit color properly */
.icon-svg { display: inline-flex; align-items: center; }
</style>
""", unsafe_allow_html=True)

# ─── SVG Icon Helpers ───────────────────────────────────────
def icon(name: str, size: int = 16, color: str = "currentColor") -> str:
    s = f'width="{size}" height="{size}" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
    icons = {
        "shield":      f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
        "user":        f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
        "briefcase":   f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/></svg>',
        "map-pin":     f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>',
        "search":      f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>',
        "bar-chart":   f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
        "check":       f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><path d="M20 6 9 17l-5-5"/></svg>',
        "alert":       f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><path d="m10.29 3.86-8.8 15.2A1 1 0 0 0 2.35 21h19.3a1 1 0 0 0 .87-1.5L13.72 3.86a2 2 0 0 0-3.43 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
        "zap":         f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
        "clock":       f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
        "database":    f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>',
        "target":      f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
        "cpu":         f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="14" x2="23" y2="14"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="14" x2="4" y2="14"/></svg>',
        "settings":    f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>',
        "refresh":     f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>',
        "eye":         f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>',
        "arrow-up":    f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><line x1="12" y1="19" x2="12" y2="5"/><polyline points="5 12 12 5 19 12"/></svg>',
        "check-circle":f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>',
        "edit":        f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>',
        "activity":    f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>',
        "layers":      f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>',
        "flag":        f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><line x1="4" y1="22" x2="4" y2="15"/></svg>',
        "lightbulb":   f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><line x1="9" y1="18" x2="15" y2="18"/><line x1="10" y1="22" x2="14" y2="22"/><path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .23 2.23 1.5 3.5A4.61 4.61 0 0 1 8.91 14"/></svg>',
        "bookmark":    f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><path d="m19 21-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>',
        "list":        f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>',
        "trending-up": f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>',
        "map":         f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/><line x1="8" y1="2" x2="8" y2="18"/><line x1="16" y1="6" x2="16" y2="22"/></svg>',
        "server":      f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><rect x="2" y="2" width="20" height="8" rx="2" ry="2"/><rect x="2" y="14" width="20" height="8" rx="2" ry="2"/><line x1="6" y1="6" x2="6.01" y2="6"/><line x1="6" y1="18" x2="6.01" y2="18"/></svg>',
        "save":        f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>',
        "inbox":       f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><polyline points="22 12 16 12 14 15 10 15 8 12 2 12"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/></svg>',
        "fire":        f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/></svg>',
        "radar":       f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg>',
        "grid":        f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>',
        "help":        f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
        "info":        f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>',
        "key":         f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><path d="m21 2-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0 3 3L22 7l-3-3m-3.5 3.5L19 4"/></svg>',
        "star":        f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>',
        "health":      f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>',
        "pin":         f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><line x1="12" y1="17" x2="12" y2="22"/><path d="M5 17h14v-1.76a2 2 0 0 0-1.11-1.79l-1.78-.9A2 2 0 0 1 15 10.76V6h1a2 2 0 0 0 0-4H8a2 2 0 0 0 0 4h1v4.76a2 2 0 0 1-1.11 1.79l-1.78.9A2 2 0 0 0 5 15.24Z"/></svg>',
        "table":       f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><path d="M9 3H5a2 2 0 0 0-2 2v4m6-6h10a2 2 0 0 1 2 2v4M9 3v18m0 0h10a2 2 0 0 0 2-2V9M9 21H5a2 2 0 0 1-2-2V9m0 0h18"/></svg>',
        "users":       f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
        "clipboard":   f'<svg xmlns="http://www.w3.org/2000/svg" {s} viewBox="0 0 24 24"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/></svg>',
    }
    return icons.get(name, icons["help"])


# ─── API Helpers ───
def api_get(ep, params=None):
    try:
        r = requests.get(f"{API}{ep}", params=params, timeout=10)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None


def api_post(ep, data):
    try:
        r = requests.post(f"{API}{ep}", json=data, timeout=30)
        return r.json() if r.status_code == 200 else None
    except Exception as e:
        st.error(f"خطأ في الاتصال: {e}")
        return None


# ─── Constants ───
sev_icon  = {
    "high":   icon("alert", 14, "#f87171"),
    "medium": icon("alert", 14, "#fbbf24"),
    "low":    icon("info",  14, "#60a5fa"),
}
sev_class = {"high": "", "medium": "medium", "low": "low"}
field_labels = {
    "age": "العمر", "experience_years": "سنوات الخبرة", "education": "التعليم",
    "job_title": "المسمى الوظيفي", "income": "الدخل", "employment_status": "حالة التوظيف",
}
review_labels = {
    "pending":              "بانتظار المراجعة",
    "reviewed":             "تمت المراجعة",
    "confirmed":            "مؤكد",
    "escalated":            "مُصعّد",
    "correction_requested": "طلب تصحيح",
}
pill_class = {
    "pending": "pill-pending", "reviewed": "pill-reviewed",
    "confirmed": "pill-confirmed", "escalated": "pill-escalated",
    "correction_requested": "pill-correction",
}

# ─── Dark Plotly Defaults ───
CHART_FONT = dict(family="IBM Plex Sans Arabic, Tajawal, sans-serif", color="#94a3b8")
DARK_BG    = "rgba(0,0,0,0)"
DARK_PLOT  = "rgba(255,255,255,0.03)"
CHART_LAYOUT = dict(
    plot_bgcolor=DARK_PLOT,
    paper_bgcolor=DARK_BG,
    font=CHART_FONT,
    margin=dict(l=40, r=40, t=55, b=40),
    hoverlabel=dict(
        bgcolor="#1e293b",
        bordercolor="rgba(255,255,255,0.12)",
        font=dict(family="IBM Plex Sans Arabic, Tajawal", color="#f1f5f9"),
    ),
)
GRID_COLOR = "rgba(255,255,255,0.06)"


# ─── Confidence Gauge (dark theme) ───
def make_gauge(score: float, label_ar: str) -> go.Figure:
    if score >= 75:
        bar_color = "#34d399"
        num_color = "#34d399"
    elif score >= 45:
        bar_color = "#fbbf24"
        num_color = "#fbbf24"
    else:
        bar_color = "#f87171"
        num_color = "#f87171"

    steps_colors = [
        {"range": [0,  45], "color": "rgba(248,113,113,0.18)"},
        {"range": [45, 75], "color": "rgba(251,191,36,0.18)"},
        {"range": [75,100], "color": "rgba(52,211,153,0.18)"},
    ]

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"font": {"size": 44, "family": "IBM Plex Sans Arabic, Tajawal", "color": num_color}},
        title={
            "text": f"<b style='color:#f1f5f9'>درجة الثقة</b>"
                    f"<br><span style='font-size:0.85em;color:#64748b'>{label_ar}</span>",
            "font": {"size": 13, "family": "IBM Plex Sans Arabic, Tajawal"},
        },
        gauge={
            "axis": {
                "range": [0, 100],
                "tickwidth": 1,
                "tickcolor": "rgba(255,255,255,0.15)",
                "tickfont": {"size": 9, "color": "#64748b"},
            },
            "bar":       {"color": bar_color, "thickness": 0.20},
            "bgcolor":   "rgba(0,0,0,0)",
            "borderwidth": 0,
            "steps":     steps_colors,
            "threshold": {
                "line": {"color": bar_color, "width": 2},
                "thickness": 0.75,
                "value": score,
            },
        },
    ))
    fig.update_layout(
        height=235,
        margin=dict(l=20, r=20, t=60, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font=CHART_FONT,
    )
    return fig


# ─── Header ─────────────────────────────────────────────────
root_info = api_get("/")
llm_badge = "وضع القواعد"
llm_badge_icon = icon("layers", 14, "#93c5fd")
if root_info:
    prov = root_info.get("llm_provider", "offline")
    configured = root_info.get("llm_configured", False)
    if prov != "offline" and configured:
        llm_badge = prov
        llm_badge_icon = icon("cpu", 14, "#93c5fd")

st.markdown(f"""
<div class="main-header">
    <div class="header-center">
        <div class="header-icon-wrap">
            {icon("shield", 26, "#60a5fa")}
        </div>
        <div class="header-title">الحارس الدلالي AI – بصير</div>
        <div class="header-subtitle">
            نظام ذكي للكشف عن التناقضات في بيانات الاستبيانات الحكومية
        </div>
        <div class="header-badges">
            <span class="header-badge">
                {llm_badge_icon} {llm_badge}
            </span>
            <span class="header-badge live">
                <span class="live-dot"></span> نظام حي
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════
# LLM Setup
# ═══════════════════════════════════════
def show_llm_settings(location="sidebar"):
    settings = api_get("/llm_settings")
    if not settings:
        return

    if location == "main":
        st.markdown('<div class="setup-box">', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="rtl">
            <h4 style="margin:0 0 0.4rem;color:#f1f5f9;display:flex;align-items:center;gap:0.5rem">
                {icon("settings", 18, "#38bdf8")} إعداد مزود الذكاء الاصطناعي
            </h4>
            <p style="font-size:0.85rem;color:#94a3b8;margin:0">
                لتفعيل التحقق الدلالي المتقدم، أدخل إعدادات مزود الذكاء الاصطناعي أدناه.
            </p>
        </div>""", unsafe_allow_html=True)

    providers_list = ["openai", "anthropic", "gemini", "groq", "offline"]
    current_provider = settings.get("provider", "offline")
    provider_index = providers_list.index(current_provider) if current_provider in providers_list else len(providers_list) - 1
    provider = st.selectbox("المزود", providers_list, index=provider_index, key=f"llm_provider_{location}")

    default_models = {
        "openai": "gpt-4o-mini", "anthropic": "claude-sonnet-4-20250514",
        "gemini": "gemini-1.5-flash", "groq": "llama-3.3-70b-versatile", "offline": "",
    }
    model = st.text_input("اسم النموذج",
                          value=settings.get("model", "") or default_models.get(provider, ""),
                          key=f"llm_model_{location}")
    api_key = st.text_input("مفتاح الوصول", type="password",
                            placeholder="أدخل مفتاح API الخاص بالمزود",
                            key=f"llm_key_{location}")

    if settings.get("is_configured", False):
        st.markdown(
            f'<span class="health-badge health-ok">'
            f'{icon("check-circle", 13, "#6ee7b7")} مُفعّل — {settings.get("api_key_masked","")}'
            f'</span>',
            unsafe_allow_html=True)

    if st.button("حفظ الإعدادات", key=f"save_llm_{location}"):
        if provider == "offline":
            result = api_post("/llm_settings", {"provider": "offline", "api_key": "", "model": ""})
        elif api_key:
            result = api_post("/llm_settings", {"provider": provider, "api_key": api_key, "model": model})
        else:
            st.warning("يرجى إدخال مفتاح الوصول")
            return
        if result and result.get("status") == "ok":
            st.success("تم حفظ الإعدادات بنجاح!")
            st.rerun()
        else:
            st.error("فشل حفظ الإعدادات")

    if location == "main":
        st.markdown('</div>', unsafe_allow_html=True)


llm_settings   = api_get("/llm_settings")
show_first_run = llm_settings and not llm_settings.get("is_configured", False)


# ═══════════════════════════════════════
# Sidebar
# ═══════════════════════════════════════
with st.sidebar:
    st.markdown(
        f'<div class="rtl" style="padding:0.5rem 0">'
        f'<h3 style="color:#f1f5f9;display:flex;align-items:center;gap:0.5rem">'
        f'{icon("settings", 18, "#f1f5f9")} إعدادات النظام'
        f'</h3></div>',
        unsafe_allow_html=True)
    show_llm_settings("sidebar")

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="rtl"><h4 style="color:#f1f5f9;display:flex;align-items:center;gap:0.5rem">'
        f'{icon("health", 16, "#f1f5f9")} صحة النظام'
        f'</h4></div>',
        unsafe_allow_html=True)
    health = api_get("/health")
    if health:
        api_ok = health.get("api_status") == "running"
        llm_on = health.get("llm_enabled", False)
        st.markdown(
            f'<span class="health-badge {"health-ok" if api_ok else "health-off"}">'
            f'{icon("server", 13, "#6ee7b7" if api_ok else "#fca5a5")}'
            f' الخادم: {"يعمل" if api_ok else "متوقف"}</span>',
            unsafe_allow_html=True)
        st.markdown(
            f'<span class="health-badge {"health-ok" if llm_on else "health-warn"}">'
            f'{icon("cpu", 13, "#6ee7b7" if llm_on else "#fde68a")}'
            f' الذكاء: {"مُفعّل" if llm_on else "غير مُفعّل"}</span>',
            unsafe_allow_html=True)
        st.markdown(
            f'<span class="health-badge health-ok">'
            f'{icon("layers", 13, "#6ee7b7")} المزود: {health.get("llm_provider","؟")}</span>',
            unsafe_allow_html=True)

        ls = health.get("llm_stats", {})
        if ls.get("total_calls", 0) > 0:
            st.markdown(f"""
            <div style="font-size:0.77rem;direction:rtl;margin-top:0.7rem;
                        background:rgba(255,255,255,0.05);padding:0.7rem 0.9rem;border-radius:10px;
                        border:1px solid rgba(255,255,255,0.08);line-height:1.9;color:#94a3b8">
            استدعاءات: <b style="color:#f1f5f9">{ls['total_calls']}</b> ·
            ناجحة: <b style="color:#34d399">{ls['successful_calls']}</b><br>
            متوسط: <b style="color:#f1f5f9">{ls['average_latency_ms']}ms</b> ·
            كاش: <b style="color:#a78bfa">{ls['cache_hit_rate']}%</b>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown(
            f'<span class="health-badge health-off">'
            f'{icon("server", 13, "#fca5a5")} الخادم غير متاح</span>',
            unsafe_allow_html=True)


# ═══════════════════════════════════════
# Tabs
# ═══════════════════════════════════════
tab1, tab2, tab3 = st.tabs([
    "  إدخال الاستبيان",
    "  الباحث الميداني",
    "  لوحة الجهة المشرفة",
])


# ═══════════════════════════════════════
# TAB 1 — Survey Entry
# ═══════════════════════════════════════
with tab1:
    if show_first_run:
        show_llm_settings("main")

    st.markdown(f"""<div class="section-header">
        <h3>{icon("clipboard", 18, "#93c5fd")} محاكاة إدخال بيانات الاستبيان</h3>
        <div class="subtitle">أدخل بيانات المشارك للكشف الفوري عن التناقضات الدلالية والمنطقية</div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="demo-tip">
        {icon("info", 16, "#a78bfa")}
        <span><b>نصيحة للعرض:</b> جرّب: عمر <b>22</b> + خبرة <b>15 سنة</b> + دكتوراه + دخل <b>45,000 ريال</b>
        لمشاهدة الكشف الفوري عن التناقضات</span>
    </div>""", unsafe_allow_html=True)

    col_form, col_result = st.columns([1, 1], gap="large")

    with col_form:
        st.markdown(
            f'<div class="form-group-label">{icon("user", 14, "#94a3b8")} البيانات الديموغرافية</div>',
            unsafe_allow_html=True)
        fc1, fc2 = st.columns(2)
        with fc1:
            age        = st.number_input("العمر", 1, 120, 22)
        with fc2:
            experience = st.number_input("سنوات الخبرة", 0, 80, 15)
        education  = st.selectbox("المستوى التعليمي", [
            "High School", "Diploma", "Bachelor", "Master", "PhD",
            "ثانوية", "دبلوم", "بكالوريوس", "ماجستير", "دكتوراه"], index=4)

        st.markdown(
            f'<div class="form-group-label" style="margin-top:1rem">{icon("briefcase", 14, "#94a3b8")} البيانات المهنية</div>',
            unsafe_allow_html=True)
        job_title  = st.text_input("المسمى الوظيفي", "Software Engineer")
        employment = st.selectbox("حالة التوظيف", ["Full-time", "Part-time", "عاطل", "Student", "Self-employed"])

        st.markdown(
            f'<div class="form-group-label" style="margin-top:1rem">{icon("map-pin", 14, "#94a3b8")} الموقع والدخل</div>',
            unsafe_allow_html=True)
        ff1, ff2 = st.columns(2)
        with ff1:
            income = st.number_input("الدخل الشهري (ريال)", 0.0, 500_000.0, 45_000.0, 1000.0, format="%.0f")
        with ff2:
            region = st.selectbox("المنطقة", ["الرياض", "جدة", "الدمام", "مكة", "المدينة", "أبها", "تبوك", "حائل"])

        max_exp = max(0, age - 18)
        if experience > max_exp:
            st.warning(f"تحذير: الخبرة ({experience} سنة) تتجاوز الحد المنطقي للعمر {age}")

        st.markdown("<div style='margin-top:1.2rem'></div>", unsafe_allow_html=True)
        submit = st.button("تحقق من البيانات الآن", type="primary", use_container_width=True)

    with col_result:
        st.markdown(
            f'<div class="rtl" style="font-weight:700;font-size:1rem;margin-bottom:0.6rem;'
            f'color:#f1f5f9;display:flex;align-items:center;gap:0.5rem">'
            f'{icon("bar-chart", 18, "#93c5fd")} نتائج التحقق الفوري</div>',
            unsafe_allow_html=True)

        if submit:
            payload = {"record": {
                "age": age, "experience_years": experience, "education": education,
                "job_title": job_title, "income": income, "region": region,
                "employment_status": employment,
            }}
            with st.spinner("جاري التحقق الدلالي..."):
                result = api_post("/ingest", payload)

            if result:
                score    = result["confidence_score"]
                label_ar = result.get("confidence_label_ar", "")
                reason_ar= result.get("confidence_reason_ar", "")
                n        = result["contradictions_count"]
                detected = result.get("detected_by", "rule")
                llm_tag  = {
                    "rule":   f'{icon("layers", 12, "#94a3b8")} القواعد',
                    "llm":    f'{icon("cpu", 12, "#94a3b8")} الذكاء',
                    "hybrid": f'{icon("activity", 12, "#94a3b8")} هجين',
                }.get(detected, f'{icon("layers", 12, "#94a3b8")} القواعد')
                lat = result.get("latency_ms", 0)

                fig_gauge = make_gauge(score, label_ar)
                st.plotly_chart(fig_gauge, use_container_width=True, config={"displayModeBar": False})

                st.markdown(f"""
                <div class="info-row">
                    <span class="info-chip">{icon("alert", 12, "#94a3b8")} {n} تناقض</span>
                    <span class="info-chip">{llm_tag}</span>
                    <span class="info-chip">{icon("zap", 12, "#94a3b8")} {lat:.0f}ms</span>
                </div>
                <div class="rtl" style="font-size:0.83rem;color:#94a3b8;
                     margin:0.3rem 0 0.8rem;line-height:1.7;
                     background:rgba(255,255,255,0.04);padding:0.6rem 0.9rem;
                     border-radius:10px;border:1px solid rgba(255,255,255,0.07)">
                    {reason_ar}
                </div>""", unsafe_allow_html=True)

                if result["warnings"]:
                    st.markdown(
                        f'<div class="rtl" style="font-weight:700;color:#f1f5f9;margin-top:0.5rem;'
                        f'display:flex;align-items:center;gap:0.4rem">'
                        f'{icon("alert", 16, "#f87171")} التحذيرات</div>',
                        unsafe_allow_html=True)
                    for w in result["warnings"]:
                        sc  = sev_class.get(w["severity"], "")
                        si  = sev_icon.get(w["severity"], icon("help", 14, "#94a3b8"))
                        src_map = {
                            "rules":    f'{icon("layers", 12, "currentColor")} قواعد',
                            "semantic": f'{icon("search", 12, "currentColor")} دلالي',
                            "llm":      f'{icon("cpu", 12, "currentColor")} ذكاء',
                        }
                        src = src_map.get(w.get("source",""), "")
                        st.markdown(f"""<div class="warning-card {sc}">
                            <div class="rtl">{si} {src} {w.get('message_ar', w.get('message_en',''))}
                            </div></div>""", unsafe_allow_html=True)

                if result.get("recommendations"):
                    st.markdown(
                        f'<div class="rtl" style="font-weight:700;color:#f1f5f9;margin-top:0.8rem;'
                        f'display:flex;align-items:center;gap:0.4rem">'
                        f'{icon("lightbulb", 16, "#34d399")} التوصيات</div>',
                        unsafe_allow_html=True)
                    for rec in result["recommendations"]:
                        if "suggestion_ar" in rec:
                            st.markdown(f"""<div class="rec-card"><div class="rtl">
                                <b>{icon("pin", 12, "#34d399")} {rec.get('field','')}:</b> {rec.get('current_value','')} →
                                {rec.get('suggestion_ar', rec.get('suggestion_en',''))}
                            </div></div>""", unsafe_allow_html=True)
                        elif "message_ar" in rec:
                            pri_map = {
                                "high":   icon("alert", 13, "#f87171"),
                                "medium": icon("alert", 13, "#fbbf24"),
                            }
                            pri = pri_map.get(rec.get("priority",""), icon("info", 13, "#60a5fa"))
                            st.markdown(f"""<div class="rec-card system"><div class="rtl">
                                {pri} <b>{rec.get('message_ar','')}</b>
                            </div></div>""", unsafe_allow_html=True)

                if n == 0:
                    st.success("لا توجد تناقضات — البيانات متسقة ومنطقية تماماً")
            else:
                st.error("تعذر الاتصال بالخادم")
        else:
            st.markdown(f"""
            <div class="empty-state">
                <div class="empty-icon">{icon("search", 32, "#64748b")}</div>
                <div class="empty-title">في انتظار البيانات</div>
                <div class="empty-desc">أدخل بيانات المشارك ثم اضغط "تحقق"<br>
                    ستظهر هنا نتائج التحقق مع مؤشر الثقة</div>
            </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════
# TAB 2 — Field Researcher
# ═══════════════════════════════════════
with tab2:
    st.markdown(f"""<div class="section-header">
        <h3>{icon("search", 18, "#93c5fd")} واجهة الباحث الميداني</h3>
        <div class="subtitle">مراجعة الاستجابات التي تتضمن تناقضات واتخاذ الإجراءات المناسبة</div>
    </div>""", unsafe_allow_html=True)

    fr_c1, fr_c2 = st.columns([2, 1])
    with fr_c1:
        filter_status = st.selectbox("تصفية حسب الحالة",
            ["pending", "all", "reviewed", "escalated", "correction_requested"],
            format_func=lambda x: review_labels.get(x, x) if x != "all" else "جميع الحالات",
            key="fr_filter")
    with fr_c2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("تحديث", use_container_width=True, key="fr_refresh")

    fr_data = api_get("/field_researcher", {"status": filter_status, "limit": 50})

    if fr_data and fr_data["responses"]:
        st.markdown(
            f'<div class="rtl" style="margin-bottom:0.7rem;font-size:0.9rem;color:#94a3b8">'
            f'<b style="color:#f1f5f9">{icon("list", 14, "#f1f5f9")} {fr_data["total"]} سجل</b> — '
            f'{review_labels.get(filter_status, filter_status)}</div>',
            unsafe_allow_html=True)

        for resp in fr_data["responses"]:
            score    = resp["confidence_score"]
            detected = resp.get("detected_by", "rule")
            det_lbl  = {
                "rule":   f'{icon("layers", 13, "#94a3b8")} قواعد',
                "llm":    f'{icon("cpu", 13, "#94a3b8")} ذكاء',
                "hybrid": f'{icon("activity", 13, "#94a3b8")} هجين',
            }.get(detected, f'{icon("layers", 13, "#94a3b8")} قواعد')
            rs       = resp.get("review_status", "pending")
            rs_pill  = pill_class.get(rs, "pill-pending")
            sc_cls   = "high" if score >= 75 else ("medium" if score >= 45 else "low")

            with st.expander(f"سجل #{resp['id']}  ·  ثقة: {score}"):
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;align-items:center;
                            direction:rtl;margin-bottom:0.9rem">
                    <span class="score-badge {sc_cls}">{icon("target", 13, "currentColor")} {score}</span>
                    <span class="status-pill {rs_pill}">{review_labels.get(rs, rs)}</span>
                </div>""", unsafe_allow_html=True)

                mc1, mc2, mc3, mc4 = st.columns(4)
                mc1.metric("العمر",   resp["age"])
                mc2.metric("الخبرة",  resp["experience_years"])
                mc3.metric("الدخل",   f"{resp['income']:,.0f}")
                mc4.metric("المنطقة", resp["region"])

                st.markdown(f"""
                <div class="info-row">
                    <span class="info-chip">{icon("briefcase", 12, "#94a3b8")} {resp['job_title']}</span>
                    <span class="info-chip">{icon("bookmark", 12, "#94a3b8")} {resp['education']}</span>
                    <span class="info-chip">{icon("clipboard", 12, "#94a3b8")} {resp['employment_status']}</span>
                    <span class="info-chip">{icon("user", 12, "#94a3b8")} {resp.get('enumerator_id','default')}</span>
                </div>""", unsafe_allow_html=True)

                if resp.get("confidence_reason_ar"):
                    st.markdown(
                        f'<div class="rtl" style="font-size:0.83rem;color:#94a3b8;margin:0.5rem 0;'
                        f'background:rgba(255,255,255,0.04);padding:0.55rem 0.9rem;border-radius:9px;'
                        f'border:1px solid rgba(255,255,255,0.07)">{resp["confidence_reason_ar"]}</div>',
                        unsafe_allow_html=True)

                for w in resp.get("warnings", []):
                    sc = sev_class.get(w.get("severity",""), "")
                    si = sev_icon.get(w.get("severity",""), icon("info", 14, "#94a3b8"))
                    st.markdown(
                        f'<div class="warning-card {sc}"><div class="rtl">'
                        f'{si} {w.get("message_ar", w.get("message_en",""))}'
                        f'</div></div>', unsafe_allow_html=True)

                st.markdown(
                    f'<div class="rtl" style="margin:0.9rem 0 0.3rem;font-weight:700;color:#f1f5f9;'
                    f'display:flex;align-items:center;gap:0.4rem">'
                    f'{icon("zap", 15, "#f1f5f9")} الإجراءات</div>',
                    unsafe_allow_html=True)
                ac1, ac2, ac3, ac4 = st.columns(4)
                with ac1:
                    if st.button("مراجعة", key=f"review_{resp['id']}", use_container_width=True):
                        api_post("/review", {"response_id": resp["id"], "status": "reviewed"})
                        st.rerun()
                with ac2:
                    if st.button("تأكيد", key=f"confirm_{resp['id']}", use_container_width=True):
                        api_post("/review", {"response_id": resp["id"], "status": "confirmed"})
                        st.rerun()
                with ac3:
                    if st.button("تصحيح", key=f"correct_{resp['id']}", use_container_width=True):
                        api_post("/review", {"response_id": resp["id"], "status": "correction_requested"})
                        st.rerun()
                with ac4:
                    if st.button("تصعيد", key=f"escalate_{resp['id']}", use_container_width=True):
                        api_post("/review", {"response_id": resp["id"], "status": "escalated"})
                        st.rerun()
    else:
        st.markdown(f"""
        <div class="empty-state">
            <div class="empty-icon">{icon("check-circle", 32, "#64748b")}</div>
            <div class="empty-title">لا توجد سجلات تحتاج مراجعة</div>
            <div class="empty-desc">شغّل: <code>python scripts/ingest_dataset.py</code></div>
        </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════
# TAB 3 — Authority Dashboard
# ═══════════════════════════════════════
with tab3:
    stats = api_get("/stats")
    if not stats:
        st.markdown(f"""
        <div class="empty-state">
            <div class="empty-icon">{icon("bar-chart", 32, "#64748b")}</div>
            <div class="empty-title">لا توجد بيانات بعد</div>
            <div class="empty-desc">شغّل: <code>python scripts/ingest_dataset.py</code></div>
        </div>""", unsafe_allow_html=True)
        st.stop()

    # ── KPIs ──
    st.markdown(f"""<div class="section-header">
        <h3>{icon("bar-chart", 18, "#93c5fd")} مؤشرات جودة البيانات الرئيسية</h3>
        <div class="subtitle">نظرة شاملة على حالة جودة البيانات في الوقت الفعلي</div>
    </div>""", unsafe_allow_html=True)

    total   = stats["total_responses"]
    quality = stats["quality_percentage"]
    avg_sc  = stats["average_confidence_score"]
    contra  = stats["total_contradictions"]
    latency = stats["average_latency_ms"]
    pending = stats.get("review_status", {}).get("pending", 0)

    def kpi(col, ico_name, ico_color, label, value, color, bar_pct=None, sub=""):
        bar = ""
        if bar_pct is not None:
            bar = (f'<div class="kpi-bar"><div class="kpi-bar-fill" '
                   f'style="width:{min(bar_pct,100):.0f}%;background:{color}"></div></div>')
        col.markdown(
            f'<div class="kpi-card">'
            f'<div class="kpi-icon">{icon(ico_name, 22, ico_color)}</div>'
            f'<div class="kpi-label">{label}</div>'
            f'<div class="kpi-value" style="color:{color}">{value}</div>'
            f'{f"<div class=kpi-sub>{sub}</div>" if sub else ""}'
            f'{bar}</div>',
            unsafe_allow_html=True)

    k1,k2,k3,k4,k5,k6 = st.columns(6)
    kpi(k1, "database",    "#60a5fa", "إجمالي السجلات",   total,          "#60a5fa",  min(total/10,100))
    kpi(k2, "check-circle","#34d399", "نسبة الجودة",      f"{quality}%",  "#34d399",  quality)
    kpi(k3, "target",      "#38bdf8", "متوسط الثقة",      avg_sc,         "#38bdf8",  avg_sc)
    kpi(k4, "alert",       "#f87171", "إجمالي التناقضات", contra,         "#f87171",  min(contra/5,100))
    kpi(k5, "zap",         "#a78bfa", "متوسط الزمن",      f"{latency}ms", "#a78bfa",  sub="لكل سجل")
    kpi(k6, "clock",       "#fbbf24", "بانتظار المراجعة",  pending,        "#fbbf24",  min(pending*10,100))

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts Row ──
    cc1, cc2 = st.columns(2)

    with cc1:
        dist    = stats["confidence_distribution"]
        fig_bar = go.Figure(data=[go.Bar(
            x=["ثقة عالية", "ثقة متوسطة", "ثقة منخفضة"],
            y=[dist["high"], dist["medium"], dist["low"]],
            marker=dict(
                color=["#34d399", "#fbbf24", "#f87171"],
                line=dict(color="rgba(255,255,255,0.08)", width=1),
            ),
            text=[dist["high"], dist["medium"], dist["low"]],
            textposition="outside",
            textfont=dict(size=14, color="#f1f5f9"),
            width=0.52,
        )])
        fig_bar.update_layout(
            **CHART_LAYOUT,
            title=dict(text="توزيع درجات الثقة",
                       font=dict(size=13, color="#f1f5f9"), x=0),
            height=300,
            showlegend=False,
            yaxis=dict(title="عدد السجلات", gridcolor=GRID_COLOR,
                       color="#64748b", tickcolor="#64748b"),
            xaxis=dict(tickfont=dict(size=12, color="#94a3b8"), tickcolor="#64748b"),
        )
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

    with cc2:
        det_dist = stats.get("detection_distribution", {})
        if any(det_dist.values()):
            fig_pie = go.Figure(data=[go.Pie(
                labels=["القواعد فقط", "الذكاء فقط", "هجين"],
                values=[det_dist.get("rule",0), det_dist.get("llm",0), det_dist.get("hybrid",0)],
                marker=dict(
                    colors=["#3b82f6","#a78bfa","#38bdf8"],
                    line=dict(color="rgba(0,0,0,0.30)", width=2),
                ),
                textfont=dict(size=12, color="#f1f5f9"),
                hole=0.52,
                pull=[0.03,0.03,0.03],
            )])
            fig_pie.update_layout(
                **CHART_LAYOUT,
                title=dict(text="مصدر الكشف",
                           font=dict(size=13, color="#f1f5f9"), x=0),
                height=300,
                legend=dict(font=dict(color="#94a3b8", size=11),
                            orientation="h", yanchor="bottom", y=-0.25),
            )
            st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})

    # ── Top Questions + Radar ──
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    tq_col, radar_col = st.columns(2)

    tq = stats.get("top_questions_table", [])

    with tq_col:
        st.markdown(f"""<div class="section-header">
            <h3>{icon("fire", 18, "#f87171")} أكثر الأسئلة تسبباً في الأخطاء</h3>
        </div>""", unsafe_allow_html=True)
        if tq:
            df_tq = pd.DataFrame(tq)
            df_tq["field_ar"] = df_tq["field"].map(lambda x: field_labels.get(x, x))
            st.dataframe(
                df_tq[["field_ar","severity","count"]].rename(
                    columns={"field_ar":"السؤال","severity":"الشدة","count":"عدد الأخطاء"}),
                use_container_width=True, height=250, hide_index=True)
        else:
            st.info("لا توجد بيانات كافية")

    with radar_col:
        st.markdown(f"""<div class="section-header">
            <h3>{icon("radar", 18, "#60a5fa")} تحليل توزيع الأخطاء</h3>
        </div>""", unsafe_allow_html=True)
        if tq:
            df_r = pd.DataFrame(tq)
            df_r["field_ar"] = df_r["field"].map(lambda x: field_labels.get(x, x))
            ft = df_r.groupby("field_ar")["count"].sum().reset_index()
            cats   = ft["field_ar"].tolist()
            values = ft["count"].tolist()
            cats_c   = cats   + [cats[0]]
            values_c = values + [values[0]]
            fig_radar = go.Figure(data=go.Scatterpolar(
                r=values_c, theta=cats_c,
                fill="toself",
                fillcolor="rgba(59,130,246,0.12)",
                line=dict(color="#60a5fa", width=2),
                marker=dict(color="#60a5fa", size=6),
            ))
            fig_radar.update_layout(
                **CHART_LAYOUT,
                height=280,
                polar=dict(
                    bgcolor="rgba(255,255,255,0.03)",
                    radialaxis=dict(visible=True, color="#334155",
                                   tickfont=dict(size=9, color="#64748b"),
                                   gridcolor=GRID_COLOR),
                    angularaxis=dict(tickfont=dict(size=10, color="#94a3b8"),
                                     gridcolor=GRID_COLOR),
                ),
                showlegend=False,
            )
            st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})

    # ── Heatmap ──
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown(f"""<div class="section-header">
        <h3>{icon("map", 18, "#38bdf8")} الخريطة الحرارية الاستراتيجية — كثافة الأخطاء</h3>
        <div class="subtitle">تكشف أين تتركز التناقضات لتحسين صياغة الأسئلة وتدريب الباحثين</div>
    </div>""", unsafe_allow_html=True)

    hm_r1, hm_r2 = st.columns(2)
    with hm_r1:
        hm_metric = st.radio("المقياس", ["العدد (Count)", "النسبة % (Conflict Rate)",
            "متوسط الثقة (Avg Confidence)", "معدل اختلاف الذكاء (LLM Disagreement)"],
            horizontal=True, key="hm_metric")
    with hm_r2:
        hm_axis = st.radio("المحور", ["المنطقة (Region)", "الباحث (Enumerator)"],
                           horizontal=True, key="hm_axis")

    metric_map = {
        "العدد (Count)": "count",
        "النسبة % (Conflict Rate)": "percentage",
        "متوسط الثقة (Avg Confidence)": "avg_confidence",
        "معدل اختلاف الذكاء (LLM Disagreement)": "llm_disagreement",
    }
    axis_map = {"المنطقة (Region)": "region", "الباحث (Enumerator)": "enumerator"}
    mp = metric_map.get(hm_metric, "count")
    ax = axis_map.get(hm_axis, "region")

    hm = api_get("/heatmap", {"metric": mp, "axis": ax})

    if hm and hm.get("regions"):
        regions  = hm["regions"]
        fields   = hm["fields"]
        fl       = hm["field_labels"]
        matrix   = hm["matrix"]
        annots   = hm["annotations"]
        y_labels = [fl.get(f, f) for f in fields]

        if mp == "avg_confidence":
            cscale = [[0,"#7f1d1d"],[0.3,"#991b1b"],[0.5,"#b45309"],
                      [0.7,"#065f46"],[1,"#34d399"]]
        elif mp == "llm_disagreement":
            cscale = [[0,"rgba(52,211,153,0.1)"],[0.4,"#fbbf24"],
                      [0.7,"#f87171"],[1,"#dc2626"]]
        else:
            cscale = [[0,"rgba(59,130,246,0.05)"],[0.2,"rgba(59,130,246,0.20)"],
                      [0.4,"rgba(59,130,246,0.40)"],[0.6,"#2563eb"],
                      [0.8,"#1d4ed8"],[1,"#1e3a8a"]]

        fig_hm = go.Figure(data=go.Heatmap(
            z=matrix, x=regions, y=y_labels,
            text=[[annots[i][j] for j in range(len(regions))] for i in range(len(fields))],
            texttemplate="%{text}",
            textfont=dict(size=12, color="#f1f5f9"),
            colorscale=cscale,
            colorbar=dict(
                title=dict(text="كثافة", font=dict(color="#94a3b8", size=11)),
                thickness=14, len=0.8,
                tickfont=dict(color="#94a3b8"),
                bgcolor="rgba(0,0,0,0)",
                bordercolor="rgba(255,255,255,0.08)",
            ),
            hovertemplate="<b>%{x}</b><br>%{y}<br>القيمة: %{text}<extra></extra>",
        ))

        tqi = fields.index(hm["top_question"]) if hm["top_question"] in fields else None
        tri = regions.index(hm["top_region"])  if hm["top_region"]   in regions else None
        if tqi is not None and tri is not None:
            fig_hm.add_annotation(x=regions[tri], y=y_labels[tqi], text="★",
                                  showarrow=False, font=dict(size=16, color="#fbbf24"))

        axis_title = hm.get("axis_label", "المنطقة")
        fig_hm.update_layout(
            **CHART_LAYOUT,
            title=dict(text=f"كثافة الأخطاء — {hm_metric}",
                       font=dict(size=13, color="#f1f5f9"), x=0.5),
            xaxis=dict(title=axis_title,
                       tickfont=dict(size=11, color="#94a3b8"),
                       color="#64748b"),
            yaxis=dict(title="الحقل", tickfont=dict(size=11, color="#94a3b8"),
                       color="#64748b", autorange="reversed"),
            height=440,
        )
        st.plotly_chart(fig_hm, use_container_width=True, config={"displayModeBar": False})

        # Heatmap KPIs
        hk1, hk2, hk3 = st.columns(3)
        hk1.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">{icon("fire", 22, "#f87171")}</div>
            <div class="kpi-label">أكثر سؤال تسبباً في الأخطاء</div>
            <div style="font-size:0.95rem;font-weight:700;color:#60a5fa;margin:0.35rem 0;direction:rtl">
                {hm["top_question_label"]}</div>
            <div class="kpi-label">{hm["top_question_errors"]} خطأ</div>
        </div>""", unsafe_allow_html=True)
        hk2.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">{icon("map-pin", 22, "#60a5fa")}</div>
            <div class="kpi-label">أكثر {axis_title} تركيزاً للأخطاء</div>
            <div style="font-size:0.95rem;font-weight:700;color:#60a5fa;margin:0.35rem 0;direction:rtl">
                {hm["top_region"]}</div>
            <div class="kpi-label">{hm["top_region_errors"]} خطأ</div>
        </div>""", unsafe_allow_html=True)
        nz  = sum(1 for row in matrix for v in row if v > 0)
        tc  = len(regions) * len(fields)
        cov = round((nz / max(tc,1)) * 100, 1)
        hk3.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">{icon("grid", 22, "#60a5fa")}</div>
            <div class="kpi-label">تغطية الأخطاء</div>
            <div style="font-size:0.95rem;font-weight:700;color:#60a5fa;margin:0.35rem 0">{cov}%</div>
            <div class="kpi-label">{nz}/{tc} خلية</div>
            <div class="kpi-bar"><div class="kpi-bar-fill" style="width:{cov}%;background:#3b82f6"></div></div>
        </div>""", unsafe_allow_html=True)

        # ── Cell Detail ──
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""<div class="section-header">
            <h3>{icon("search", 18, "#93c5fd")} تفاصيل خلية محددة</h3>
        </div>""", unsafe_allow_html=True)
        dc1, dc2, dc3 = st.columns([2,2,1])
        with dc1:
            sel_field  = st.selectbox("الحقل", fields, format_func=lambda x: fl.get(x,x), key="cd_field")
        with dc2:
            sel_region = st.selectbox(axis_title, regions, key="cd_region")
        with dc3:
            st.markdown("<br>", unsafe_allow_html=True)
            show_detail = st.button("عرض", key="cell_btn", use_container_width=True)

        if show_detail:
            detail = api_get("/cell_detail", {"field": sel_field, "region": sel_region, "axis": ax})
            if detail:
                rate  = detail.get("conflict_rate_pct", 0)
                avg_c = detail.get("average_confidence", 0)
                rc    = "#f87171" if rate > 30 else ("#fbbf24" if rate > 10 else "#34d399")
                st.markdown(f"""
                <div class="detail-panel">
                    <h4 style="margin:0 0 0.7rem;color:#f1f5f9">{fl.get(sel_field,sel_field)} — {sel_region}</h4>
                    <div class="info-row">
                        <span class="info-chip">{icon("alert", 12, "#94a3b8")} أخطاء: {detail['error_count']}</span>
                        <span class="info-chip" style="color:{rc}">نسبة التعارض: {rate}%</span>
                        <span class="info-chip">{icon("target", 12, "#94a3b8")} متوسط الثقة: {avg_c}</span>
                    </div>
                """, unsafe_allow_html=True)
                top_rules = detail.get("top_rules", [])
                if top_rules:
                    rules_str = " · ".join([f"{r['rule']} ({r['count']})" for r in top_rules[:3]])
                    st.markdown(
                        f'<p style="color:#94a3b8;font-size:0.87rem;direction:rtl;margin-top:0.6rem">'
                        f'<b style="color:#f1f5f9">أكثر القواعد انتهاكاً:</b> {rules_str}</p>',
                        unsafe_allow_html=True)
                llm_exps = detail.get("llm_explanations", [])
                if llm_exps:
                    st.markdown(
                        f'<p style="color:#94a3b8;font-size:0.87rem;direction:rtl">'
                        f'<b style="color:#f1f5f9">تفسير الذكاء:</b> {llm_exps[0]}</p>',
                        unsafe_allow_html=True)
                st.markdown(
                    f'<p style="color:#94a3b8;font-size:0.87rem;direction:rtl">'
                    f'<b style="color:#f1f5f9">التوصية:</b> {detail.get("recommendation_ar","")}</p>'
                    f'</div>', unsafe_allow_html=True)
                if detail.get("examples"):
                    st.markdown(
                        f'<div class="section-header"><h3>{icon("table", 16, "#93c5fd")} أمثلة من السجلات</h3></div>',
                        unsafe_allow_html=True)
                    st.dataframe(pd.DataFrame(detail["examples"]),
                                 use_container_width=True, height=200, hide_index=True)
            else:
                st.info("لا توجد بيانات لهذه الخلية")

        # ── Region Bar ──
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            f'<div class="section-header"><h3>{icon("bar-chart", 18, "#93c5fd")} توزيع الأخطاء حسب {axis_title}</h3></div>',
            unsafe_allow_html=True)
        reg_err = {regions[j]: sum(matrix[i][j] for i in range(len(fields))) for j in range(len(regions))}
        s_reg   = dict(sorted(reg_err.items(), key=lambda x: -x[1]))
        fig_r   = go.Figure(data=[go.Bar(
            x=list(s_reg.keys()), y=list(s_reg.values()),
            marker=dict(color=list(s_reg.values()),
                        colorscale=[[0,"#1e3a8a"],[0.5,"#2563eb"],[1,"#60a5fa"]],
                        line=dict(color="rgba(255,255,255,0.06)", width=1)),
            text=list(s_reg.values()),
            textposition="outside",
            textfont=dict(size=13, color="#f1f5f9"),
            width=0.6,
        )])
        fig_r.update_layout(
            **CHART_LAYOUT, height=300, showlegend=False,
            yaxis=dict(title="عدد الأخطاء", gridcolor=GRID_COLOR, color="#64748b"),
            xaxis=dict(tickfont=dict(size=12, color="#94a3b8")),
        )
        st.plotly_chart(fig_r, use_container_width=True, config={"displayModeBar": False})
    else:
        st.warning("لا توجد بيانات كافية. شغّل: python scripts/ingest_dataset.py")

    # ── Recommendations ──
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown(f"""<div class="section-header">
        <h3>{icon("lightbulb", 18, "#34d399")} التوصيات المجمّعة الاستراتيجية</h3>
        <div class="subtitle">مبنية على تحليل أنماط الأخطاء عبر جميع السجلات</div>
    </div>""", unsafe_allow_html=True)

    recs_data = api_get("/recommendations")
    if recs_data and recs_data.get("recommendations"):
        type_labels = {
            "question_rephrase":   "إعادة صياغة سؤال",
            "field_review":        "مراجعة حقل",
            "researcher_training": "تدريب الباحثين",
            "enumerator_review":   "مراجعة أداء الباحث",
        }
        for rec in recs_data["recommendations"]:
            pri_map = {
                "high":   icon("flag", 14, "#f87171"),
                "medium": icon("flag", 14, "#fbbf24"),
            }
            pri  = pri_map.get(rec.get("priority",""), icon("flag", 14, "#60a5fa"))
            tlbl = type_labels.get(rec.get("type",""), "توصية")
            ec   = rec.get("error_count","")
            st.markdown(f"""
            <div class="rec-card system">
                <div class="rtl">
                    {pri} <b>[{tlbl}]</b> {rec.get('message_ar','')}
                    <span style="font-size:0.76rem;color:#6b7280">{"  (" + str(ec) + " خطأ)" if ec else ""}</span>
                </div>
            </div>""", unsafe_allow_html=True)
    else:
        st.success("لا توجد توصيات حالياً — جودة البيانات ممتازة")

    # ── Researcher Performance ──
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="section-header"><h3>{icon("users", 18, "#a78bfa")} أداء الباحثين الميدانيين</h3></div>',
        unsafe_allow_html=True)
    hm_enum = api_get("/heatmap", {"metric": "count", "axis": "enumerator"})
    if hm_enum and hm_enum.get("regions"):
        enums = hm_enum["regions"]
        enum_totals = {
            enums[j]: sum(hm_enum["matrix"][i][j] for i in range(len(hm_enum["fields"])))
            for j in range(len(enums))
        }
        s_enum = dict(sorted(enum_totals.items(), key=lambda x: -x[1]))
        fig_enum = go.Figure(data=[go.Bar(
            x=list(s_enum.keys()), y=list(s_enum.values()),
            marker_color="#a78bfa",
            text=list(s_enum.values()),
            textposition="outside",
            textfont=dict(size=12, color="#f1f5f9"),
            width=0.5,
        )])
        fig_enum.update_layout(
            **CHART_LAYOUT, height=260, showlegend=False,
            yaxis=dict(title="عدد الأخطاء", gridcolor=GRID_COLOR, color="#64748b"),
            xaxis=dict(tickfont=dict(size=11, color="#94a3b8")),
        )
        st.plotly_chart(fig_enum, use_container_width=True, config={"displayModeBar": False})
        df_enum = pd.DataFrame([{"الباحث": k, "عدد الأخطاء": v} for k, v in s_enum.items()])
        st.dataframe(df_enum, use_container_width=True, height=180, hide_index=True)

    # ── System Health ──
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="section-header"><h3>{icon("health", 18, "#34d399")} مراقبة صحة النظام</h3></div>',
        unsafe_allow_html=True)
    health = api_get("/health")
    if health:
        hs1,hs2,hs3,hs4,hs5 = st.columns(5)
        ls = health.get("llm_stats", {})

        ok_cls  = "health-ok"  if health.get("api_status") == "running" else "health-off"
        ok_txt  = "يعمل"       if health.get("api_status") == "running" else "متوقف"
        ok_ico  = icon("check-circle", 14, "#6ee7b7") if health.get("api_status") == "running" else icon("alert", 14, "#fca5a5")
        llm_cls = "health-ok"  if health.get("llm_enabled") else "health-warn"
        llm_txt = "مُفعّل"     if health.get("llm_enabled") else "غير مُفعّل"
        llm_ico = icon("check-circle", 14, "#6ee7b7") if health.get("llm_enabled") else icon("clock", 14, "#fde68a")

        for col, ico_h, lbl, badge_c, badge_t, badge_ico in [
            (hs1, icon("server", 22, "#60a5fa"), "حالة الخادم",      ok_cls,  ok_txt,  ok_ico),
            (hs2, icon("cpu",    22, "#a78bfa"), "الذكاء الاصطناعي", llm_cls, llm_txt, llm_ico),
        ]:
            col.markdown(
                f'<div class="kpi-card"><div class="kpi-icon">{ico_h}</div>'
                f'<div class="kpi-label">{lbl}</div>'
                f'<span class="health-badge {badge_c}">{badge_ico} {badge_t}</span></div>',
                unsafe_allow_html=True)

        for col, ico_name, ico_clr, lbl, val, clr in [
            (hs3, "inbox",    "#a78bfa", "استدعاءات",         ls.get("total_calls",0),        "#a78bfa"),
            (hs4, "zap",      "#a78bfa", "متوسط زمن الذكاء",  f"{ls.get('average_latency_ms',0)}ms","#a78bfa"),
            (hs5, "database", "#38bdf8", "نسبة الكاش",        f"{ls.get('cache_hit_rate',0)}%","#38bdf8"),
        ]:
            col.markdown(
                f'<div class="kpi-card"><div class="kpi-icon">{icon(ico_name, 22, ico_clr)}</div>'
                f'<div class="kpi-label">{lbl}</div>'
                f'<div class="kpi-value" style="color:{clr};font-size:1.4rem">{val}</div></div>',
                unsafe_allow_html=True)

    # ── Latest Responses ──
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="section-header"><h3>{icon("table", 18, "#93c5fd")} آخر الاستجابات المسجّلة</h3></div>',
        unsafe_allow_html=True)
    resp_data = api_get("/responses", {"limit": 30})
    if resp_data and resp_data.get("responses"):
        df = pd.DataFrame(resp_data["responses"])
        cols = ["id","age","experience_years","education","job_title","income",
                "region","confidence_score","contradictions_count","detected_by",
                "review_status","llm_used","latency_ms"]
        avail = [c for c in cols if c in df.columns]
        rename = {
            "id":"#","age":"العمر","experience_years":"الخبرة",
            "education":"التعليم","job_title":"الوظيفة","income":"الدخل",
            "region":"المنطقة","confidence_score":"الثقة",
            "contradictions_count":"التناقضات","detected_by":"المصدر",
            "review_status":"الحالة","llm_used":"ذكاء","latency_ms":"الزمن (ms)",
        }
        st.dataframe(df[avail].rename(columns=rename),
                     use_container_width=True, height=300, hide_index=True)
    else:
        st.markdown(f"""
        <div class="empty-state">
            <div class="empty-icon">{icon("inbox", 32, "#64748b")}</div>
            <div class="empty-title">لا توجد استجابات بعد</div>
            <div class="empty-desc">شغّل البرنامج لبدء جمع البيانات</div>
        </div>""", unsafe_allow_html=True)
