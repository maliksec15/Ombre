GITHUB FILE PATH: README.md
============================================================
<div align="center">

```
 ██████╗ ███╗   ███╗██████╗ ██████╗ ███████╗
██╔═══██╗████╗ ████║██╔══██╗██╔══██╗██╔════╝
██║   ██║██╔████╔██║██████╔╝██████╔╝█████╗
██║   ██║██║╚██╔╝██║██╔══██╗██╔══██╗██╔══╝
╚██████╔╝██║ ╚═╝ ██║██████╔╝██║  ██║███████╗
 ╚═════╝ ╚═╝     ╚═╝╚═════╝ ╚═╝  ╚═╝╚══════╝
```

**Autonomous AI Reasoning Data Infrastructure**

*You bring your own AI API keys. Ombre handles everything else.*

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-green.svg)](https://python.org)
[![Tests](https://img.shields.io/badge/Tests-107%20passing-brightgreen.svg)](tests/test_all.py)
[![Contact](https://img.shields.io/badge/Enterprise-ombreaiq%40gmail.com-orange)](mailto:ombreaiq@gmail.com)

</div>

---

## What is Ombre?

Ombre is **open source AI reasoning data infrastructure**.

You point Ombre at your existing AI API keys. Ombre runs your models in parallel on hard problems, validates every reasoning trace through 4 quality tiers, indexes everything for semantic search, and exposes the entire catalog through an MCP server your agents can call directly.

**You own the models. Ombre owns the quality layer.**

---

## How It Works

```
You set your own API keys (Anthropic, OpenAI, etc.)
                    ↓
Ombre runs your models in parallel on hard problems
3 models × 3 temperatures = up to 9 traces per problem
                    ↓
4-tier validation pipeline filters every trace
Only traces scoring 85+ enter your catalog
                    ↓
Catalog indexed as dense vectors for semantic RAG search
                    ↓
Your AI agents access everything via MCP
One config block. Fully autonomous.
                    ↓
Companies billed per trace pulled
Developers use it free forever
```

---

## Your API Keys — You Stay In Control

Ombre never stores or transmits your API keys. They live in your environment. Ombre reads them locally to call your models. Nothing leaves your infrastructure.

```bash
# Set whichever you have — Ombre uses all available
export ANTHROPIC_API_KEY=sk-ant-...
export OPENAI_API_KEY=sk-...
```

That is it. Ombre automatically detects which models are available and uses all of them in parallel.

**No API keys set?** Ombre falls back to a simulated model — useful for testing the pipeline, not for production catalog data.

---

## MCP Integration

**Developers — free forever:**

```json
{
  "mcpServers": {
    "ombre": {
      "command": "python3",
      "args": ["-m", "ombre.mcp.server"],
      "env": {
        "OMBRE_MODE":          "developer",
        "ANTHROPIC_API_KEY":   "sk-ant-...",
        "OPENAI_API_KEY":      "sk-..."
      }
    }
  }
}
```

**Companies — metered billing:**

```json
{
  "mcpServers": {
    "ombre": {
      "command": "python3",
      "args": ["-m", "ombre.mcp.server"],
      "env": {
        "OMBRE_CLIENT_EMAIL":  "cto@yourcompany.com",
        "OMBRE_CLIENT_NAME":   "Your Company Name",
        "ANTHROPIC_API_KEY":   "sk-ant-...",
        "OPENAI_API_KEY":      "sk-..."
      }
    }
  }
}
```

Company accounts are created automatically on first connection. No registration form. No waiting.

---

## Available MCP Tools

```
ombre_search_traces      Filter search — domain, score, model, difficulty
ombre_rag_search         Semantic RAG search — meaning-based retrieval
ombre_rag_similar        Find traces similar to one you already have
ombre_get_trace          Full trace with reasoning steps + provenance
ombre_build_dataset      Build custom training dataset from filters
ombre_get_dataset        Retrieve a built dataset
ombre_generate_trace     Custom generation using your API keys ($0.50)
ombre_submit_problem     Submit problem for solving (free)
ombre_get_billing        Billing summary + payment info
ombre_catalog_stats      Live catalog statistics
ombre_rag_index_stats    RAG index health
```

---

## Install

```bash
pip install git+https://github.com/ombreaiq/ombre.git
```

**Start the server:**

```bash
export ANTHROPIC_API_KEY=sk-ant-...
python3 -m ombre
# Dashboard → http://localhost:8080
```

**Run tests:**

```bash
python3 tests/test_all.py
# 107 tests. All pass.
```

**Run the demo:**

```bash
python3 examples/quickstart.py
```

---

## The 4-Tier Validation System

Every trace must pass all four tiers before entering the catalog.

| Tier | Weight | What It Checks |
|---|---|---|
| T1 — Automated | 20% | Answer correctness, step consistency, hallucination detection |
| T2 — Consensus | 25% | Do multiple models agree on the reasoning path? |
| T3 — Human review | 35% | 3 reviewers, 2/3 agreement threshold |
| T4 — Adversarial | 20% | Problem perturbation, logical gap detection |

**Final score = T1×0.20 + T2×0.25 + T3×0.35 + T4×0.20**

- Score **< 85** → Rejected. Never reaches the catalog.
- Score **85–94** → Standard. $0.08 per retrieval.
- Score **95+** → Premium. $0.24 per retrieval (3× multiplier, automatic).

---

## Pricing

| Action | Rate |
|---|---|
| Standard trace retrieval | $0.08 |
| Premium trace retrieval (95+) | $0.24 — 3× auto |
| Custom generation | $0.50 per request |
| Dataset build | $0.08 per trace |
| **Monthly minimum** | **$5,000 per company** |
| **Developers** | **Free forever** |

---

## Payment

End of month — payment page appears automatically in your dashboard. Click **Email Ombre To Pay**. Your email client opens pre-filled with your statement ID and amount due. Send it to [ombreaiq@gmail.com](mailto:ombreaiq@gmail.com). We reply within 24 hours with payment details.

---

## Trust & Safety

Every trace has a full immutable audit trail. Every delivery includes a SHA-256 cryptographic hash clients can verify.

```
GET /v1/trust/audit/{trace_id}   Full immutable audit trail
GET /v1/trust/data-card          Public data card (live data)
GET /v1/trust/model-card         Model configs and known biases
GET /v1/trust/security           Security posture documentation
GET /v1/trust/stats              Live catalog statistics
```

---

## Domains Covered

| Domain | Generation Cost | Use Cases |
|---|---|---|
| Mathematics | $2/trace | Theorem proving, calculus, algebra |
| Code | $3/trace | Algorithms, data structures, optimization |
| Science | $8/trace | Physics, chemistry, biology |
| Medicine | $15/trace | Clinical reasoning, diagnostics |
| Finance | $12/trace | Quantitative analysis, risk modeling |
| Logic | $5/trace | Formal reasoning, proofs |

---

## Architecture

```
Your API Keys (Anthropic, OpenAI)
         ↓
┌─────────────────────────────────────────┐
│              OMBRE ENGINE               │
│                                         │
│  Ingestion   → Dedup → Difficulty score │
│  Generation  → Multi-model parallel     │
│  Validation  → 4-tier quality filter    │
│  RAG Index   → Dense vector search      │
│  Billing     → Per-call metering        │
│  MCP Server  → 11 tools for agents      │
│  Trust Layer → Audit trails + hashes    │
│  Dashboard   → http://localhost:8080    │
│                                         │
│    SQLite (dev) / PostgreSQL (prod)     │
└─────────────────────────────────────────┘
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). New provider connectors, domain scrapers, and validation improvements are welcome.

---

## License

Apache License 2.0 — see [LICENSE](LICENSE).

Enterprise contact: [ombreaiq@gmail.com](mailto:ombreaiq@gmail.com)

---

<div align="center">

**You bring the models. Ombre brings the quality.**

[ombreaiq@gmail.com]

</div>
