# Skill Architect 技能架构师

Skill Architect 是一个可复用、可发布的 Codex Skill，用于把过大的 `SKILL.md` 从“整本常驻”改成“目录 + 路由索引 + 按需读取技能包”。它覆盖审计、备份、抽取、路由、验证和回滚，定位是架构级瘦身，不是简单压缩文字。

## 发布结构

- `public/skill-architect-public/`：公开发布版 Skill
- `public/skill-architect-public-0.2.0.zip`：发布压缩包
- `public/skill-architect-generic/`：跨 Agent 通用版 Skill
- `public/skill-architect-generic-0.2.0.zip`：跨 Agent 通用版压缩包
- `docs/产品说明.md`：面向使用者的产品说明
- `docs/使用说明.md`：面向使用者的操作说明
- `docs/平台发布材料.md`：SkillHub、扣子、GitHub 发布材料
- `docs/制作过程.md`：制作该 Skill 的对话脉络和关键决策
- `docs/发布清单.md`：发布前检查与核对结果

通用版不绑定 Codex，任何能读取 Markdown 并运行 Python 3.9+ 脚本的 Agent 都可以接入；核心工作流与公开发布版一致，并额外提供隐私检查和 token 估算工具。

> 重要提示：通用版已做基础版权声明和去隐私处理，发布前请阅读 `public/skill-architect-generic/NOTICE.md` 和 `PRIVACY.md`，并运行隐私检查。

## 省 Token 估算

脱敏案例：

- 第一轮：2034 → 836 行，约省 17,300-23,100 tokens。
- 第二轮：836 → 586 行，约省 8,400-11,200 tokens。
- 累计两轮：2034 → 586 行，约省 25,700-34,300 tokens。

实际节省因模型和加载方式而异，可按自己的文件运行：

```bash
python3 public/skill-architect-generic/scripts/estimate_tokens.py --original 原始SKILL.md --slimmed 瘦身后的SKILL.md
```

第二轮脱敏案例见 `public/skill-architect-generic/CASE_STUDIES.md`。

## 快速使用

安装或直接使用公开包中的脚本：

```bash
python3 public/skill-architect-public/scripts/audit.py --skill SKILL.md
python3 public/skill-architect-public/scripts/self_test.py
```

## 长对话续接

本段对话快照位于 `conversation-output/`。新对话应说：

```text
继续讨论 <问题>。先读取 conversation-output/conversation-snapshot.md 和 conversation-output/routing-index.md，按需加载对应技能包，不要复制旧对话全文。
```

长对话归纳：

```bash
python3 public/skill-architect-public/scripts/conversation_architect.py --transcript 对话文件.md --output-dir conversation-output --skill-name project-notes
```

新对话自动查找快照：

```bash
python3 public/skill-architect-public/scripts/find_conversation_handoff.py
```

当前已开对话导入：

```bash
python3 public/skill-architect-public/scripts/import_conversation_handoff.py --topic <问题>
```

跨用户导出与导入：

```bash
python3 public/skill-architect-public/scripts/export_conversation_handoff.py --snapshot-dir conversation-output --output skill-architect-handoff.zip
python3 public/skill-architect-public/scripts/import_conversation_handoff.py --source skill-architect-handoff.zip --topic <问题>
```

完整工作流和配置示例见 `docs/产品说明.md`、`docs/使用说明.md` 与 `public/skill-architect-public/SKILL.md`。
