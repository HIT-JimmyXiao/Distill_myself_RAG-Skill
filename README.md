# Distill Myself RAG-Skill

把去敏后的联系人分层结果继续变成个人 skill / RAG / Codex 自动化骨架的公开仓库。这个仓库默认依赖上游 [`Distill_myself_wechat_history_extrate`](https://github.com/HIT-JimmyXiao/Distill_myself_wechat_history_extrate) 先准备好安全化输入。

[English README](README_EN.md)

## Overview

这个仓库只接收“去敏后的结构化输入”，不直接处理原始微信数据。

目标是把上游仓库产出的联系人摘要继续转成：

- `rag_docs.jsonl`
- `skill_summary.json`
- `SKILL.template.md`
- 一套适合在 Codex 里继续手工完善的自动化接口骨架

## Why A Second Repository

把流程拆成第二个仓库，是为了明确两层边界：

1. 上游仓库负责导出、去敏、分层
2. 本仓库负责 RAG 文档、skill 模板、Codex 自动化接口

这样不会把“个人聊天原始事实”直接跟“自动回复/记忆技能”绑死在同一公开仓库里。

## Highlights

- 强制要求先经过上游仓库的去敏产物
- 用结构化标签而不是原始聊天文本构建 RAG 文档
- 自动生成一版可继续手工修改的 `SKILL.template.md`
- 保留 Codex / ChatGPT Computer Use 的接口边界，但不公开任何私人运行时状态

## Repository Layout

```text
Distill_myself_RAG-Skill/
├── docs/
│   ├── architecture.md        # 两仓库协作架构
│   ├── privacy_boundary.md    # 公开版边界
│   └── skill_workflow.md      # 从上游结果到 skill 模板
├── examples/
│   └── contacts_sanitized.example.json
├── src/
│   └── distill_myself_rag_skill/
│       ├── bundle.py          # RAG 文档与摘要构建
│       └── cli.py             # CLI 入口
├── templates/
│   └── skill/
│       └── SKILL.template.md  # 通用 skill 模板
├── LICENSE
├── README.md
├── README_EN.md
└── pyproject.toml
```

## Workflow

### Step 0. 先跑上游仓库

先在上游仓库里拿到这些文件：

- `export_manifest.redacted.json`
- `contact_tiers.json`
- `pipeline_handoff.md`

也就是先跑：

- [Distill_myself_wechat_history_extrate](https://github.com/HIT-JimmyXiao/Distill_myself_wechat_history_extrate)

### Step 1. 初始化公开工作区

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .

distill-rag-skill init-workspace --workspace ./demo_workspace
```

### Step 2. 生成 RAG bundle

```bash
distill-rag-skill build-rag-bundle \
  --contacts ./examples/contacts_sanitized.example.json \
  --workspace ./demo_workspace
```

会生成：

- `demo_workspace/outputs/rag_docs.jsonl`
- `demo_workspace/outputs/skill_summary.json`

### Step 3. 渲染 skill 模板

```bash
distill-rag-skill render-skill-template --workspace ./demo_workspace --output ./demo_workspace/outputs/SKILL.open_source.md
```

这一步不会替你伪造私人记忆，它只会生成一份“如何把结构化联系人摘要接入 skill”的公开模板。

如果你在 Windows 的中文路径下运行，且终端对相对路径解析出现编码异常，优先直接传绝对路径。

## Input Contract

每个联系人只保留这些公开安全字段：

- `public_contact_id`
- `tier`
- `message_count`
- `topic_tags`
- `relation_tags`
- `style_notes`
- `tone_hint`

不接收：

- 原始聊天全文
- 真实姓名、备注、`wxid`
- 私有日志、会话缓存、发送记录

## Codex Skill Boundary

这个仓库公开的是“skill 如何组织”的方法，不是你的私人 skill 本体。

推荐流程：

1. 用本仓库生成 `SKILL.template.md`
2. 在本地复制成你自己的私有 `SKILL.md`
3. 只在本地再接入真实个人画像、关系证据和运行时工具

## Notes

- 公开版默认不自动发送消息
- 公开版默认不包含任何 live WeChat UI 控制逻辑
- 公开版只保留“RAG 文档生成 + skill 模板化 + 工作流说明”三部分
