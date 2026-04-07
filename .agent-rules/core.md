# 项目核心规则

## 项目定位

<!-- {{PROJECT_DESCRIPTION}} — 用一段话描述项目背景、类型（科研 / 工程 / 混合）、核心目标 -->

**项目名称**：{{PROJECT_NAME}}

**主要贡献 / 目标**：

| # | 方向 | 关键词 |
|---|------|--------|
| C1 | {{CONTRIBUTION_1}} | {{KEYWORDS_1}} |
| C2 | {{CONTRIBUTION_2}} | {{KEYWORDS_2}} |
| C3 | {{CONTRIBUTION_3}} | {{KEYWORDS_3}} |

<!-- 如贡献不足 3 条，删减对应行即可 -->

目标：{{TARGET_GOAL}}（例：投稿会议、交付产品、完成课题）

## 开发阶段分离（如适用）

<!-- 若项目有明确的阶段边界（例如研究阶段 → 部署阶段），在此声明，Agent 不得混淆阶段约束 -->

**阶段一 — {{PHASE_1_NAME}}**：{{PHASE_1_DESCRIPTION}}
此阶段**不考虑** {{PHASE_1_IGNORE_CONSTRAINTS}} 约束。

**阶段二 — {{PHASE_2_NAME}}**：{{PHASE_2_DESCRIPTION}}
仅在阶段一完成后启动。

> 如无阶段分离需求，删除本节。

## Python 环境

**始终使用项目虚拟环境 `.venv/`（Python {{PYTHON_VERSION}}）**，禁止使用系统 Python。

所有 `python`、`pytest`、`pip` 命令必须使用 `.venv/bin/` 前缀，或在已激活虚拟环境的 shell 中执行：

```bash
source .venv/bin/activate   # 激活
.venv/bin/python ...        # 直接调用（推荐，确保隔离）
```

## 目录规范

<!-- 根据项目实际结构调整，保持与真实目录一致 -->

```
src/             # 主要源代码
scripts/         # 可执行脚本（训练 / 评估 / 构建 / 工具）
tests/           # 测试，镜像 src/ 结构
data/            # 数据集（原始 / 处理后 / 标注）
experiments/     # 实验结果与日志
.planning/       # 所有规划文件（按任务命名）
.cursor/         # IDE 与 Agent 会话状态（memory/、task_plan.md 等）
docs/            # 文档
```

- 禁止在根目录创建 `.py` 文件
- 大二进制文件（权重、原始数据）不提交 Git
- 上游依赖通过 git submodule 或包管理引入，不直接复制源码

## Claude Code 记忆存储规范

Claude Code 的持久化记忆文件必须保存在项目目录下，不使用全局路径：

- **记忆根目录**：`.cursor/memory/`
- **索引文件**：`.cursor/memory/MEMORY.md`（仅包含指向各记忆文件的链接，不写记忆内容）
- **记忆文件命名**：`{type}_{topic}.md`，例如 `feedback_planning_location.md`
- **禁止**使用 `~/.claude/` 或任何项目目录之外的路径存储记忆

每个记忆文件使用如下 frontmatter 格式：

```markdown
---
name: 记忆名称
description: 一句话描述（用于判断未来会话的相关性）
type: user | feedback | project | reference
---

内容
```
