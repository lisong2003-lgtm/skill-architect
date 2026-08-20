---
name: skill-architect-conversation-2026-08-20-skill-architect发布
description: 把架构外移流程发布为可复用 Codex Skill。
---

# skill-architect发布

## 适用场景

- 想把已完成流程打包成可发布 Skill。
- 需要让其他用户解决同样的 SKILL.md 过大问题。
- 需要生成发布目录、manifest 和 zip。

## 核心方法

- 建立独立发布目录。
- 包含 SKILL.md、scripts、templates、references、examples。
- 添加 README、LICENSE、manifest.json。
- 运行 self_test.py 自测。
- 打包 zip。
- 检查发布包无私密路径。

## 边界

- 发布版不包含原始书籍、私人日志、个人数据。
- 发布前确认作者名、版本号和许可证。
- 安装版与公开版要同步。

## 来源

- `conversation-snapshot.md`
