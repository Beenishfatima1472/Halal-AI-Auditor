"""
MACI V.03 — Maqasid-Aligned Consequence-Boundary Review Layer
Streamlit Live Audit Tool

Run locally:
    pip install streamlit requests
    streamlit run app.py

This tool is a technical governance review demo. It does not issue fatwas,
replace scholars, or certify Shariah compliance.
"""

import streamlit as st
import datetime
import hashlib
import random
import string

# Optional — only needed if MACI_API_URL is configured for live mode
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


# ──────────────────────────────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="MACI V.03 — Live Audit Tool",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Set this to your live MACI endpoint to use real classification.
# Leave as None to run fully in demo / mock mode.
MACI_API_URL = None  # e.g. "https://api.maqasidai.com/v1/classify"
MACI_API_KEY = None  # e.g. "your-maci-key"


# ──────────────────────────────────────────────────────────────────────
# STYLE — warm green & gold, light, paper-like theme
# ──────────────────────────────────────────────────────────────────────

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg-page:     #f6f3ea;   /* warm parchment */
    --bg-surface:  #ffffff;
    --bg-card:     #fbf9f2;
    --bg-soft:     #f0ecdf;
    --green-deep:  #1f4d3a;   /* deep forest green */
    --green-mid:   #2e6b50;
    --green-soft:  #e8f1ec;
    --gold:        #b8893a;
    --gold-lt:     #d3a85a;
    --gold-soft:   #f3e7cf;
    --text:        #2b2a25;
    --text-mid:    #6b6859;
    --text-dim:    #9c987f;
    --red:         #b8493e;
    --red-soft:    #f6e6e3;
    --amber:       #b8793a;
    --amber-soft:  #f6ecd9;
    --border:      #e1dac4;
    --border-mid:  #d3c9a8;
    --shadow:      rgba(31,77,58,0.07);
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, sans-serif;
}

.stApp {
    background-color: var(--bg-page);
    background-image:
        radial-gradient(ellipse at top left, rgba(31,77,58,0.04) 0%, transparent 55%),
        radial-gradient(ellipse at bottom right, rgba(184,137,58,0.05) 0%, transparent 55%);
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

h1, h2, h3 {
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    color: var(--green-deep) !important;
    font-weight: 500 !important;
}

p, span, label, div { color: var(--text); }

/* Version ribbon */
.version-ribbon {
    background: var(--green-deep);
    border: 1px solid var(--green-deep);
    border-radius: 6px;
    padding: 0.6rem 1.2rem;
    text-align: center;
    font-size: 0.72rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #f3ead0;
    margin-bottom: 1.25rem;
    box-shadow: 0 2px 10px var(--shadow);
}
.version-ribbon .sub {
    color: rgba(243,234,208,0.7);
    font-size: 0.65rem;
    display: block;
    margin-top: 0.3rem;
    letter-spacing: 0.05em;
    text-transform: none;
}

/* Disclaimer box */
.disclaimer-box {
    background: var(--gold-soft);
    border: 1px solid var(--border-mid);
    border-left: 4px solid var(--gold);
    border-radius: 6px;
    padding: 1rem 1.25rem;
    font-size: 0.82rem;
    line-height: 1.75;
    color: var(--text-mid);
    margin-bottom: 1.5rem;
}
.disclaimer-box strong { color: var(--green-deep); }

/* Signal packet card */
.packet-card {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.4rem 1.6rem;
    font-family: 'Inter', monospace;
    font-size: 0.88rem;
    line-height: 2;
    color: var(--text);
    box-shadow: 0 2px 12px var(--shadow);
}
.packet-card .k { color: var(--green-mid); font-weight: 600; }
.packet-card .s { color: var(--gold); }
.packet-card .comment { color: var(--text-dim); font-style: italic; }

/* Result pills */
.pill {
    display: inline-block;
    padding: 0.28rem 0.8rem;
    border-radius: 20px;
    font-size: 0.68rem;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    font-weight: 700;
    margin-right: 0.45rem;
    margin-bottom: 0.3rem;
}
.pill-pass    { background: var(--green-soft);  color: var(--green-deep); border: 1px solid rgba(31,77,58,0.25); }
.pill-flag    { background: var(--amber-soft);  color: var(--amber);      border: 1px solid rgba(184,121,58,0.3); }
.pill-block   { background: var(--red-soft);    color: var(--red);        border: 1px solid rgba(184,73,62,0.3); }
.pill-neutral { background: var(--bg-soft);     color: var(--text-mid);   border: 1px solid var(--border-mid); }
.pill-gold    { background: var(--gold-soft);   color: var(--gold);       border: 1px solid rgba(184,137,58,0.35); }

/* Enrichment block */
.enrichment-block {
    background: var(--green-soft);
    border: 1px solid rgba(31,77,58,0.18);
    border-radius: 8px;
    padding: 1.1rem 1.4rem;
    margin-top: 1.1rem;
    box-shadow: 0 2px 10px var(--shadow);
}
.enrichment-header {
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--green-deep);
    font-weight: 700;
    margin-bottom: 0.85rem;
    border-bottom: 1px solid rgba(31,77,58,0.15);
    padding-bottom: 0.55rem;
}
.e-label {
    font-size: 0.64rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-dim);
    margin-bottom: 0.25rem;
    font-weight: 600;
}
.e-val {
    font-size: 0.9rem;
    color: var(--text);
    margin-bottom: 0.8rem;
}
.e-val.gold { color: var(--gold); font-weight: 600; }

