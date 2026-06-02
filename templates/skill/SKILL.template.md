---
name: personal-wechat-skill-template
description: Build a private local reply and memory skill from sanitized contact summaries instead of raw chat logs.
---

# Personal WeChat Skill Template

## Upstream Dependency

Run the upstream repository first:

- $upstream_repo

## Public Boundary

- Only ingest sanitized summaries
- Never commit raw chat logs
- Never commit real names, wxid, runtime keys, or session logs

## Suggested Workflow

$workflow_steps

## Current Public Summary

- contact_count: $contact_count
- tier_counts: $tier_counts
- top_topics: $top_topics

## What Stays Local

- full self profile
- real relation evidence
- private examples
- live reply runtime

