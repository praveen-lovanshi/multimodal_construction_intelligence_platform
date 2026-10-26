"""
gemini_client.py — Thin wrapper around the Google Generative AI SDK.
Handles model configuration, image encoding, prompt dispatch, and
graceful fallback to demonstration mode when no API key is available.
"""

from __future__ import annotations

import base64
import json
import re
from io import BytesIO
from typing import Optional

from PIL import Image

# ---------------------------------------------------------------------------
# Lazy import – google-generativeai may not be installed in every env
# ---------------------------------------------------------------------------
_genai = None


def _ensure_genai():
    global _genai
    if _genai is None:
        try:
            import google.generativeai as genai
            _genai = genai
        except ImportError:
            raise ImportError(
                "google-generativeai is required.  Run:  pip install google-generativeai"
            )
    return _genai


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _pil_to_bytes(image: Image.Image, fmt: str = "JPEG") -> bytes:
    """Convert a PIL Image to raw bytes."""
    buf = BytesIO()
    image.save(buf, format=fmt)
    return buf.getvalue()


def _extract_json(text: str) -> dict:
    """
    Best-effort extraction of the first JSON object from model output.
    Handles markdown fenced blocks (```json ... ```) and bare JSON.
    """
    # Try fenced block first
    match = re.search(r"```(?:json)?\s*\n?(.*?)```", text, re.DOTALL)
    if match:
        candidate = match.group(1).strip()
    else:
        # Fall back to first { … }
        start = text.find("{")
        end = text.rfind("}") + 1
        candidate = text[start:end] if start != -1 and end > start else text

    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        return {"raw_response": text}


# ---------------------------------------------------------------------------
# Core API Functions
# ---------------------------------------------------------------------------

def configure_api(api_key: str) -> bool:
    """Configure the Generative AI SDK.  Returns True on success."""
    try:
        genai = _ensure_genai()
        genai.configure(api_key=api_key)
        return True
    except Exception:
        return False


def analyze_image(
    image: Image.Image,
    prompt: str,
    api_key: str,
    model_name: str = "gemini-1.5-flash",
) -> dict:
    """
    Send a multimodal (image + text) request to Gemini and return
    parsed JSON output.
    """
    genai = _ensure_genai()
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(model_name)
    response = model.generate_content([prompt, image])
    return _extract_json(response.text)


def chat_with_gemini(
    messages: list[dict],
    api_key: str,
    system_instruction: str = "",
    model_name: str = "gemini-1.5-flash",
) -> str:
    """
    Multi-turn chat completion.  *messages* is a list of
    ``{"role": "user"|"model", "parts": [str]}``.
    """
    genai = _ensure_genai()
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(
        model_name,
        system_instruction=system_instruction if system_instruction else None,
    )
    chat = model.start_chat(history=messages[:-1])
    last = messages[-1]["parts"][0] if messages else ""
    response = chat.send_message(last)
    return response.text


# ---------------------------------------------------------------------------
# Demonstration / Fallback Data
# ---------------------------------------------------------------------------

def demo_ppe_report() -> dict:
    """Return a realistic mock PPE audit report for demonstration mode."""
    return {
        "safety_score": 62,
        "overall_status": "Needs Improvement",
        "ppe_detection": {
            "hard_hat_helmet": {"detected": True, "compliance": "Partial — 3 of 5 workers wearing helmets"},
            "high_visibility_vest": {"detected": True, "compliance": "Compliant — all workers wearing hi-vis vests"},
            "steel_toe_boots": {"detected": False, "compliance": "Non-Compliant — unable to confirm safety footwear"},
            "safety_harness": {"detected": False, "compliance": "Non-Compliant — workers at height without fall-arrest harness"},
            "safety_gloves": {"detected": True, "compliance": "Partial — only 2 of 5 workers wearing gloves"},
            "eye_protection": {"detected": False, "compliance": "Non-Compliant — no safety goggles observed during grinding"}
        },
        "site_hazards": [
            {
                "hazard": "Unguarded floor opening on 3rd level",
                "severity": "Critical",
                "remedy": "Install temporary guardrails & toe boards immediately per OSHA 1926.502"
            },
            {
                "hazard": "Loose scaffolding planks on east elevation",
                "severity": "High",
                "remedy": "Secure all planks with scaffold clips; conduct scaffold inspection per IS 3696"
            },
            {
                "hazard": "Electrical cables running through standing water",
                "severity": "High",
                "remedy": "Re-route cabling above ground; install GFCI protection per OSHA 1926.405"
            },
            {
                "hazard": "Debris accumulation near stairwell exit",
                "severity": "Medium",
                "remedy": "Clear debris to maintain unobstructed egress path; daily housekeeping schedule"
            },
            {
                "hazard": "Missing signage for overhead crane operation zone",
                "severity": "Low",
                "remedy": "Post warning signage and demarcate exclusion zone with barricade tape"
            }
        ],
        "standards_referenced": ["OSHA 1926", "IS 456:2000", "NBC India 2016"],
        "recommendations_summary": (
            "Immediate action required: Secure floor openings and scaffolding. "
            "Conduct mandatory PPE re-training for all site personnel. "
            "Schedule full safety audit within 48 hours."
        ),
    }


