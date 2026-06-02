from __future__ import annotations

import argparse
import json
from pathlib import Path

from .bundle import build_rag_bundle, init_workspace, load_contacts, render_skill_template, write_json, write_rag_docs


def package_root() -> Path:
    return Path(__file__).resolve().parents[2]


def default_template_path() -> Path:
    return package_root() / "templates" / "skill" / "SKILL.template.md"


def cmd_init_workspace(args: argparse.Namespace) -> None:
    result = init_workspace(Path(args.workspace), default_template_path())
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_build_rag_bundle(args: argparse.Namespace) -> None:
    workspace = Path(args.workspace).resolve()
    init_workspace(workspace, default_template_path())
    contacts = load_contacts(Path(args.contacts))
    rag_docs, summary = build_rag_bundle(contacts)
    write_rag_docs(workspace / "outputs" / "rag_docs.jsonl", rag_docs)
    write_json(workspace / "outputs" / "skill_summary.json", summary)
    print(
        json.dumps(
            {
                "status": "ok",
                "rag_docs": str((workspace / "outputs" / "rag_docs.jsonl").resolve()),
                "summary": str((workspace / "outputs" / "skill_summary.json").resolve()),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def cmd_render_skill_template(args: argparse.Namespace) -> None:
    workspace = Path(args.workspace).resolve()
    summary_path = workspace / "outputs" / "skill_summary.json"
    if not summary_path.exists():
        raise FileNotFoundError(f"summary not found: {summary_path}")
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    template_path = Path(args.template).resolve() if args.template else workspace / "skill" / "SKILL.template.md"
    output_path = Path(args.output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_skill_template(summary, template_path), encoding="utf-8")
    print(json.dumps({"status": "ok", "output": str(output_path)}, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Sanitized RAG / skill bundle builder")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init-workspace")
    init_parser.add_argument("--workspace", required=True)
    init_parser.set_defaults(func=cmd_init_workspace)

    bundle_parser = subparsers.add_parser("build-rag-bundle")
    bundle_parser.add_argument("--contacts", required=True)
    bundle_parser.add_argument("--workspace", required=True)
    bundle_parser.set_defaults(func=cmd_build_rag_bundle)

    render_parser = subparsers.add_parser("render-skill-template")
    render_parser.add_argument("--workspace", required=True)
    render_parser.add_argument("--output", required=True)
    render_parser.add_argument("--template")
    render_parser.set_defaults(func=cmd_render_skill_template)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
