# Skill Workflow

## Recommended Steps

1. 在上游仓库完成 `scan -> redact -> tier`
2. 把去敏后的联系人统计文件传入本仓库
3. 生成 `rag_docs.jsonl`
4. 生成 `skill_summary.json`
5. 渲染 `SKILL.template.md`
6. 在本地把模板改成你自己的私有 `SKILL.md`

## Why Not Publish A Full Personal Skill

因为真正可用的私人 skill 一定会包含：

- 个人画像
- 关系证据
- 私有表达习惯
- 真实运行时路径与工具状态

这些都不应该直接开源。

