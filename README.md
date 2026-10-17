# Document Evidence Review

A focused Streamlit app that compares a claim with PDF/text evidence using Snowflake Cortex,
then rejects fabricated citations by checking each quote against its source text.

This public edition refactors an earlier specialised document-review workflow into a smaller,
domain-neutral example. It does not include the original licensing rules, guide database,
OCR/deployment framework or automated eligibility decisions.

## Architecture

Upload PDF/TXT → extract text locally → build bounded evidence prompt → Cortex JSON response →
validate schema and exact source quotations → inspect/download JSON.

Exact quotation checks establish that a quote exists, not that the conclusion is correct.
A person must assess whether each citation supports the claim.

## Setup

Requires Python 3.11+ and your own Snowflake account, warehouse, Cortex-enabled role and supported model.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Fill in your Snowflake account, role, warehouse, key file path and MODEL_NAME.
streamlit run app.py
```

Keep the private key outside the repository. Configure its passphrase through the environment.
On Windows use `.venv\Scripts\activate`. Try `examples/evidence.txt` and the claim
“The demonstration sensor was calibrated on 2026-01-10.”

Maximum file size is 10 MB; combined extracted evidence is limited to 60,000 characters. Scanned
PDFs need OCR before upload. Extracted text is sent to your configured Snowflake service; use
synthetic or authorised documents and verify your account's retention, model and region settings.

## Validation

```bash
python -m unittest discover -s tests -v
python -m compileall -q .
```

6 offline tests pass for citation validation, missing evidence and input limits. Live Cortex calls,
OCR and production deployment have not been tested as part of this public release.

## Public edition

This is a separately prepared portfolio edition with fresh history. Private deployment settings,
credentials, operational records, uploads, backups and organisation-specific assets are excluded.
See [PUBLIC_EDITION.md](PUBLIC_EDITION.md). No deployment workflows are included.