def demo_crack_report() -> dict:
    """Return a realistic mock crack diagnostics report for demonstration mode."""
    return {
        "defect_type": "Settlement Crack",
        "estimated_crack_width_mm": 1.8,
        "crack_pattern": "Diagonal stepping pattern through mortar joints",
        "location_zone": "Load-bearing wall — ground floor",
        "urgency": "High",
        "root_causes": [
            "Differential foundation settlement due to non-uniform soil bearing capacity",
            "Inadequate foundation depth for soil classification (possibly filled ground)",
            "Possible water ingress weakening sub-grade over time",
        ],
        "structural_integrity_assessment": {
            "risk_level": "Moderate-High",
            "load_capacity_impact": "Potential 15-20% reduction in wall load transfer efficiency",
            "monitoring_required": True,
        },
        "recommended_repairs": [
            {
                "method": "Epoxy Injection",
                "description": "Pressure-inject structural epoxy (ER-2200 or equivalent) into crack to restore monolithic bond",
                "priority": "Immediate",
            },
            {
                "method": "Micro-piling / Underpinning",
                "description": "Install mini-piles to stabilize foundation and arrest further settlement",
                "priority": "Within 2 weeks",
            },
            {
                "method": "Carbon Fiber Reinforcement",
                "description": "Apply CFRP strips across crack plane to restore tensile capacity",
                "priority": "After epoxy curing (7 days)",
            },
        ],
        "monitoring_plan": "Install crack gauges at 3 points; measure weekly for 6 months; trigger re-assessment if growth > 0.2 mm/month.",
        "standards_referenced": ["IS 456:2000", "IS 13920", "ACI 224R"],
    }


def demo_chat_response(user_msg: str) -> str:
    """Return a helpful contextual demo response."""
    msg = user_msg.lower()
    if "concrete" in msg or "mix" in msg or "curing" in msg:
        return (
            "**Concrete Mix Design Guidance (IS 456:2000)**\n\n"
            "For M25 grade concrete the typical mix ratio is **1 : 1 : 2** "
            "(cement : fine aggregate : coarse aggregate) with a w/c ratio of **0.45**.\n\n"
            "**Curing Protocol:**\n"
            "- Maintain continuous moist curing for a minimum of **7 days** (28 days ideal).\n"
            "- Water curing or curing compound application within **30 minutes** of finishing.\n"
            "- Ambient temperature monitoring — if T > 35 °C, use chilled water or ice.\n\n"
            "Would you like mix-design calculations for a specific grade?"
        )
    if "rebar" in msg or "reinforcement" in msg or "steel" in msg:
        return (
            "**Steel Reinforcement Best Practices**\n\n"
            "- **Lap Length:** Minimum 40× bar diameter for tension zone (IS 456 Cl. 26.2.5).\n"
            "- **Cover:** 40 mm for columns, 25 mm for slabs (moderate exposure).\n"
            "- **Spacing:** Maximum 300 mm c/c for main bars; minimum 75 mm or bar diameter.\n"
            "- **Grade:** Fe 500D is recommended for seismic zones III–V.\n\n"
            "Need help with a bar-bending schedule?"
        )
    if "weather" in msg or "rain" in msg or "wind" in msg:
        return (
            "**Weather Impact on Construction Activities**\n\n"
            "🌧 **Rain:** Suspend concreting if rainfall > 2.5 mm/hr. Cover fresh pours with polythene.\n"
            "💨 **Wind:** Suspend crane/lifting operations when wind speed exceeds **20 m/s** (IS 3177).\n"
            "☀️ **Heat:** Above 40 °C, schedule pours for early morning; use retarders in mix.\n\n"
            "Shall I generate a weather-adjusted work schedule?"
        )
    return (
        "**Construction Engineering Assistant — Demo Mode**\n\n"
        "I can help with:\n"
        "- 🧱 Concrete mix design & curing protocols\n"
        "- 🔩 Reinforcement detailing & bar-bending schedules\n"
        "- 📐 Structural load analysis guidance\n"
        "- 🦺 OSHA & IS code compliance queries\n"
        "- 🌤 Weather-impact advisories\n\n"
        "Try asking about *concrete curing*, *rebar lap length*, or *weather impact on construction*!"
    )
