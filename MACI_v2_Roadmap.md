# MACI v2.5 — RAG & Agentic AI Roadmap
### For Founders, CTOs, and Fintech Partners

> This document describes the technical vision for MACI beyond v1.0. For the current implementation, see the main README.

---

## The Problem with Static Rules

MACI v1.0 works. It catches Riba keywords, fake fatwa signals, and Gharar patterns in AI outputs using a rule-based engine. But Islamic jurisprudence is not a static keyword list. A financial product can be structured to be technically Riba-free in its language while being Riba-adjacent in its economic effect. A modern AI system can avoid every flagged phrase while still producing a ruling that no qualified scholar would sanction.

Static rules break at the edges. The next version of MACI does not.

---

## RAG — Retrieval-Augmented Generation in MACI

In MACI v2.5, before scoring any AI output, the audit pipeline first retrieves relevant content from a verified knowledge base — authenticated fatwa collections, AAOIFI standards, OIC Fiqh Academy resolutions — and uses that retrieved content as grounding for its compliance decision.

```
AI system output
       ↓
MACI receives the output text
       ↓
Retrieval engine queries:
   → Authenticated fatwa corpus (Dar al-Ifta Egypt, IslamWeb, etc.)
   → Scholarly consensus database
   → AAOIFI Shariah standards for financial products
   → MACI historical audit findings
       ↓
Retrieved context passed to MACI reasoning model
       ↓
Model compares output against authoritative retrieved content
       ↓
MACI score + citations + flagged contradictions
```

When a fintech's AI tells a user "this murabaha structure is Shariah-compliant," MACI v2.5 retrieves the relevant AAOIFI standard, the most recent fatwa on that product category, and prior scholarly rulings — then evaluates whether the AI's claim is substantiated. If not, MACI flags it, cites the specific source it contradicts, and recommends the correction.

This is the difference between a spell-checker and a compliance officer.

### Knowledge base sources

- Authenticated fatwa collections from major Islamic institutions
- AAOIFI standards
- OIC Fiqh Academy resolutions
- Peer-reviewed Islamic finance research
- MACI's own growing audit history (anonymised)

All sources are manually verified. No AI-generated religious content enters the corpus.

---

## Agentic MACI — Autonomous Audit Operations

```
Fintech AI produces 10,000 outputs per day
          ↓
MACI agent monitors all outputs at the output layer
          ↓
98% pass — logged, no action
          ↓
2% flagged — MACI retrieves relevant scholarly sources,
             scores the violation, categorises severity
          ↓
Severity 1 (Critical): instant alert to compliance team
Severity 2 (Warning):  added to daily digest report
Severity 3 (Advisory): included in monthly audit summary
          ↓
Compliance team reviews, approves or escalates
          ↓
MACI records resolution and updates certification status
```

### Tools the MACI agent uses autonomously

| Tool | Purpose |
|---|---|
| `fatwa_retriever` | Query authenticated fatwa corpus for relevant rulings |
| `aaoifi_lookup` | Retrieve applicable AAOIFI standard for a financial product |
| `fake_fatwa_shield` | Run the proprietary classifier on any religious claim |
| `score_calculator` | Compute per-pillar MACI score and generate findings |
| `alert_dispatcher` | Send severity-graded alerts to compliance contacts |
| `report_generator` | Produce formatted PDF audit reports on demand |
| `audit_logger` | Write timestamped records to the compliance ledger |

---

## Why MACI is Not Replaceable by General AI

**1. General LLMs hallucinate religious authority.** You cannot use the system that creates fake fatwas to detect fake fatwas.

**2. General LLMs have no authenticated knowledge base.** MACI's corpus is manually verified. A general model trained on the internet cannot distinguish authentic scholarship from misinformation.

**3. General LLMs cannot produce a legally defensible audit trail.** A prompt-response from ChatGPT is not a compliance document.

---

## Planned API (v2.0)

```json
POST /v1/audit
{
  "text": "AI output here",
  "context": "fintech | religious | general",
  "pillar_focus": ["hifz_al_mal", "hifz_al_din"]
}
```

Response:
```json
{
  "maci_score": 32,
  "certification_status": "needs_improvement",
  "pillars": {
    "hifz_al_din": { "score": 2, "flags": ["unverified_fatwa_claim"] },
    "hifz_al_mal": { "score": 8, "flags": [] }
  },
  "citations": ["AAOIFI FAS 2, §4.3", "Dar al-Ifta fatwa #7821"],
  "remediation": ["Replace unverified ruling with authenticated source"]
}
```

---

## Capability Roadmap

| Capability | v1.0 (Now) | v2.0 (API) | v2.5 (Agentic) |
|---|---|---|---|
| Riba / Gharar detection | ✅ Rule-based | ✅ Enhanced | ✅ Continuous |
| Fake fatwa detection | ✅ Rule-based | ✅ ML classifier | ✅ RAG-grounded |
| Audit report | ✅ Manual | ✅ API-generated | ✅ Autonomous |
| Scholarly citations | ❌ | ✅ | ✅ |
| Real-time monitoring | ❌ | Partial | ✅ |
| Compliance alert system | ❌ | ❌ | ✅ |
| Regulatory audit trail | ❌ | ✅ | ✅ |

---

## Contact

**Syeda Beenish Fatima** — Founder, MaqasidAI
syedabeenishf.14@gmail.com · maqasidai.org
