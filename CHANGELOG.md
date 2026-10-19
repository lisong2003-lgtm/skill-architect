# 变更记录

## 0.3.3 - 2026-10-19

- 三平台版本对齐到 0.3.3（GitHub / SkillHub / ClawHub）。
- 新增自检断言「拆包→回滚→再发布」行为不变：回滚后 SHA-256 必须与原文一致，再发布抽取结果必须与首轮完全一致。
- 真实大 SKILL 多重回归：从本地现成技能/某项目快照选 3 个真实大 SKILL（均不含发布包内容），每样本 3 轮 audit→extract→build_index→validate→回滚→再发布，共 9 轮，全部 PASS。

| 样本（脱敏） | SKILL 大小（字节/行） | 轮数 | 抽取块 | audit | extract | build_index | validate | 回滚（SHA-256 与原文一致） | 再发布抽取一致 |
| --- | ---: | ---: | --- | --- | --- | --- | --- | --- | --- |
| 本地项目快照A | 182,325 / 2,034 | 3 | 块A1–A3 | PASS ×3 | PASS ×3 | PASS ×3 | PASS ×3 | PASS ×3 | PASS ×3 |
| 本地现成技能B | 106,432 / 1,466 | 3 | 块B1–B3 | PASS ×3 | PASS ×3 | PASS ×3 | PASS ×3 | PASS ×3 | PASS ×3 |
| 本地现成技能C | 142,557 / 3,457 | 3 | 块C1–C3 | PASS ×3 | PASS ×3 | PASS ×3 | PASS ×3 | PASS ×3 | PASS ×3 |

- 回滚后 SHA-256 前 16 位与原文一致：A=`9b7884f855761e55`，B=`9c7f6d5ba3856803`，C=`0d7f8b77d5ab9f60`。
- `scripts/self_test.py` 冒烟测试 SELF_TEST_OK。

## 0.3.2 - 2026-10-18

- 与 SkillHub 平台版本统一到 0.3.2；GitHub Release 与 SkillHub 双端版本一致。
- 真实大 SKILL 回归：使用一个 104,744 字节（836 行）真实大 SKILL 快照（本地回归，具体路径不出包），完成 3 轮 拆包→回滚→再发布：
  - 第 1 轮：抽取「六类能力增强协议→七项能力增强执行方案」；audit+extract+build_index+validate OK；回滚后 SHA-256 与原文一致；再发布抽取结果与首轮完全一致。
  - 第 2 轮：抽取「高生产力服务协议→我的判断尺」；同上全部 PASS。
  - 第 3 轮：抽取「方法神经网络→我说话的方式」（198 行）；同上全部 PASS，行为保持不变。
- `scripts/self_test.py` 冒烟测试 SELF_TEST_OK。


## 0.2.1 - 2026-08-27

- 修复导入 zip 时路径穿越风险，逐个成员校验解压路径必须位于目标目录内。
- 导出改为白名单：只打包快照、路由索引和 `skills/` 下的 SKILL.md，不再打包目录内任意文件。
- 自动查找快照不再默认全盘扫描 `~/Documents/Codex`，只扫当前项目；跨项目使用 `--search-base`。
- 对话归纳候选行标注“自动候选，需复核”，避免被当成最终结论。
- 自测新增恶意 zip 拒绝和导出隐私测试。
- 新增 Ponytail 前置审查说明：Ponytail 决定“要不要”，skill-architect 决定“放哪里”。

## 0.2.0 - 2026-08-20

- 重写产品说明和使用说明，突出“Skill 架构重构、长对话快照迁移、跨 Agent 传输”三大能力。
- 产品说明加入本机实际验证案例：架构重构、长对话快照、Skill 包导出导入、触发优先级。
- 新增 `PRODUCT.md` 和 `USAGE.md`，便于 SkillHub、GitHub 等平台直接发布。
- 发布包升级为 `skill-architect-public-0.2.0.zip`。

## 0.1.0 - 2026-08-20

- 首个公开发布版。
- 提供审计、备份、抽取、路由、验证、回滚和自测脚本。
- 提供通用 JSON 配置模式，可对任意 `SKILL.md` 执行章节外移。
- 新增长对话归纳：`scripts/conversation_architect.py`、对话模板和最佳实践。
- 增加简化续接：老对话“帮我总结这个长对话”，新对话“继续讨论 <问题>”。
- 增加总结范围强制规则：必须总结整个当前对话框，不能只总结当前 SKILL 任务。
- `conversation_architect.py` 默认强制 `conversation_scope: whole-dialog`，主题片段必须显式 `--scope topic`。
- 新增 `scripts/find_conversation_handoff.py`，新对话可自动查找最新快照和路由索引。
- 新增 `scripts/import_conversation_handoff.py`，当前已开对话可导入已总结长对话。
- 新增 `scripts/export_conversation_handoff.py`，支持跨用户只传快照 zip。
- 快照新增“老对话最后一段回答”，继续迁移问题时不自动执行旧任务。
- 快照查找和导入脚本直接输出 `last_answer=...`，Agent 必须展示后停止。
- 修复 `rollback.py` 对备份目录回滚时报 `BACKUP_NOT_FOUND` 的问题。
- 新增触发优先级与故障排查说明，提醒用户存在高优先级 Skill 时显式调用。
- 新增低消耗快速导入模式：只导入快照并展示最后一段回答，不执行项目分析。
- 新增隐私检查和 token 估算脚本。
- 无第三方依赖，Python 3.9+ 可运行。
