#!/usr/bin/env python3
"""Sync canonical agent rules from .agent-rules/ to all tool-specific config files.

Usage:
    python .agent-rules/sync_agent_rules.py

Targets:
    CLAUDE.md                    — Claude Code
    AGENTS.md                    — General AI agents (Codex, etc.)
    .cursor/rules/00_synced.mdc  — Cursor (alwaysApply)

Customization:
    Edit the CLAUDE_HEADER, AGENTS_HEADER, and CURSOR_FRONTMATTER constants below
    to match your project name and commands, then run this script.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
RULES_DIR = REPO_ROOT / ".agent-rules"


def load_canonical() -> str:
    files = sorted(f for f in RULES_DIR.glob("*.md"))
    if not files:
        raise FileNotFoundError(f"No .md files found in {RULES_DIR}")
    sections = []
    for f in files:
        sections.append(f.read_text(encoding="utf-8").strip())
    return "\n\n---\n\n".join(sections)


SYNC_NOTE = (
    "<!-- AUTO-GENERATED — edit .agent-rules/*.md and run "
    "`.venv/bin/python .agent-rules/sync_agent_rules.py` to update -->"
)

# ─────────────────────────────────────────────────────────────────────────────
# CUSTOMIZE: Replace {{PROJECT_NAME}} and the Commands block for your project.
# ─────────────────────────────────────────────────────────────────────────────
CLAUDE_HEADER = """\
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

<!-- AUTO-GENERATED — edit .agent-rules/*.md and run `.venv/bin/python .agent-rules/sync_agent_rules.py` to update -->

## Commands

```bash
# {{PROJECT_COMMANDS_DESCRIPTION}}
# Example — replace with your project's actual commands:

# Run tests
.venv/bin/pytest tests/

# Single test
.venv/bin/pytest tests/path/to/test_file.py::test_name -v

# Sync agent rules after editing .agent-rules/
.venv/bin/python .agent-rules/sync_agent_rules.py
```

Allowed tools per `.claude/settings.local.json`: see that file for the full list.

## Codex 代码审查（Claude Code 专用）

当「代码审查（Codex Review Gate）」规则触发时，使用以下 MCP 工具调用 Codex：

```
mcp__codex__codex({
  prompt: "<审查要求与待审查代码的上下文>",
  sandbox: "read-only",
  cwd: "<项目根目录>"
})
```

- 始终使用 `read-only` sandbox，确保审查过程不修改文件
- 如需对审查结果追问，使用 `mcp__codex__codex-reply` 传入 `threadId`
- 审查 prompt 应包含：改动摘要、涉及文件、需关注的审查重点

---
"""

AGENTS_HEADER = """\
# {{PROJECT_NAME}} — AI Coding Agent 指令

<!-- AUTO-GENERATED — edit .agent-rules/*.md and run `.venv/bin/python .agent-rules/sync_agent_rules.py` to update -->

> 适用于 Claude Code / Cursor / Codeium 等所有 AI coding agent。
> Cursor 用户另见 `.cursor/rules/` 获取完整规则。
> 规则修改请编辑 `.agent-rules/*.md` 后运行 `.venv/bin/python .agent-rules/sync_agent_rules.py`。

---
"""

CURSOR_FRONTMATTER = """\
---
description: >-
  {{PROJECT_NAME}} 全局规则（Auto-synced from .agent-rules/）
  编辑 .agent-rules/*.md 后运行 .venv/bin/python .agent-rules/sync_agent_rules.py
alwaysApply: true
---

"""
# ─────────────────────────────────────────────────────────────────────────────


def write_if_changed(path: Path, content: str) -> None:
    if path.exists() and path.read_text(encoding="utf-8") == content:
        print(f"  [unchanged] {path.relative_to(REPO_ROOT)}")
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"  [updated]   {path.relative_to(REPO_ROOT)}")


def main() -> None:
    canonical = load_canonical()
    md_files = sorted(f for f in RULES_DIR.glob("*.md"))
    print(f"Loaded {len(md_files)} canonical files from .agent-rules/\n")

    targets = [
        (REPO_ROOT / "CLAUDE.md",                         CLAUDE_HEADER + canonical + "\n"),
        (REPO_ROOT / "AGENTS.md",                         AGENTS_HEADER + canonical + "\n"),
        (REPO_ROOT / ".cursor/rules/00_synced.mdc",       CURSOR_FRONTMATTER + canonical + "\n"),
    ]

    print("Syncing:")
    for path, content in targets:
        write_if_changed(path, content)

    print("\nDone. Commit all changed files together.")


if __name__ == "__main__":
    main()