.alt-box {
    background: var(--bg-surface);
    border: 1px solid rgba(31,77,58,0.2);
    border-left: 4px solid var(--green-mid);
    border-radius: 6px;
    padding: 0.9rem 1.1rem;
    margin-top: 0.6rem;
    font-size: 0.85rem;
    color: var(--green-deep);
    line-height: 1.7;
}
.alt-label {
    font-size: 0.64rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--green-mid);
    margin-bottom: 0.45rem;
    font-weight: 700;
}

.warning-box {
    background: var(--amber-soft);
    border: 1px solid rgba(184,121,58,0.3);
    border-left: 4px solid var(--amber);
    border-radius: 6px;
    padding: 0.8rem 1.1rem;
    font-size: 0.82rem;
    color: #8a5a26;
    margin-top: 0.85rem;
}

.audit-id {
    font-size: 0.72rem;
    color: var(--text-dim);
    margin-top: 0.85rem;
    letter-spacing: 0.04em;
    font-family: 'Inter', monospace;
}

/* Buttons */
div.stButton > button {
    background: var(--green-deep);
    color: #f6f3ea;
    border: none;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    font-size: 0.8rem;
    padding: 0.65rem 1rem;
    border-radius: 6px;
    box-shadow: 0 2px 8px rgba(31,77,58,0.2);
}
div.stButton > button:hover {
    background: var(--green-mid);
    color: #f6f3ea;
    box-shadow: 0 3px 12px rgba(31,77,58,0.28);
}

/* Inputs */
.stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
    background-color: var(--bg-surface) !important;
    border: 1px solid var(--border-mid) !important;
    border-radius: 6px !important;
    color: var(--text) !important;
}
.stTextArea textarea:focus {
    border-color: var(--green-mid) !important;
    box-shadow: 0 0 0 1px var(--green-mid) !important;
}

/* Radio buttons in sidebar */
.stRadio label { color: var(--text) !important; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: var(--bg-card);
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] hr {
    border-color: var(--border);
}

/* Captions */
.stCaption, [data-testid="stCaptionContainer"] {
    color: var(--text-dim) !important;
}

