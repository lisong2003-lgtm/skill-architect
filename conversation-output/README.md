# 对话快照使用说明

这段长对话已经归纳为快照和主题技能包，用于新对话减少 Token。

## 文件

- `conversation-snapshot.md`：核心结论、关键决策、待办、边界。
- `routing-index.md`：主题路由。
- `skills/*/SKILL.md`：按主题拆分的技能包。

## 新对话用法

在新对话框中说：

```text
继续讨论 <问题>。先读取 conversation-output/conversation-snapshot.md 和 conversation-output/routing-index.md，按需加载对应技能包，不要复制旧对话全文。
```

## 边界

- 快照用于新对话，不压缩当前对话框。
- 当前对话框继续使用时，仍使用当前上下文。
