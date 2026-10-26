"""
styles.py — Premium CSS design system for the Multimodal Construction Intelligence Platform.
All visual tokens, animations, metric cards, status pills, and layout utilities.
"""


def get_main_css() -> str:
    """Return the complete CSS stylesheet as a string."""
    return """
<style>
/* ─────────── Google Fonts ─────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ─────────── Root Design Tokens ─────────── */
:root {
    --bg-primary:    #0E1117;
    --bg-card:       #161B22;
    --bg-card-hover: #1C2230;
    --bg-glass:      rgba(22, 27, 34, 0.72);
    --border-subtle: rgba(255, 255, 255, 0.06);
    --border-glow:   rgba(255, 107, 53, 0.3);
    --accent:        #FF6B35;
    --accent-light:  #FF8F66;
    --accent-dim:    rgba(255, 107, 53, 0.12);
    --teal:          #2DD4BF;
    --teal-dim:      rgba(45, 212, 191, 0.12);
    --blue:          #60A5FA;
    --blue-dim:      rgba(96, 165, 250, 0.12);
    --purple:        #A78BFA;
    --purple-dim:    rgba(167, 139, 250, 0.12);
    --green:         #34D399;
    --green-dim:     rgba(52, 211, 153, 0.12);
    --yellow:        #FBBF24;
    --yellow-dim:    rgba(251, 191, 36, 0.12);
    --red:           #F87171;
    --red-dim:       rgba(248, 113, 113, 0.12);
    --text-primary:  #F0F6FC;
    --text-secondary:#8B949E;
    --text-muted:    #6E7681;
    --radius-sm:     8px;
    --radius-md:     12px;
    --radius-lg:     16px;
    --radius-xl:     20px;
    --shadow-card:   0 4px 24px rgba(0,0,0,0.35);
    --shadow-glow:   0 0 20px rgba(255,107,53,0.15);
    --transition:    all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ─────────── Global Resets ─────────── */
html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}
.stApp { background: var(--bg-primary); }

/* ─────────── Sidebar ─────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #12161C 0%, #0D1117 100%) !important;
    border-right: 1px solid var(--border-subtle);
}
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: var(--accent) !important;
}

/* ─────────── Tab Styling ─────────── */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: var(--bg-card);
    border-radius: var(--radius-lg);
    padding: 4px;
    border: 1px solid var(--border-subtle);
}
.stTabs [data-baseweb="tab"] {
    border-radius: var(--radius-md);
    padding: 10px 20px;
    font-weight: 600;
    font-size: 0.85rem;
    letter-spacing: 0.02em;
    color: var(--text-secondary);
    transition: var(--transition);
}
.stTabs [data-baseweb="tab"]:hover { color: var(--text-primary); background: var(--bg-card-hover); }
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, var(--accent) 0%, #E85D2B 100%) !important;
    color: #fff !important;
    box-shadow: 0 4px 16px rgba(255,107,53,0.35);
}
.stTabs [data-baseweb="tab-highlight"] { display: none; }
.stTabs [data-baseweb="tab-border"] { display: none; }

/* ─────────── Metric Card ─────────── */
.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 24px;
    text-align: center;
    transition: var(--transition);
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--accent), var(--teal));
    opacity: 0;
    transition: var(--transition);
}
.metric-card:hover { border-color: var(--border-glow); transform: translateY(-2px); box-shadow: var(--shadow-glow); }
.metric-card:hover::before { opacity: 1; }
.metric-card .metric-icon { font-size: 2rem; margin-bottom: 8px; }
.metric-card .metric-value {
    font-size: 2.2rem; font-weight: 800;
    background: linear-gradient(135deg, var(--accent), var(--teal));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    line-height: 1.1; margin-bottom: 4px;
}
.metric-card .metric-label { font-size: 0.82rem; color: var(--text-secondary); font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; }

/* ─────────── Status Pills ─────────── */
.pill { display: inline-block; padding: 6px 16px; border-radius: 100px; font-weight: 600; font-size: 0.78rem; letter-spacing: 0.04em; text-transform: uppercase; }
.pill-safe   { background: var(--green-dim);  color: var(--green);  border: 1px solid rgba(52,211,153,0.25); }
.pill-warn   { background: var(--yellow-dim); color: var(--yellow); border: 1px solid rgba(251,191,36,0.25); }
.pill-danger { background: var(--red-dim);    color: var(--red);    border: 1px solid rgba(248,113,113,0.25); }
.pill-info   { background: var(--blue-dim);   color: var(--blue);   border: 1px solid rgba(96,165,250,0.25); }
.pill-purple { background: var(--purple-dim); color: var(--purple); border: 1px solid rgba(167,139,250,0.25); }

/* ─────────── Severity Badges ─────────── */
.severity-low      { background: var(--green-dim);  color: var(--green);  padding: 3px 10px; border-radius: 6px; font-weight: 600; font-size: 0.75rem; }
.severity-medium   { background: var(--yellow-dim); color: var(--yellow); padding: 3px 10px; border-radius: 6px; font-weight: 600; font-size: 0.75rem; }
.severity-high     { background: var(--accent-dim); color: var(--accent); padding: 3px 10px; border-radius: 6px; font-weight: 600; font-size: 0.75rem; }
.severity-critical { background: var(--red-dim);    color: var(--red);    padding: 3px 10px; border-radius: 6px; font-weight: 600; font-size: 0.75rem; }

/* ─────────── Info / Alert Panels ─────────── */
.info-panel {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-left: 4px solid var(--accent);
    border-radius: var(--radius-md);
    padding: 20px 24px;
    margin: 12px 0;
}
.alert-panel {
    border-radius: var(--radius-md);
    padding: 16px 20px;
    margin: 8px 0;
    font-weight: 500;
    border: 1px solid;
}
.alert-warning { background: var(--yellow-dim); border-color: rgba(251,191,36,0.25); color: var(--yellow); }
.alert-danger  { background: var(--red-dim);    border-color: rgba(248,113,113,0.25); color: var(--red); }
.alert-success { background: var(--green-dim);  border-color: rgba(52,211,153,0.25);  color: var(--green); }
.alert-info    { background: var(--blue-dim);   border-color: rgba(96,165,250,0.25);  color: var(--blue); }

/* ─────────── Section Headers ─────────── */
.section-header {
    font-size: 1.4rem; font-weight: 700;
    color: var(--text-primary);
    margin: 28px 0 16px;
    padding-bottom: 10px;
    border-bottom: 2px solid var(--border-subtle);
    display: flex; align-items: center; gap: 10px;
}

/* ─────────── Glass Card ─────────── */
.glass-card {
    background: var(--bg-glass);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 28px;
    box-shadow: var(--shadow-card);
}

/* ─────────── PPE Checklist ─────────── */
.ppe-item {
    display: flex; align-items: center; gap: 12px;
    padding: 12px 16px;
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    margin: 6px 0;
    transition: var(--transition);
}
.ppe-item:hover { border-color: var(--border-glow); }
.ppe-check { color: var(--green);  font-size: 1.2rem; }
.ppe-cross { color: var(--red);    font-size: 1.2rem; }

/* ─────────── Hazard Card ─────────── */
.hazard-card {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 18px 20px;
    margin: 8px 0;
    transition: var(--transition);
}
.hazard-card:hover { border-color: var(--border-glow); transform: translateY(-1px); }

/* ─────────── Chat Bubble ─────────── */
.chat-user {
    background: linear-gradient(135deg, rgba(255,107,53,0.15), rgba(255,107,53,0.05));
    border: 1px solid rgba(255,107,53,0.2);
    border-radius: var(--radius-lg) var(--radius-lg) 4px var(--radius-lg);
    padding: 14px 18px;
    margin: 8px 0; max-width: 85%;
    margin-left: auto;
}
.chat-ai {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg) var(--radius-lg) var(--radius-lg) 4px;
    padding: 14px 18px;
    margin: 8px 0; max-width: 85%;
}

/* ─────────── Progress Bars ─────────── */
.progress-container {
    background: var(--bg-card);
    border-radius: 100px;
    height: 14px;
    overflow: hidden;
    border: 1px solid var(--border-subtle);
}
.progress-fill {
    height: 100%;
    border-radius: 100px;
    background: linear-gradient(90deg, var(--accent), var(--teal));
    transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 0 12px rgba(255,107,53,0.4);
}

/* ─────────── Weather Card ─────────── */
.weather-card {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 24px;
    text-align: center;
    transition: var(--transition);
}
.weather-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-glow); }
.weather-icon { font-size: 3.5rem; margin-bottom: 8px; }
.weather-label { font-size: 1rem; font-weight: 600; color: var(--text-primary); }

/* ─────────── Divider ─────────── */
.styled-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border-subtle), transparent);
    margin: 24px 0;
    border: none;
}

/* ─────────── Demo Badge ─────────── */
.demo-badge {
    background: linear-gradient(135deg, var(--purple-dim), rgba(167,139,250,0.05));
    border: 1px solid rgba(167,139,250,0.3);
    border-radius: var(--radius-md);
    padding: 12px 18px;
    text-align: center;
    color: var(--purple);
    font-weight: 600;
    font-size: 0.85rem;
    margin: 8px 0;
    animation: pulse-border 3s ease-in-out infinite;
}
@keyframes pulse-border {
    0%, 100% { border-color: rgba(167,139,250,0.3); }
    50%      { border-color: rgba(167,139,250,0.6); }
}

/* ─────────── Animations ─────────── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}
.animate-in { animation: fadeInUp 0.5s ease-out forwards; }

/* ─────────── File Uploader ─────────── */
[data-testid="stFileUploader"] {
    border: 2px dashed var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 8px;
    transition: var(--transition);
}
[data-testid="stFileUploader"]:hover { border-color: var(--accent); }

/* ─────────── Button Overrides ─────────── */
.stButton > button {
    border-radius: var(--radius-md) !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    transition: var(--transition) !important;
}
.stDownloadButton > button {
    background: linear-gradient(135deg, var(--accent), #E85D2B) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius-md) !important;
    font-weight: 600 !important;
}
.stDownloadButton > button:hover {
    box-shadow: 0 4px 20px rgba(255,107,53,0.4) !important;
    transform: translateY(-1px);
}

/* ─────────── Expander ─────────── */
.streamlit-expanderHeader {
    font-weight: 600 !important;
    color: var(--text-primary) !important;
}

/* ─────────── Architecture Diagram (text-based) ─────────── */
.arch-block {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 14px 18px;
    margin: 6px 0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: var(--text-secondary);
    transition: var(--transition);
}
.arch-block:hover { border-color: var(--accent); color: var(--text-primary); }

/* ─────────── Hero Header ─────────── */
.hero-header {
    background: linear-gradient(135deg, rgba(255,107,53,0.08) 0%, rgba(45,212,191,0.06) 50%, rgba(96,165,250,0.04) 100%);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-xl);
    padding: 32px 36px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero-header::after {
    content: '';
    position: absolute; top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--accent), var(--teal), var(--blue), var(--purple));
}
.hero-title {
    font-size: 2rem; font-weight: 900;
    background: linear-gradient(135deg, var(--accent), var(--teal));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 4px; line-height: 1.2;
}
.hero-sub { color: var(--text-secondary); font-size: 0.95rem; font-weight: 400; }
</style>
"""
