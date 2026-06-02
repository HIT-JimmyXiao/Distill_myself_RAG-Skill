# Privacy Boundary

## Public Inputs Only

本仓库只能处理这些字段：

- `public_contact_id`
- `tier`
- `message_count`
- `topic_tags`
- `relation_tags`
- `style_notes`
- `tone_hint`

## Must Stay Local

以下内容不能公开：

- 原始消息全文
- 真实联系人映射表
- 任何数据库、key、pending reply 队列
- 真实个人画像与联系人画像 JSON
- 具体 live UI 自动回复记录

## Review Principle

如果某份 RAG 文档仍然可以让人推回真实联系人，就说明去敏还不够。

