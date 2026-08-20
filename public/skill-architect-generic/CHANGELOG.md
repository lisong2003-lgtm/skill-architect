# 变更记录

## 0.2.0 - 2026-08-20

- 重写产品说明和使用说明，突出“Skill 架构重构、长对话快照迁移、跨 Agent 传输”三大能力。
- 产品说明加入本机实际验证案例：架构重构、长对话快照、Skill 包导出导入、触发优先级。
- 新增 `PRODUCT.md` 和 `USAGE.md`，便于 SkillHub、GitHub 等平台直接发布。
- 发布包升级为 `skill-architect-generic-0.2.0.zip`。

## 0.1.0 - 2026-08-20

- 首个公开发布版。
- 提供审计、备份、抽取、路由、验证、回滚和自测脚本。
- 提供通用 JSON 配置模式，可对任意 `SKILL.md` 执行章节外移。
- 无第三方依赖，Python 3.9+ 可运行。

## 0.1.0-generic - 2026-08-20

- 从 Codex 发布版拆出的跨 Agent 通用版。
- 新增 `AGENTS.md`，供任意 Agent 读取接入流程。
- 新增 `NOTICE.md` 和 `PRIVACY.md`，补齐版权与去隐私说明。
- 示例审计数据改为虚构占位，移除原项目统计痕迹。
- 新增 `scripts/check_privacy.py` 和 `scripts/estimate_tokens.py`。
- README 增加发布提醒和省 token 估算说明。
- 新增 `CASE_STUDIES.md`，写入第二轮瘦身的脱敏量化案例。
- 新增 `PRODUCT.md`，按“Token 节省 + 架构重构好处”结构输出平台产品说明。
- `PRODUCT.md` 增加长对话归纳场景：把长对话沉淀为可检索技能库。
- 新增 `scripts/conversation_architect.py`、对话快照模板、技能包模板和最佳实践。
- 增加简化续接模板：老对话“帮我总结这个长对话”，新对话“继续讨论 <问题>”。
- 增加总结范围强制规则：收到总结请求后先停止当前 SKILL 修改，且默认覆盖整个对话框。
- `conversation_architect.py` 增加 transcript scope 校验，默认拒绝主题片段冒充完整对话。
- 新增 `scripts/find_conversation_handoff.py`，新对话可自动查找最新快照，不再依赖用户手动给路径。
- 新增 `scripts/import_conversation_handoff.py`，当前已开对话可只导入快照和匹配技能包。
- 新增 `scripts/export_conversation_handoff.py` 和跨用户传输最佳实践。
- 快照保留“老对话最后一段回答”；继续时先展示并停止，由用户决定下一步。
- 快照查找和导入脚本直接输出 `last_answer=...`，强化停止规则。
- 修复 `rollback.py` 对备份目录回滚时报 `BACKUP_NOT_FOUND` 的问题。
- 新增触发优先级与故障排查说明，防止被其他高优先级 Skill 接管后长时间分析。
- 新增低消耗快速导入模式，避免长时间思考造成 Token 浪费。
- 保留全部脚本、模板、示例和自测能力。
