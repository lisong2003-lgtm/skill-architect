---
name: skill-architect-conversation-2026-08-20-长对话快照
description: 把长对话压缩成快照和技能包，供新对话按需加载。
---

# 长对话快照

## 适用场景

- 长对话积累了多个结论、决策和待办。
- 新对话不想加载完整聊天记录。
- 需要保留核心上下文并继续同类工作。

## 核心方法

- 导出长对话为 transcript。
- 运行 conversation_architect.py。
- 生成 conversation-snapshot.md。
- 按主题生成技能包和 routing-index.md。
- 新对话只读取快照和对应技能包。

## 边界

- 快照用于新对话，不压缩当前对话框。
- 新对话应说“先读取 conversation-output/conversation-snapshot.md 和 routing-index.md”。
- 快照是决策依据，不是替代完整审计。

## 来源

- `conversation-snapshot.md`
