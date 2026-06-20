# MACI V.03 — Streamlit Live Audit Tool

A Streamlit version of the MACI live demo, matching the web tool at
`maqasidai.org/demo-maci`.

## What this is

MACI is a technical, pre-effect consequence-boundary review layer.
**It does not issue fatwas, replace scholars, or certify Shariah compliance.**
This demo lets you type or select example text and see the V.03 Signal Packet
the system would return, including the Maqasid enrichment layer
(pillar undermined, severity × confidence, Shariah-compliant structural
alternative, and governing AAOIFI standard).

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```

It will open at `http://localhost:8501`.

## Modes

- **Demo mode (default)** — runs fully offline. The six presets each carry
  hand-written mock enrichment data, and free-typed text runs through a
  light keyword heuristic so the tool still returns something sensible.
  No backend or API key required — safe to hand to anyone for a demo.

- **Live API mode** — open `app.py` and set:

  ```python
  MACI_API_URL = "https://api.maqasidai.com/v1/classify"
  MACI_API_KEY = "your-maci-key"
  ```

  near the top of the file. When set, the app will call your real MACI
  endpoint first and only fall back to demo mode if that call fails
  (e.g. cold start, network issue).

## Files

- `app.py` — the Streamlit app
- `requirements.txt` — `streamlit` + `requests`

## Notes

- Styling mirrors the dark/gold theme used across the rest of the
  maqasidai.org site (IBM Plex Mono, the same gold/green/red/amber palette).
- The disclaimer banner and footer text intentionally match the corrected
  language used on the rest of the site: governance review language only,
  no certification or fatwa-issuance claims.
- MEDIUM confidence results always surface the secondary-review warning.