hr {
    border-color: var(--border) !important;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────
# PRESETS — mirrors the web demo presets, each with mock enrichment
# ──────────────────────────────────────────────────────────────────────

PRESETS = {
    "Guaranteed return": {
        "text": "This investment product guarantees an 8% annual return on your deposit, fully secured and Shariah-compliant.",
        "context": "Islamic Finance",
        "role": "End User",
        "mock": {
            "result": "FLAGGED",
            "violation": "Riba (Usury / Interest)",
            "confidence": "HIGH",
            "severity": "CRITICAL",
            "action": "QUARANTINE",
            "language": "English",
            "pillar": "Hifz al-Mal (Protection of Property)",
            "pillar_class": "Financial Integrity",
            "aaoifi": "FAS 28 · Murabaha & Deferred Payment Sales",
            "alternative": (
                "Replace fixed-return guarantee with profit-and-loss sharing "
                "(Mudarabah) or cost-plus-mark-up financing (Murabaha) per "
                "AAOIFI FAS 28. Guaranteed returns on deposits constitute "
                "Riba and are not permissible."
            ),
        },
    },
    "Sukuk structure": {
        "text": (
            "This sukuk al-Ijarah structure transfers beneficial ownership of "
            "the underlying asset, generating returns through lease payments "
            "rather than interest."
        ),
        "context": "Islamic Finance",
        "role": "Compliance Officer",
        "mock": {
            "result": "PASS",
            "violation": "None",
            "confidence": "HIGH",
            "severity": "NONE",
            "action": "ALLOW",
            "language": "English",
            "pillar": None,
            "pillar_class": None,
            "aaoifi": None,
            "alternative": None,
        },
    },
    "Fake fatwa": {
        "text": (
            "According to Sheikh Ibn Baz's 2019 fatwa, this cryptocurrency "
            "trading arrangement is fully permissible under Hanbali jurisprudence."
        ),
        "context": "Fatwa Platform",
        "role": "End User",
        "mock": {
            "result": "FLAGGED",
            "violation": "Fabricated Fatwa / Scholar Misattribution",
            "confidence": "HIGH",
            "severity": "CRITICAL",
            "action": "QUARANTINE",
            "language": "English",
            "pillar": "Hifz al-Din (Protection of Religion)",
            "pillar_class": "Religious Authority Integrity",
            "aaoifi": "GSIFI 6 · Governance & Scholar Attribution Standards",
            "alternative": (
                "Remove unverifiable scholar attribution. Reference only "
                "documented, verifiable fatawa from authoritative bodies "
                "(e.g. AAOIFI Shariah Board, OIC Fiqh Academy) with full "
                "source citation, date, and issuing authority."
            ),
        },
    },
    "Arabic · Riba": {
        "text": "القرض بفائدة 24% سنوياً مضمون ومعتمد شرعياً",
        "context": "Islamic Finance",
        "role": "End User",
        "mock": {
            "result": "FLAGGED",
            "violation": "Riba (Usury / Interest)",
            "confidence": "HIGH",
            "severity": "CRITICAL",
            "action": "QUARANTINE",
            "language": "Arabic",
            "pillar": "Hifz al-Mal (Protection of Property)",
            "pillar_class": "Financial Integrity",
            "aaoifi": "FAS 1 · General Presentation and Disclosure",
            "alternative": (
                "استبدل القرض بفائدة بعقد مرابحة أو مشاركة قائم على تقاسم "
                "الأرباح والخسائر. الفائدة المضمونة بنسبة 24% تعد ربا "
                "محرماً وفقاً للفقه الإسلامي."
            ),
        },
    },
    "Urdu · MLM": {
        "text": "ہمارے حلال نیٹ ورک میں شامل ہوں اور ہر رکن کو لانے پر 500 روپے کمائیں",
        "context": "Customer Tool",
        "role": "End User",
        "mock": {
            "result": "FLAGGED",
            "violation": "MLM / Multi-level Marketing Structure",
            "confidence": "HIGH",
            "severity": "HIGH",
            "action": "QUARANTINE",
            "language": "Urdu",
            "pillar": "Hifz al-Mal (Protection of Property)",
            "pillar_class": "Financial Integrity — Exploitative Structures",
            "aaoifi": "FAS 30 · Impairment and Credit Losses",
            "alternative": (
                "Remove recruitment-based commission structure. Permissible "
                "income must derive from genuine trade or service, not from "
                "chain recruitment. Consider a transparent fee-for-service "
                "or profit-sharing model."
            ),
        },
    },
    "Arabizi · Gharar": {
        "text": "ana biddi akhadh qard bil faida 24% — shu ra2yek?",
        "context": "Islamic Finance",
        "role": "End User",
        "mock": {
            "result": "FLAGGED",
            "violation": "Gharar / Riba — Mixed Signal",
            "confidence": "MEDIUM",
            "severity": "HIGH",
            "action": "ESCALATE",
            "language": "Arabizi (Arabic Romanised)",
            "pillar": "Hifz al-Mal (Protection of Property)",
            "pillar_class": "Financial Integrity — Uncertainty",
            "aaoifi": "FAS 28 · Murabaha",
            "alternative": (
                "Code-switching input detected. Core query involves "
                "interest-bearing loan (Riba). Recommend Murabaha or "
                "Musharakah alternative. MEDIUM confidence — requires "
                "scholar review given informal register and ambiguity."
            ),
        },
    },
}

CONTEXT_OPTIONS = [
    "Islamic Finance",
    "Fatwa Platform",
    "Customer Tool",
    "Regulatory Review",
    "General",
]
ROLE_OPTIONS = [
    "End User",
    "Compliance Officer",
    "Shariah Board",
    "Developer",
]


# ──────────────────────────────────────────────────────────────────────
# CLASSIFICATION LOGIC
# ──────────────────────────────────────────────────────────────────────

def make_audit_id(text: str) -> str:
    h = hashlib.sha256(text.encode("utf-8")).hexdigest().upper()[:8]
    date = datetime.datetime.utcnow().strftime("%Y%m%d")
    return f"MACI-{date}-{h}"


def derive_mock_enrichment(violation: str):
    """Fallback enrichment lookup when text doesn't match a preset exactly."""
    v = (violation or "").lower()
    table = {
        "riba": {
            "pillar": "Hifz al-Mal (Protection of Property)",
            "pillar_class": "Financial Integrity",
            "aaoifi": "FAS 28 · Murabaha & Deferred Payment Sales",
            "alternative": (
                "Replace fixed-return with profit-and-loss sharing "
                "(Mudarabah) or cost-plus financing (Murabaha) per "
                "AAOIFI FAS 28."
            ),
        },
        "gharar": {
            "pillar": "Hifz al-Mal (Protection of Property)",
            "pillar_class": "Financial Integrity — Excessive Uncertainty",
            "aaoifi": "FAS 1 · General Presentation and Disclosure",
            "alternative": (
                "Remove speculative or ambiguous terms. Ensure full "
                "disclosure of contract terms, underlying assets, and "
                "return mechanism per AAOIFI FAS 1."
            ),
        },
        "maysir": {
            "pillar": "Hifz al-Mal (Protection of Property)",
            "pillar_class": "Financial Integrity — Gambling",
            "aaoifi": "FAS 30 · Impairment and Credit Losses",
            "alternative": (
                "Remove gambling or lottery-based return mechanism. "
                "Consider Mudarabah with clearly defined profit ratios."
            ),
        },
        "mlm": {
            "pillar": "Hifz al-Mal (Protection of Property)",
            "pillar_class": "Financial Integrity — Exploitative Structures",
            "aaoifi": "FAS 30 · Impairment and Credit Losses",
            "alternative": (
                "Remove recruitment-based commission structure. Income "
                "must derive from genuine trade, not chain recruitment."
            ),
        },
        "fatwa": {
            "pillar": "Hifz al-Din (Protection of Religion)",
            "pillar_class": "Religious Authority Integrity",
            "aaoifi": "GSIFI 6 · Governance & Scholar Attribution",
            "alternative": (
                "Remove unverifiable scholar attribution. Reference only "
                "documented, verifiable fatawa with full citation."
            ),
        },
        "scholar": {
            "pillar": "Hifz al-Din (Protection of Religion)",
            "pillar_class": "Religious Authority Integrity",
            "aaoifi": "GSIFI 6 · Governance & Scholar Attribution",
            "alternative": (
                "Verify scholar citation. Provide issuing body, date, and "
                "source document for all attributed religious opinions."
            ),
        },
    }
    for key, val in table.items():
        if key in v:
            return val
    return None


def mock_classify(text: str, preset_mock: dict | None) -> dict:
    """
    Pure offline classification used when no live MACI_API_URL is set,
    or when the live call fails. Falls back to simple heuristics for
    free-typed text not matching a preset.
    """
    if preset_mock is not None:
        return {**preset_mock, "audit_id": make_audit_id(text)}

    # Very light heuristic fallback for arbitrary user text
    lowered = text.lower()
    triggers = {
        "riba": ["interest", "guarantee", "guaranteed return", "فائدة", "ربا"],
        "gharar": ["uncertain", "speculat", "غرر"],
        "maysir": ["gamble", "lottery", "bet "],
        "mlm": ["recruit", "referral bonus", "network marketing", "نیٹ ورک"],
        "fatwa": ["fatwa", "sheikh", "scholar ruled", "فتوى"],
    }
    matched = None
    for key, words in triggers.items():
        if any(w in lowered for w in words):
            matched = key
            break

    if matched is None:
        return {
            "result": "PASS",
            "violation": "None",
            "confidence": "MEDIUM",
            "severity": "NONE",
            "action": "ALLOW",
            "language": "Auto-detected",
            "pillar": None,
            "pillar_class": None,
            "aaoifi": None,
            "alternative": None,
            "audit_id": make_audit_id(text),
        }

    enrichment = derive_mock_enrichment(matched) or {}
    return {
        "result": "FLAGGED",
        "violation": matched.capitalize(),
        "confidence": "MEDIUM",
        "severity": "HIGH",
        "action": "ESCALATE",
        "language": "Auto-detected",
        "pillar": enrichment.get("pillar"),
        "pillar_class": enrichment.get("pillar_class"),
        "aaoifi": enrichment.get("aaoifi"),
        "alternative": enrichment.get("alternative"),
        "audit_id": make_audit_id(text),
    }


def live_classify(text: str, context: str, role: str) -> dict | None:
    """Attempt a real call to a configured MACI API. Returns None on failure."""
    if not (MACI_API_URL and HAS_REQUESTS):
        return None
    try:
        headers = {"Content-Type": "application/json"}
        if MACI_API_KEY:
            headers["X-MACI-Key"] = MACI_API_KEY
        resp = requests.post(
            MACI_API_URL,
            json={
                "text": text,
                "context": context,
                "user_role": role,
                "deployment_context": "customer_facing_tool",
            },
            headers=headers,
            timeout=15,
        )
        resp.raise_for_status()
        d = resp.json()
        ev = d.get("maci_evaluation", {})
        bb = d.get("boundary_behavior", {})
        return {
            "result": ev.get("result", d.get("result", "UNKNOWN")),
            "violation": ev.get("violation_class", d.get("violation_class", "Unknown")),
            "confidence": ev.get("confidence_band", d.get("confidence_band", "UNKNOWN")),
            "severity": ev.get("severity", d.get("severity", "UNKNOWN")),
            "action": bb.get("recommendation"),
            "language": d.get("language", "Unknown"),
            "pillar": ev.get("pillar_undermined") or ev.get("pillar"),
            "pillar_class": ev.get("pillar_class"),
            "aaoifi": ev.get("aaoifi_standard") or ev.get("aaoifi"),
            "alternative": ev.get("shariah_alternative") or ev.get("alternative"),
            "audit_id": make_audit_id(text),
        }
    except Exception:
        return None


def classify(text: str, context: str, role: str, preset_mock: dict | None) -> tuple[dict, bool]:
    """Returns (result_dict, used_live_api: bool)."""
    live = live_classify(text, context, role)
    if live is not None:
        return live, True
    return mock_classify(text, preset_mock), False


# ──────────────────────────────────────────────────────────────────────
# UI HELPERS
# ──────────────────────────────────────────────────────────────────────

def pill_class(result: str) -> str:
    r = (result or "").upper()
    if r in ("PASS", "ALLOW"):
        return "pill-pass"
    if r in ("FLAGGED", "QUARANTINE", "BLOCK"):
        return "pill-block"
    if r in ("ESCALATE", "UNCERTAIN", "REVIEW"):
        return "pill-flag"
    return "pill-neutral"


def render_packet(data: dict, text: str):
    pc = pill_class(data["result"])
    pills_html = (
        f'<span class="pill {pc}">{data["result"]}</span>'
        f'<span class="pill pill-neutral">{data["violation"]}</span>'
        f'<span class="pill pill-neutral">{data.get("language","—")}</span>'
    )
    if data.get("action"):
        pills_html += f'<span class="pill {pill_class(data["action"])}">{data["action"]}</span>'
    if data.get("pillar"):
        pills_html += '<span class="pill pill-gold">Maqasid ◈</span>'

    st.markdown(pills_html, unsafe_allow_html=True)
    st.write("")

    packet_html = f"""
    <div class="packet-card">
        <span class="comment">// MACI V.03 Signal Packet · Consequence-Boundary Review</span><br><br>
        <span class="k">"input"</span>: <span class="s">"{text[:80]}{'...' if len(text) > 80 else ''}"</span>,<br>
        <span class="k">"result"</span>: <span class="s">"{data['result']}"</span>,<br>
        <span class="k">"violation_class"</span>: <span class="s">"{data['violation']}"</span>,<br>
        <span class="k">"confidence_band"</span>: <span class="s">"{data['confidence']}"</span>,<br>
        <span class="k">"severity"</span>: <span class="s">"{data['severity']}"</span>,<br>
        {f'<span class="k">"action"</span>: <span class="s">"{data["action"]}"</span>,<br>' if data.get("action") else ""}
        <span class="k">"language"</span>: <span class="s">"{data.get('language','—')}"</span>
    </div>
    """
    st.markdown(packet_html, unsafe_allow_html=True)

    if data.get("pillar"):
        enrichment_html = f"""
        <div class="enrichment-block">
            <div class="enrichment-header">◈ V.03 Maqasid Enrichment Layer</div>
            <div class="e-label">Pillar Undermined</div>
            <div class="e-val gold">{data['pillar']}</div>
            <div class="e-label">Maqasid Pillar Class</div>
            <div class="e-val">{data.get('pillar_class') or '—'}</div>
            <div class="e-label">AAOIFI Standard</div>
            <div class="e-val">{data.get('aaoifi') or '—'}</div>
        </div>
        """
        st.markdown(enrichment_html, unsafe_allow_html=True)

        if data.get("alternative"):
            alt_html = f"""
            <div class="alt-box">
                <div class="alt-label">✓ Shariah-Compliant Structural Alternative</div>
                {data['alternative']}
            </div>
            """
            st.markdown(alt_html, unsafe_allow_html=True)

    if data.get("confidence") == "MEDIUM":
        st.markdown(
            '<div class="warning-box">⚠ MEDIUM confidence — output requires secondary '
            "review by a qualified scholar or compliance officer before any "
            "institutional action is taken.</div>",
            unsafe_allow_html=True,
        )

    st.markdown(
        f'<div class="audit-id">audit_id: {data["audit_id"]}</div>',
        unsafe_allow_html=True,
    )


# ──────────────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown(
        '<div class="version-ribbon">MACI V.03'
        '<span class="sub">Maqasid-Aligned Consequence-Boundary Review Layer</span></div>',
        unsafe_allow_html=True,
    )

    st.markdown("### Presets")
    preset_choice = st.radio(
        "Load an example",
        options=list(PRESETS.keys()),
        index=0,
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("### Context")
    context = st.selectbox("Deployment context", CONTEXT_OPTIONS, index=0)
    role = st.selectbox("User role", ROLE_OPTIONS, index=0)

    st.markdown("---")
    mode_label = "Live API" if (MACI_API_URL and HAS_REQUESTS) else "Demo mode (offline)"
    st.caption(f"Mode: **{mode_label}**")
    st.caption(
        "Set `MACI_API_URL` near the top of `app.py` to connect a live "
        "MACI endpoint. Without it, this tool runs entirely offline using "
        "preset and heuristic mock data — safe to demo with no backend."
    )


# ──────────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────────

st.markdown(
    '<div class="version-ribbon">MACI V.03 · Live Audit Tool'
    '<span class="sub">Not a fatwa engine · Not a Shariah certification body</span></div>',
    unsafe_allow_html=True,
)

st.title("Test MACI on any text")
st.caption(
    "Type or select a preset. MACI V.03 classifies it against Maqasid al-Shariah "
    "criteria and returns a consequence-boundary signal — including pillar, "
    "severity, a Shariah-compliant structural alternative, and the governing "
    "AAOIFI standard."
)

st.markdown(
    """
    <div class="disclaimer-box">
    <strong>Technical Governance Review Tool — Not a Mufti, Shariah Board, or
    Certification Body.</strong><br>
    MACI is an AI-assisted, pre-effect consequence-boundary review layer. Its
    outputs are governance indicators for institutional review — not religious
    rulings, fatwas, or legal determinations. MACI does not replace qualified
    scholars. Outputs with MEDIUM confidence require secondary review by a
    qualified scholar or compliance officer before any institutional action
    is taken. For deployment or API access, contact
    <strong>contact@maqasidai.org</strong>.
    </div>
    """,
    unsafe_allow_html=True,
)

preset_data = PRESETS[preset_choice]

col_input, col_output = st.columns([1, 1.4], gap="large")

with col_input:
    st.markdown("##### Input")
    text_input = st.text_area(
        "Text to classify — Arabic · English · Urdu · Farsi · mixed",
        value=preset_data["text"],
        height=150,
    )
    run = st.button("▶ Run Consequence-Boundary Audit", use_container_width=True)

with col_output:
    st.markdown("##### MACI V.03 Signal Packet")
    if run and text_input.strip():
        with st.spinner("Auditing..."):
            # Only use the preset's mock if the text wasn't edited
            preset_mock = (
                preset_data["mock"] if text_input.strip() == preset_data["text"].strip() else None
            )
            result, used_live = classify(text_input, context, role, preset_mock)
        if used_live:
            st.caption("✓ Response from live MACI API")
        else:
            st.caption("ⓘ Demo mode — offline preset / heuristic response")
        render_packet(result, text_input)
    else:
        st.info("Enter text and click **Run Consequence-Boundary Audit** to see the signal packet.")


st.markdown("---")
st.markdown(
    """
    <div style="text-align:center; padding: 1.5rem 0;">
        <p style="color:#6b6859; font-style:italic; font-family:'Cormorant Garamond', Georgia, serif; font-size:1.1rem;">
        MACI sits between your AI system and your institutional process —
        every decision auditable, every violation flagged with a Maqasid-enriched
        signal before it reaches your users.
        </p>
        <p style="color:#9c987f; font-size:0.7rem; letter-spacing:0.08em; text-transform:uppercase; margin-top:1.1rem;">
        Technical governance review only · Not a Shariah certification ·
        Does not constitute a fatwa or religious ruling
        </p>
        <p style="color:#b8893a; font-size:0.65rem; letter-spacing:0.12em; text-transform:uppercase; margin-top:0.4rem;">
        MACI V.03 · Audit-Facing Production-Runtime Candidate Shell
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
