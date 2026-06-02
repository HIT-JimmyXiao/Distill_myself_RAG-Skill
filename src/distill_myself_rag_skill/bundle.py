from __future__ import annotations

import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from string import Template
from typing import Any


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def ensure_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item)]
    if value in (None, ""):
        return []
    return [str(value)]


def init_workspace(workspace: Path, template_path: Path) -> dict[str, Any]:
    workspace = workspace.resolve()
    created = [
        workspace / "inputs" / "sanitized",
        workspace / "outputs",
        workspace / "skill",
    ]
    for path in created:
        path.mkdir(parents=True, exist_ok=True)
    target_template = workspace / "skill" / "SKILL.template.md"
    if not target_template.exists():
        target_template.write_text(template_path.read_text(encoding="utf-8"), encoding="utf-8")
    return {"status": "ok", "workspace": str(workspace), "created": [str(path) for path in created]}


def load_contacts(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    contacts = payload if isinstance(payload, list) else payload.get("contacts", [])
    if not isinstance(contacts, list):
        raise ValueError("contacts input must be a list or an object with a contacts list")
    return [item for item in contacts if isinstance(item, dict)]


def infer_tone_hint(contact: dict[str, Any]) -> str:
    tone_hint = str(contact.get("tone_hint", "")).strip()
    if tone_hint:
        return tone_hint
    relation_tags = set(ensure_list(contact.get("relation_tags")))
    if "close_peer" in relation_tags:
        return "casual_direct"
    if "collaborator" in relation_tags:
        return "task_oriented"
    if "group_reference" in relation_tags:
        return "reference_only"
    return "neutral_compact"


def build_rag_bundle(contacts: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    topic_counter: Counter[str] = Counter()
    tier_counter: Counter[str] = Counter()
    rag_docs: list[dict[str, Any]] = []
    for index, contact in enumerate(contacts, start=1):
        public_contact_id = str(contact.get("public_contact_id") or f"contact_{index:04d}")
        tier = str(contact.get("tier") or "Reference")
        topic_tags = ensure_list(contact.get("topic_tags"))
        relation_tags = ensure_list(contact.get("relation_tags"))
        style_notes = ensure_list(contact.get("style_notes"))
        tone_hint = infer_tone_hint(contact)
        topic_counter.update(topic_tags)
        tier_counter.update([tier])
        content = (
            f"contact_id={public_contact_id}\n"
            f"tier={tier}\n"
            f"message_count={int(contact.get('message_count', 0) or 0)}\n"
            f"topic_tags={', '.join(topic_tags) if topic_tags else 'none'}\n"
            f"relation_tags={', '.join(relation_tags) if relation_tags else 'none'}\n"
            f"style_notes={', '.join(style_notes) if style_notes else 'none'}\n"
            f"tone_hint={tone_hint}"
        )
        rag_docs.append(
            {
                "doc_id": f"contact::{public_contact_id}",
                "bucket": "contact_profile",
                "entity_key": public_contact_id,
                "title": f"sanitized_profile::{public_contact_id}",
                "content": content,
                "metadata_json": json.dumps(
                    {
                        "tier": tier,
                        "topic_tags": topic_tags,
                        "relation_tags": relation_tags,
                        "style_notes": style_notes,
                        "tone_hint": tone_hint,
                    },
                    ensure_ascii=False,
                ),
            }
        )
    summary = {
        "generated_at": now_iso(),
        "contact_count": len(contacts),
        "tier_counts": dict(sorted(tier_counter.items())),
        "top_topics": [topic for topic, _ in topic_counter.most_common(6)],
        "workflow_steps": [
            "Run the upstream repository to produce sanitized contact summaries",
            "Build rag_docs.jsonl from sanitized contact tags",
            "Render a local SKILL.md from the template and review it manually",
            "Keep all identity-specific evidence on local disk only",
        ],
    }
    return rag_docs, summary


def write_rag_docs(path: Path, docs: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in docs:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def render_skill_template(summary: dict[str, Any], template_path: Path) -> str:
    template = Template(template_path.read_text(encoding="utf-8"))
    workflow_steps = "\n".join(f"- {step}" for step in summary.get("workflow_steps", []))
    return template.safe_substitute(
        upstream_repo="https://github.com/HIT-JimmyXiao/Distill_myself_wechat_history_extrate",
        workflow_steps=workflow_steps,
        contact_count=summary.get("contact_count", 0),
        tier_counts=json.dumps(summary.get("tier_counts", {}), ensure_ascii=False),
        top_topics=", ".join(summary.get("top_topics", [])) or "none",
    )

