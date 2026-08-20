# Skill Architect（通用版）

把过大的 `SKILL.md` 从“整本常驻”改成“目录 + 路由索引 + 按需读取技能包”的结构化瘦身技能。本版本不绑定特定 Agent，只要能读取 Markdown 并运行 Python 3.9+ 脚本即可使用。

> 重要提示：对外发布前，请先阅读 `NOTICE.md`、`PRIVACY.md` 和 `LICENSE`。本包已做基础版权声明和去隐私处理，但使用者后续加入的内容需要自行检查。

面向平台发布用的完整产品说明见 `PRODUCT.md`，使用说明见 `USAGE.md`。

## 特点

- 架构级外移，不只是压缩文字
- 审计大块章节，给出可外移建议
- 修改前完整备份，支持校验值恢复
- 自动抽取章节并替换为短说明
- 自动生成技能包路由索引
- 路径、结构、测试集验证
- 长对话归纳为快照和可复用技能包
- 无第三方依赖，Python 3.9+ 即可运行
- 内置隐私检查与 token 节省估算脚本

## 省多少 Token

脱敏案例：

- 案例一（第一轮）：2034 → 836 行，约省 17,300-23,100 tokens。
- 案例二（第二轮）：836 → 586 行，约省 8,400-11,200 tokens。
- 累计两轮：2034 → 586 行，约省 25,700-34,300 tokens。

实际节省取决于模型 tokenizer、内容长度和技能包加载频率。要按自己的文件精确估算：

```bash
python3 scripts/estimate_tokens.py --original 原始SKILL.md --slimmed 瘦身后的SKILL.md
```

详细假设和路由测试见 `TOKEN_SAVINGS.md` 与 `CASE_STUDIES.md`。

## 与 Codex 版的关系

- `skill-architect-public`：面向 Codex/OpenAI 兼容平台的发布版，包含 `agents/openai.yaml` 元信息。
- `skill-architect-generic`：本目录，面向其他 Agent 的通用版，核心工作流相同，并额外提供版权、隐私和 token 估算工具。

## 工作流

1. 审计：`scripts/audit.py --skill SKILL.md`
2. 用户确认要外移的章节
3. 备份：`scripts/backup.py --skill SKILL.md --backup backup/`
4. 抽取：`scripts/extract.py --skill SKILL.md --markers "start|end" --output extracted.md`
5. 路由：`scripts/build_index.py --pack-dir packs/ --index index.md --root .`
6. 验证：`scripts/validate.py --skill SKILL.md --index index.md --root .`
7. 回滚：`scripts/rollback.py --skill SKILL.md --backup backup/SKILL.md`

## 长对话归纳

把长对话导出为 Markdown 或文本后，运行：

```bash
python3 scripts/conversation_architect.py --transcript 对话文件.md --output-dir conversation-output --skill-name project-notes
```

生成内容：

- `conversation-snapshot.md`：核心结论、决策、待办和边界待 Agent 补充
- `skills/*/SKILL.md`：按话题生成的技能包骨架
- `routing-index.md`：后续按需读取的索引

简化触发：

- 老对话：`帮我总结这个长对话`
- 新对话：`继续讨论 <问题>`

默认输出目录为 `conversation-output/`。新对话中说“继续讨论 <问题>”时，Skill Architect 会先运行 `scripts/find_conversation_handoff.py` 自动查找最新快照和路由索引；找不到时再查找当前目录的 `conversation-output/`。

完整对话 transcript 顶部必须声明 `conversation_scope: whole-dialog`；只总结某个主题时，才使用 `--scope topic`。脚本默认拒绝用主题片段冒充完整对话。

该能力不删除或压缩当前对话框上下文，主要让新对话只引用快照和技能包。详细方法见 `references/长对话归纳最佳实践.md`。

## 当前已开对话导入

如果不想新开对话，而是在当前已开的对话框里迁移已总结的长对话：

```text
把总结过的长对话导入当前对话，继续讨论 <问题>
```

Skill Architect 会运行 `scripts/import_conversation_handoff.py --topic <问题>`，读取最新快照、路由索引和匹配技能包，不复制旧对话完整历史。

低消耗快速导入：直接说“快速导入已总结长对话”，Skill Architect 只运行导入脚本、展示最后一段回答并停止，不执行项目分析、路由优化或蒸馏。

继续规则：先展示快照中的“老对话最后一段回答”，然后停止，由用户决定下一步；不自动执行老对话中的瘦身、修改、蒸馏等任务。

触发优先级：本机某个高优先级 Skill 项目可能接管“继续老版综合思维讨论”；此时提醒用户显式说“用 skill-architect 导入已总结长对话”。其他项目或新对话中优先运行 `find_conversation_handoff.py`。

## 跨用户传输

发送方：

```bash
python3 scripts/export_conversation_handoff.py --snapshot-dir conversation-output --output skill-architect-handoff.zip
```

接收方：

```bash
python3 scripts/import_conversation_handoff.py --source skill-architect-handoff.zip --dest imported-conversation-output --topic <问题>
```

只传快照和技能包，不传完整对话。详细方法见 `references/跨用户传输最佳实践.md`。

## 接入其他 Agent

- Codex/OpenAI 兼容平台：将本目录作为 Skill 安装，或读取 `SKILL.md`。
- Claude 等支持 Skill 目录的平台：按目标平台规则放置本目录。
- DeepSeek、Gemini、OpenClaw 等通用 Agent：在项目 `AGENTS.md` 或对话上下文中引用 `SKILL.md` 与本目录路径。
- 纯命令行：直接运行 `scripts/` 下的 Python 脚本，不依赖任何 Agent 能力。

## 快速开始

```text
用 skill-architect 审计我的 SKILL.md，找出哪些大块内容适合外移。
或：把当前长对话归纳成快照和技能包。
```

## 目录

- `SKILL.md`：技能入口
- `AGENTS.md`：任意 Agent 可读取的通用接入说明
- `NOTICE.md`：版权与发布须知
- `PRIVACY.md`：隐私与去隐私检查说明
- `TOKEN_SAVINGS.md`：省 token 估算假设
- `CASE_STUDIES.md`：脱敏应用案例
- `PRODUCT.md`：面向 SkillHub、GitHub 等平台的产品说明
- `USAGE.md`：面向用户的操作说明
- `agents/openai.yaml`：可选，供 OpenAI/Codex 兼容平台读取
- `scripts/`：审计、备份、抽取、路由、验证、回滚、自测、隐私检查、token 估算、长对话归纳
- `references/`：瘦身最佳实践、长对话归纳最佳实践
- `templates/`：路由索引、技能包和对话归纳模板
- `examples/`：示例输出

## 自测

```bash
python3 scripts/self_test.py
python3 scripts/check_privacy.py --root .
```

## 版本信息

- 版本：0.2.0
- 许可证：CC BY-NC-SA 4.0
- 版权与隐私：见 `NOTICE.md` 和 `PRIVACY.md`
- 变更记录：见 `CHANGELOG.md`

## 授权

CC BY-NC-SA 4.0。
