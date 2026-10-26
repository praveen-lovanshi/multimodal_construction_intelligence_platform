"""
app.py — Multimodal Construction Intelligence Platform
Skill Wallet Capstone Project 1

A production-ready Streamlit application integrating Google Gemini
multimodal AI for construction site safety auditing, structural crack
diagnostics, real-estate valuation, and an intelligent site assistant.

Run:  streamlit run app.py
"""

from __future__ import annotations

import json
import math
import urllib.parse
from datetime import datetime
from typing import Optional

import streamlit as st
from PIL import Image

from styles import get_main_css
from gemini_client import (
    configure_api,
    analyze_image,
    chat_with_gemini,
    demo_ppe_report,
    demo_crack_report,
    demo_chat_response,
)
from prompts import (
    PPE_AUDIT_PROMPT,
    CRACK_DIAGNOSIS_PROMPT,
    CHAT_SYSTEM_INSTRUCTION,
    get_3d_render_prompt,
)

# ╔══════════════════════════════════════════════════════════════════╗
# ║  Page Configuration                                             ║
# ╚══════════════════════════════════════════════════════════════════╝

st.set_page_config(
    page_title="Multimodal Construction Intelligence Platform",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "Multimodal Construction Intelligence Platform — Skill Wallet Capstone Project 1",
    },
)

