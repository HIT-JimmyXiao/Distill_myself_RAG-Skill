# Distill Myself RAG-Skill

An open-source repository for turning sanitized contact summaries into RAG bundles, Codex skill templates, and automation-facing workflow scaffolds. This repository assumes the upstream repository has already produced redacted inputs.

[中文 README](README.md)

## Overview

This repository only accepts sanitized structured inputs.

Its outputs are:

- `rag_docs.jsonl`
- `skill_summary.json`
- `SKILL.template.md`

It does not publish:

- raw chat texts,
- real names or `wxid`,
- local runtime states,
- private live-reply automation logs.

## Upstream Dependency

Run the upstream repository first:

- [Distill_myself_wechat_history_extrate](https://github.com/HIT-JimmyXiao/Distill_myself_wechat_history_extrate)

## Quick Start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .

distill-rag-skill init-workspace --workspace ./demo_workspace
distill-rag-skill build-rag-bundle --contacts ./examples/contacts_sanitized.example.json --workspace ./demo_workspace
distill-rag-skill render-skill-template --workspace ./demo_workspace --output ./demo_workspace/outputs/SKILL.open_source.md
```

## Repository Layout

```text
Distill_myself_RAG-Skill/
├── docs/
├── examples/
├── src/distill_myself_rag_skill/
├── templates/skill/
├── LICENSE
├── README.md
├── README_EN.md
└── pyproject.toml
```

## Scope Boundary

This repository focuses on:

- converting sanitized contacts into compact RAG docs,
- generating a skill summary for human review,
- drafting a generic Codex skill template.

It intentionally avoids:

- raw message ingestion,
- personal identity data,
- automatic message delivery,
- private runtime state.