# Inject CSS
st.markdown(get_main_css(), unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════╗
# ║  Session State Initialization                                   ║
# ╚══════════════════════════════════════════════════════════════════╝

def _init_state():
    defaults = {
        "api_key": "",
        "demo_mode": True,
        "chat_history": [],
        "ppe_report": None,
        "crack_report": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init_state()


# ╔══════════════════════════════════════════════════════════════════╗
# ║  Helper Renderers                                               ║
# ╚══════════════════════════════════════════════════════════════════╝

def _metric_card(icon: str, value: str, label: str) -> str:
    return f"""
    <div class="metric-card animate-in">
        <div class="metric-icon">{icon}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
    </div>"""


def _status_pill(text: str, variant: str = "info") -> str:
    return f'<span class="pill pill-{variant}">{text}</span>'


def _severity_badge(severity: str) -> str:
    s = severity.lower()
    return f'<span class="severity-{s}">{severity}</span>'


def _section_header(icon: str, text: str) -> str:
    return f'<div class="section-header">{icon} {text}</div>'


def _progress_bar(pct: float) -> str:
    return f"""
    <div class="progress-container">
        <div class="progress-fill" style="width:{min(pct, 100):.1f}%"></div>
    </div>"""


def _divider():
    st.markdown('<div class="styled-divider"></div>', unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════╗
# ║  Sidebar                                                        ║
# ╚══════════════════════════════════════════════════════════════════╝

with st.sidebar:
    st.markdown("## 🏗️ Construction AI")
    st.markdown("**Multimodal Intelligence Platform**")
    st.markdown("---")

    # --- API Key ---
    st.markdown("### 🔑 API Configuration")
    api_key_input = st.text_input(
        "Google Gemini API Key",
        type="password",
        placeholder="Enter your Gemini API key…",
        help="Get a free API key from https://aistudio.google.com/app/apikey",
    )

    if api_key_input:
        st.session_state["api_key"] = api_key_input
        st.session_state["demo_mode"] = False
        st.markdown(_status_pill("🟢 API Connected", "safe"), unsafe_allow_html=True)
    else:
        st.session_state["demo_mode"] = True
        st.markdown(
            '<div class="demo-badge">🎭 Demo Mode — sample data shown</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # --- Architecture Overview ---
    st.markdown("### 🏛️ Architecture")
    with st.expander("System Overview", expanded=False):
        st.markdown(
            """
<div class="arch-block">┌─────────────────────────┐
│   Streamlit Frontend    │
│  (Tabs · Cards · Chat) │
└──────────┬──────────────┘
           │
    ┌──────▼──────┐
    │ Gemini 1.5  │
    │  Flash API  │
    └──────┬──────┘
           │
  ┌────────▼────────────┐
  │ Multimodal Pipeline  │
  │ • PPE Audit          │
  │ • Crack Diagnostics  │
  │ • Chat Assistant     │
  └──────────────────────┘</div>
            """,
            unsafe_allow_html=True,
        )

    # --- Feature Navigation ---
    st.markdown("### 🧭 Quick Navigation")
    st.markdown(
        """
- 🦺 **Tab 1** — PPE & Safety Audit
- 🔍 **Tab 2** — Crack Diagnostics
- 📊 **Tab 3** — Valuation & Planning
- 🤖 **Tab 4** — Site Assistant
        """
    )
    st.markdown("---")

    # --- Footer ---
    st.markdown(
        f"""
<div style="text-align:center; color: var(--text-muted); font-size: 0.75rem;">
    <strong>Skill Wallet Capstone Project 1</strong><br/>
    v1.0.0 · {datetime.now().strftime('%B %Y')}<br/>
    Built with Streamlit + Gemini AI
</div>
        """,
        unsafe_allow_html=True,
    )


# ╔══════════════════════════════════════════════════════════════════╗
# ║  Hero Header                                                    ║
# ╚══════════════════════════════════════════════════════════════════╝

st.markdown(
    """
<div class="hero-header animate-in">
    <div class="hero-title">🏗️ Multimodal Construction Intelligence Platform</div>
    <div class="hero-sub">
        AI-powered safety auditing · Structural diagnostics · Real-estate valuation · Smart site assistant
    </div>
</div>
    """,
    unsafe_allow_html=True,
)


# ╔══════════════════════════════════════════════════════════════════╗
# ║  Tabs                                                           ║
# ╚══════════════════════════════════════════════════════════════════╝

tab1, tab2, tab3, tab4 = st.tabs([
    "🦺 Site Safety & PPE Audit",
    "🔍 Crack Diagnostics",
    "📊 Planning & Valuation",
    "🤖 Site Assistant",
])


# ───────────────────────────────────────────────────────────────────
# TAB 1 — Site Safety & PPE Audit
# ───────────────────────────────────────────────────────────────────

with tab1:
    st.markdown(_section_header("🦺", "Site Safety & PPE Compliance Audit"), unsafe_allow_html=True)
    st.markdown(
        "Upload a construction site photo to receive an AI-powered safety audit under **OSHA 1926** and **IS 456** standards."
    )
    _divider()

    uploaded_ppe = st.file_uploader(
        "Upload Construction Site Photo",
        type=["jpg", "jpeg", "png"],
        key="ppe_upload",
        help="Upload a clear photo showing workers and the construction site.",
    )

    col_img, col_ctrl = st.columns([1, 1])

    with col_img:
        if uploaded_ppe:
            image = Image.open(uploaded_ppe)
            st.image(image, caption="Uploaded Site Photo", use_container_width=True)

    with col_ctrl:
        if uploaded_ppe:
            st.markdown(
                """
<div class="info-panel">
    <strong>📋 Audit Scope</strong><br/>
    <span style="color: var(--text-secondary); font-size: 0.88rem;">
    Checking: Hard Hat · Hi-Vis Vest · Steel-Toe Boots · Safety Harness · Gloves · Eye Protection<br/>
    Standards: OSHA 1926 · IS 456:2000 · NBC India 2016
    </span>
</div>
                """,
                unsafe_allow_html=True,
            )

            analyze_btn = st.button("🔍 Run Safety Audit", type="primary", use_container_width=True, key="ppe_btn")

            if analyze_btn:
                with st.spinner("🤖 Analyzing site safety…"):
                    try:
                        if st.session_state["demo_mode"]:
                            report = demo_ppe_report()
                        else:
                            report = analyze_image(
                                image, PPE_AUDIT_PROMPT, st.session_state["api_key"]
                            )
                        st.session_state["ppe_report"] = report
                    except Exception as e:
                        st.error(f"Analysis failed: {e}")
                        st.session_state["ppe_report"] = demo_ppe_report()
                        st.info("📌 Showing demonstration data as fallback.")

    # --- Render PPE Report ---
    report = st.session_state.get("ppe_report")
    if report and uploaded_ppe:
        _divider()

        # Metric cards
        score = report.get("safety_score", 0)
        status = report.get("overall_status", "Unknown")
        hazard_count = len(report.get("site_hazards", []))

        if score >= 80:
            score_variant = "safe"
        elif score >= 50:
            score_variant = "warn"
        else:
            score_variant = "danger"

        status_variant = {"Safe": "safe", "Needs Improvement": "warn", "Unsafe": "danger", "Critical": "danger"}.get(status, "info")

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(_metric_card("🛡️", str(score), "Safety Score"), unsafe_allow_html=True)
        with m2:
            st.markdown(_metric_card("📊", status, "Overall Status"), unsafe_allow_html=True)
        with m3:
            st.markdown(_metric_card("⚠️", str(hazard_count), "Hazards Found"), unsafe_allow_html=True)
        with m4:
            ppe = report.get("ppe_detection", {})
            compliant = sum(1 for v in ppe.values() if isinstance(v, dict) and v.get("detected"))
            st.markdown(_metric_card("🦺", f"{compliant}/{len(ppe)}", "PPE Items OK"), unsafe_allow_html=True)

        _divider()

        # PPE Checklist
        st.markdown(_section_header("✅", "PPE Detection Checklist"), unsafe_allow_html=True)
        ppe_items = report.get("ppe_detection", {})
        ppe_labels = {
            "hard_hat_helmet": "🪖 Hard Hat / Helmet",
            "high_visibility_vest": "🦺 High-Visibility Vest",
            "steel_toe_boots": "👢 Steel-Toe Boots",
            "safety_harness": "🪢 Safety Harness",
            "safety_gloves": "🧤 Safety Gloves",
            "eye_protection": "🥽 Eye Protection",
        }

        cols_ppe = st.columns(2)
        for idx, (key, info) in enumerate(ppe_items.items()):
            col = cols_ppe[idx % 2]
            if isinstance(info, dict):
                icon = '<span class="ppe-check">✅</span>' if info.get("detected") else '<span class="ppe-cross">❌</span>'
                label = ppe_labels.get(key, key.replace("_", " ").title())
                compliance = info.get("compliance", "N/A")
                with col:
                    st.markdown(
                        f"""
<div class="ppe-item">
    {icon}
    <div>
        <strong>{label}</strong><br/>
        <span style="color: var(--text-secondary); font-size: 0.82rem;">{compliance}</span>
    </div>
</div>""",
                        unsafe_allow_html=True,
                    )

        _divider()

        # Site Hazards
        st.markdown(_section_header("⚠️", "Identified Site Hazards"), unsafe_allow_html=True)
        for h in report.get("site_hazards", []):
            sev = h.get("severity", "Medium")
            st.markdown(
                f"""
<div class="hazard-card">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
        <strong style="color: var(--text-primary);">{h.get('hazard', 'Unknown Hazard')}</strong>
        {_severity_badge(sev)}
    </div>
    <div style="color: var(--text-secondary); font-size: 0.85rem;">
        <strong>Remedy:</strong> {h.get('remedy', 'N/A')}
    </div>
</div>""",
                unsafe_allow_html=True,
            )

        _divider()

        # Summary & Download
        st.markdown(_section_header("📝", "Summary & Report"), unsafe_allow_html=True)
        st.markdown(
            f"""
<div class="info-panel">
    {report.get('recommendations_summary', '')}
</div>""",
            unsafe_allow_html=True,
        )

        report_json = json.dumps(report, indent=2, ensure_ascii=False)
        st.download_button(
            label="📥 Download Full JSON Report",
            data=report_json,
            file_name=f"ppe_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True,
        )


# ───────────────────────────────────────────────────────────────────
# TAB 2 — Crack Diagnostics & Structural Integrity
# ───────────────────────────────────────────────────────────────────

with tab2:
    st.markdown(_section_header("🔍", "Crack Diagnostics & Structural Integrity Analysis"), unsafe_allow_html=True)
    st.markdown(
        "Upload a photo of a concrete or masonry surface defect for AI-powered structural assessment."
    )
    _divider()

    uploaded_crack = st.file_uploader(
        "Upload Crack / Defect Photo",
        type=["jpg", "jpeg", "png"],
        key="crack_upload",
        help="Upload a close-up photo of the crack or surface defect.",
    )

    c_img, c_ctrl = st.columns([1, 1])

    with c_img:
        if uploaded_crack:
            crack_image = Image.open(uploaded_crack)
            st.image(crack_image, caption="Uploaded Defect Image", use_container_width=True)

    with c_ctrl:
        if uploaded_crack:
            st.markdown(
                """
<div class="info-panel">
    <strong>🔬 Diagnostic Scope</strong><br/>
    <span style="color: var(--text-secondary); font-size: 0.88rem;">
    Classifying: Hairline · Settlement · Structural Shear · Thermal · Spalling · Corrosion · Shrinkage<br/>
    Standards: IS 456:2000 · IS 13920 · ACI 224R
    </span>
</div>
                """,
                unsafe_allow_html=True,
            )

            diag_btn = st.button("🔬 Run Diagnostics", type="primary", use_container_width=True, key="crack_btn")

            if diag_btn:
                with st.spinner("🤖 Analyzing structural defect…"):
                    try:
                        if st.session_state["demo_mode"]:
                            crack_rpt = demo_crack_report()
                        else:
                            crack_rpt = analyze_image(
                                crack_image, CRACK_DIAGNOSIS_PROMPT, st.session_state["api_key"]
                            )
                        st.session_state["crack_report"] = crack_rpt
                    except Exception as e:
                        st.error(f"Analysis failed: {e}")
                        st.session_state["crack_report"] = demo_crack_report()
                        st.info("📌 Showing demonstration data as fallback.")

    # --- Render Crack Report ---
    crack_rpt = st.session_state.get("crack_report")
    if crack_rpt and uploaded_crack:
        _divider()

        # Top metrics
        defect = crack_rpt.get("defect_type", "Unknown")
        width = crack_rpt.get("estimated_crack_width_mm", 0)
        urgency = crack_rpt.get("urgency", "Medium")
        risk = crack_rpt.get("structural_integrity_assessment", {}).get("risk_level", "Unknown")

        urgency_variant = {"Low": "safe", "Medium": "warn", "High": "danger", "Critical": "danger"}.get(urgency, "info")

        mc1, mc2, mc3, mc4 = st.columns(4)
        with mc1:
            st.markdown(_metric_card("🔬", defect, "Defect Type"), unsafe_allow_html=True)
        with mc2:
            st.markdown(_metric_card("📏", f"{width} mm", "Crack Width"), unsafe_allow_html=True)
        with mc3:
            st.markdown(_metric_card("⏰", urgency, "Urgency"), unsafe_allow_html=True)
        with mc4:
            st.markdown(_metric_card("🏗️", risk, "Risk Level"), unsafe_allow_html=True)

        _divider()

        # Crack Details
        st.markdown(_section_header("📋", "Crack Analysis Details"), unsafe_allow_html=True)
        det_col1, det_col2 = st.columns(2)

        with det_col1:
            st.markdown(
                f"""
<div class="info-panel">
    <strong>🔎 Crack Pattern</strong><br/>
    <span style="color: var(--text-secondary);">{crack_rpt.get('crack_pattern', 'N/A')}</span>
</div>
<div class="info-panel">
    <strong>📍 Location Zone</strong><br/>
    <span style="color: var(--text-secondary);">{crack_rpt.get('location_zone', 'N/A')}</span>
</div>""",
                unsafe_allow_html=True,
            )

        with det_col2:
            integrity = crack_rpt.get("structural_integrity_assessment", {})
            st.markdown(
                f"""
<div class="info-panel">
    <strong>⚡ Load Capacity Impact</strong><br/>
    <span style="color: var(--text-secondary);">{integrity.get('load_capacity_impact', 'N/A')}</span>
</div>
<div class="info-panel">
    <strong>📡 Monitoring Required</strong><br/>
    <span style="color: var(--text-secondary);">{'Yes — continuous monitoring recommended' if integrity.get('monitoring_required') else 'No — periodic inspection sufficient'}</span>
</div>""",
                unsafe_allow_html=True,
            )

        _divider()

        # Root Causes
        st.markdown(_section_header("🌱", "Root Causes"), unsafe_allow_html=True)
        for i, cause in enumerate(crack_rpt.get("root_causes", []), 1):
            st.markdown(
                f"""
<div class="ppe-item">
    <span style="color: var(--accent); font-weight: 700; font-size: 1.1rem;">{i}</span>
    <span style="color: var(--text-primary);">{cause}</span>
</div>""",
                unsafe_allow_html=True,
            )

        _divider()

        # Recommended Repairs
        st.markdown(_section_header("🔧", "Recommended Repairs"), unsafe_allow_html=True)
        for repair in crack_rpt.get("recommended_repairs", []):
            priority = repair.get("priority", "Scheduled")
            p_variant = "danger" if "Immediate" in priority else ("warn" if "week" in priority.lower() else "info")
            st.markdown(
                f"""
<div class="hazard-card">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
        <strong style="color: var(--text-primary);">🔧 {repair.get('method', '')}</strong>
        {_status_pill(priority, p_variant)}
    </div>
    <div style="color: var(--text-secondary); font-size: 0.85rem;">
        {repair.get('description', '')}
    </div>
</div>""",
                unsafe_allow_html=True,
            )

        _divider()

        # Monitoring Plan
        st.markdown(_section_header("📡", "Monitoring Plan"), unsafe_allow_html=True)
        st.markdown(
            f'<div class="info-panel">{crack_rpt.get("monitoring_plan", "N/A")}</div>',
            unsafe_allow_html=True,
        )

        # Download
        crack_json = json.dumps(crack_rpt, indent=2, ensure_ascii=False)
        st.download_button(
            label="📥 Download Diagnostics Report",
            data=crack_json,
            file_name=f"crack_diagnostics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True,
        )


# ───────────────────────────────────────────────────────────────────
# TAB 3 — Planning & Real Estate Valuation
# ───────────────────────────────────────────────────────────────────

with tab3:
    st.markdown(_section_header("📊", "Planning & Real Estate Valuation"), unsafe_allow_html=True)
    st.markdown(
        "Configure project parameters to compute budget, asset valuation, material estimates, and generate a conceptual 3D render."
    )
    _divider()

    # --- Input Panel ---
    inp1, inp2 = st.columns(2)

    with inp1:
        structure_type = st.selectbox(
            "🏢 Structure Type",
            ["Residential Apartment", "Commercial Office", "Villa / Independent House",
             "Industrial Warehouse", "Mixed-Use Complex", "Hospital / Healthcare",
             "Educational Institute", "IT Park / Tech Campus"],
            key="struct_type",
        )

        built_up_sqft = st.number_input(
            "📐 Built-Up Area (sq. ft.)",
            min_value=500, max_value=500000, value=2500, step=100, key="sqft",
        )

        location_tier = st.selectbox(
            "📍 Location Tier",
            ["Tier 1 — Metro (Mumbai, Delhi, Bangalore)",
             "Tier 2 — City (Pune, Jaipur, Lucknow)",
             "Tier 3 — Town (Bhopal, Raipur, Dehradun)"],
            key="tier",
        )

    with inp2:
        completion_pct = st.slider(
            "🏗️ Project Completion (%)",
            min_value=0, max_value=100, value=45, step=5, key="completion",
        )

        num_floors = st.number_input(
            "🏢 Number of Floors", min_value=1, max_value=100, value=4, step=1, key="floors",
        )

        parking = st.selectbox(
            "🅿️ Parking Provision",
            ["Basement Parking", "Surface Parking", "Multilevel Parking", "No Parking"],
            key="parking",
        )

    _divider()

    # --- Calculation Engine ---
    # Cost rates per sqft (INR) by tier
    tier_key = location_tier.split("—")[0].strip()
    cost_rates = {"Tier 1": 2800, "Tier 2": 2100, "Tier 3": 1550}
    market_rates = {"Tier 1": 12500, "Tier 2": 7500, "Tier 3": 4500}  # ₹/sqft market value

    base_rate = cost_rates.get(tier_key, 2100)
    mkt_rate = market_rates.get(tier_key, 7500)

    # Multipliers by structure type
    type_multiplier = {
        "Residential Apartment": 1.0, "Commercial Office": 1.25, "Villa / Independent House": 1.15,
        "Industrial Warehouse": 0.75, "Mixed-Use Complex": 1.3, "Hospital / Healthcare": 1.6,
        "Educational Institute": 1.1, "IT Park / Tech Campus": 1.35,
    }.get(structure_type, 1.0)

    construction_cost = built_up_sqft * base_rate * type_multiplier
    capex_incurred = construction_cost * (completion_pct / 100)
    market_valuation = built_up_sqft * mkt_rate * type_multiplier

    # Material estimates (per IS norms approx.)
    steel_kg = built_up_sqft * 4.5 * num_floors * 0.25  # ~4.5 kg/sqft simplified
    cement_bags = built_up_sqft * 0.4 * num_floors * 0.25  # ~0.4 bags/sqft simplified

    def _fmt_inr(val: float) -> str:
        if val >= 1e7:
            return f"₹ {val / 1e7:.2f} Cr"
        elif val >= 1e5:
            return f"₹ {val / 1e5:.2f} L"
        else:
            return f"₹ {val:,.0f}"

    # --- Render Metrics ---
    st.markdown(_section_header("💰", "Financial Overview"), unsafe_allow_html=True)

    f1, f2, f3, f4 = st.columns(4)
    with f1:
        st.markdown(_metric_card("🏗️", _fmt_inr(construction_cost), "Total Project Budget"), unsafe_allow_html=True)
    with f2:
        st.markdown(_metric_card("💸", _fmt_inr(capex_incurred), "CapEx Incurred"), unsafe_allow_html=True)
    with f3:
        st.markdown(_metric_card("🏠", _fmt_inr(market_valuation), "Market Valuation"), unsafe_allow_html=True)
    with f4:
        roi = ((market_valuation - construction_cost) / construction_cost) * 100 if construction_cost else 0
        st.markdown(_metric_card("📈", f"{roi:.1f}%", "Projected ROI"), unsafe_allow_html=True)

    _divider()

    # Material & Progress
    st.markdown(_section_header("🧱", "Material Estimates & Progress"), unsafe_allow_html=True)
    mat1, mat2, mat3 = st.columns(3)

    with mat1:
        st.markdown(_metric_card("🔩", f"{steel_kg:,.0f} kg", "Steel Required"), unsafe_allow_html=True)
    with mat2:
        st.markdown(_metric_card("🧱", f"{cement_bags:,.0f}", "Cement Bags (50 kg)"), unsafe_allow_html=True)
    with mat3:
        st.markdown(_metric_card("🏢", str(num_floors), "Total Floors"), unsafe_allow_html=True)

    st.markdown("")
    st.markdown(f"**Milestone Progress — {completion_pct}% Complete**")
    st.markdown(_progress_bar(completion_pct), unsafe_allow_html=True)

    # Milestone labels
    milestones = [
        (0, "📋 Planning"), (15, "🏗️ Foundation"), (30, "🧱 Superstructure"),
        (55, "🔌 MEP Rough-In"), (70, "🪟 Finishing"), (85, "🎨 Interior"),
        (95, "✅ Handover"),
    ]
    current_milestone = "📋 Planning"
    for pct_threshold, label in milestones:
        if completion_pct >= pct_threshold:
            current_milestone = label

    st.markdown(
        f"""
<div class="info-panel">
    <strong>Current Phase:</strong> {current_milestone}<br/>
    <span style="color: var(--text-secondary); font-size: 0.85rem;">
        Budget utilisation: {_fmt_inr(capex_incurred)} of {_fmt_inr(construction_cost)}
        ({completion_pct}%)
    </span>
</div>""",
        unsafe_allow_html=True,
    )

    _divider()

    # --- 3D Architectural Rendering via Pollinations ---
    st.markdown(_section_header("🎨", "Conceptual 3D Architectural Rendering"), unsafe_allow_html=True)
    st.markdown(
        "Generate a conceptual AI rendering of your project using **Pollinations AI**."
    )

    location_name = location_tier.split("(")[1].rstrip(")").split(",")[0].strip() if "(" in location_tier else "India"

    if st.button("🖼️ Generate 3D Render", type="primary", use_container_width=True, key="render_btn"):
        render_prompt = get_3d_render_prompt(structure_type, built_up_sqft, location_name)
        encoded = urllib.parse.quote(render_prompt)
        img_url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=576&nologo=true"

        with st.spinner("🎨 Generating conceptual render…"):
            st.image(img_url, caption=f"AI Render — {structure_type} in {location_name}", use_container_width=True)

        st.markdown(
            f"""
<div class="info-panel">
    <strong>🤖 Prompt Used:</strong><br/>
    <span style="color: var(--text-secondary); font-size: 0.82rem; font-style: italic;">
        {render_prompt}
    </span>
</div>""",
            unsafe_allow_html=True,
        )


# ───────────────────────────────────────────────────────────────────
# TAB 4 — Daily Site Assistant & Weather-Aware Advisory
# ───────────────────────────────────────────────────────────────────

with tab4:
    st.markdown(_section_header("🤖", "Daily Site Assistant & Weather-Aware Advisory"), unsafe_allow_html=True)
    _divider()

    # --- Weather Advisory ---
    st.markdown(_section_header("🌤️", "Weather Condition Advisory"), unsafe_allow_html=True)

    weather_options = {
        "☀️ Normal": {
            "icon": "☀️", "label": "Normal Conditions",
            "alerts": [
                ("alert-success", "✅ All construction activities may proceed as scheduled."),
                ("alert-info", "💧 Ensure adequate hydration breaks for workers every 90 minutes."),
                ("alert-info", "📋 Standard safety protocols in effect."),
            ],
        },
        "💨 High Wind": {
            "icon": "💨", "label": "High Wind Alert",
            "alerts": [
                ("alert-danger", "🏗️ <strong>SUSPEND</strong> all crane and lifting operations when wind speed exceeds 20 m/s (IS 3177)."),
                ("alert-danger", "🪜 Suspend scaffolding work above 3 storeys."),
                ("alert-warning", "📦 Secure all loose materials, formwork panels, and temporary sheeting."),
                ("alert-warning", "🚧 Barricade areas below elevated work zones."),
                ("alert-info", "📡 Monitor wind speed every 30 minutes; resume when sustained < 15 m/s."),
            ],
        },
        "🌧️ Heavy Rain": {
            "icon": "🌧️", "label": "Heavy Rain Alert",
            "alerts": [
                ("alert-danger", "🚫 <strong>HALT</strong> concrete pouring operations immediately."),
                ("alert-danger", "⚡ <strong>ELECTRICAL HAZARD</strong> — De-energize temporary power lines near pooling water."),
                ("alert-warning", "🪣 Activate site drainage / dewatering pumps."),
                ("alert-warning", "🛡️ Cover fresh concrete pours with polythene sheets."),
                ("alert-info", "🧪 Post-rain: Test aggregate moisture content before resuming batching."),
                ("alert-info", "🔍 Inspect excavations for soil collapse risk before re-entry."),
            ],
        },
        "🔥 Extreme Heat": {
            "icon": "🔥", "label": "Extreme Heat Alert",
            "alerts": [
                ("alert-danger", "🌡️ <strong>HEAT STRESS</strong> — Mandatory 15-min rest every 60 min when T > 40 °C."),
                ("alert-warning", "🧊 Concrete curing protocol: Use chilled water or ice; avoid pouring between 11 AM – 3 PM."),
                ("alert-warning", "💧 Deploy ORS stations at every floor; mandatory hydration tracking."),
                ("alert-info", "🕶️ Provide UV-protective eyewear and wide-brim attachments for helmets."),
                ("alert-info", "📅 Shift heavy-labour tasks to early morning (6–10 AM) or evening (4–6 PM)."),
            ],
        },
    }

    weather_cols = st.columns(4)
    selected_weather = st.session_state.get("selected_weather", "☀️ Normal")

    for i, (key, data) in enumerate(weather_options.items()):
        with weather_cols[i]:
            if st.button(
                f"{data['icon']}\n{data['label']}", key=f"weather_{key}",
                use_container_width=True,
            ):
                st.session_state["selected_weather"] = key
                selected_weather = key

    sel = weather_options.get(selected_weather, weather_options["☀️ Normal"])
    st.markdown(
        f"""
<div class="weather-card" style="margin:16px 0;">
    <div class="weather-icon">{sel['icon']}</div>
    <div class="weather-label">{sel['label']}</div>
</div>""",
        unsafe_allow_html=True,
    )

    for cls, txt in sel["alerts"]:
        st.markdown(f'<div class="alert-panel {cls}">{txt}</div>', unsafe_allow_html=True)

    _divider()

    # --- Chatbot ---
    st.markdown(_section_header("💬", "Construction Engineering Chatbot"), unsafe_allow_html=True)
    st.markdown(
        "Ask questions about concrete technology, reinforcement detailing, IS codes, OSHA standards, and more."
    )

    # Render chat history
    for msg in st.session_state["chat_history"]:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-user">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-ai">{msg["content"]}</div>', unsafe_allow_html=True)

    # Chat input
    user_input = st.chat_input("Ask ConstructBot anything about construction engineering…", key="chat_input")

    if user_input:
        # Add user message
        st.session_state["chat_history"].append({"role": "user", "content": user_input})

        with st.spinner("🤖 Thinking…"):
            try:
                if st.session_state["demo_mode"]:
                    ai_response = demo_chat_response(user_input)
                else:
                    gemini_messages = [
                        {
                            "role": m["role"] if m["role"] == "user" else "model",
                            "parts": [m["content"]],
                        }
                        for m in st.session_state["chat_history"]
                    ]
                    ai_response = chat_with_gemini(
                        gemini_messages,
                        st.session_state["api_key"],
                        system_instruction=CHAT_SYSTEM_INSTRUCTION,
                    )
            except Exception as e:
                ai_response = f"⚠️ Error communicating with AI: {e}\n\nShowing demo response instead.\n\n{demo_chat_response(user_input)}"

        st.session_state["chat_history"].append({"role": "assistant", "content": ai_response})
        st.rerun()

    # Clear chat button
    if st.session_state["chat_history"]:
        if st.button("🗑️ Clear Chat History", key="clear_chat"):
            st.session_state["chat_history"] = []
            st.rerun()
