# Skill Architect Generic Agent Guide

This skill works with any AI agent that can read Markdown and run Python 3.9+ scripts.

## When to use

Use when the user asks to slim, externalize, token-optimize, or restructure a large `SKILL.md`.

## Required workflow

1. Audit: run `scripts/audit.py --skill SKILL.md` and present externalizable sections.
2. Confirm: list exactly which sections will move and which will stay. Wait for user approval.
3. Backup: run `scripts/backup.py --skill SKILL.md --backup backup/`.
4. Extract: run `scripts/extract.py --skill SKILL.md --config slim-config.json`.
5. Route: run `scripts/build_index.py --pack-dir packs --index index.md --root .`.
6. Validate: run `scripts/validate.py --skill SKILL.md --index index.md --root . --test-command "python3 scripts/self_test.py"`.
7. Rollback if needed: run `scripts/rollback.py --skill SKILL.md --backup backup/SKILL.md`.
8. Release check: before distributing, run `scripts/check_privacy.py --root .` and report token savings with `scripts/estimate_tokens.py --original 原始SKILL.md --slimmed 瘦身后的SKILL.md`.

## Long-conversation mode

Use when the user wants to summarize a long conversation into reusable skill packs for a new chat.

1. Save the conversation as Markdown or text.
2. Run `scripts/conversation_architect.py --transcript <conversation.md> --output-dir conversation-output --skill-name <skill-name>`.
3. Fill the snapshot fields: core conclusions, decisions, todos, boundaries, and risks.
4. Use `scripts/build_index.py` and `scripts/validate.py` to route and validate the generated packs.

This mode does not delete or compress the current conversation context. Its token benefit applies when a new chat loads the snapshot and selected packs instead of the full history.

Continuation trigger:

- Old chat: when the user says “帮我总结这个长对话”, generate `conversation-snapshot.md`, skill packs, and `routing-index.md`.
- New chat: when the user says “继续讨论 <topic>”, run `scripts/find_conversation_handoff.py` first, read the latest snapshot and routing index, then load only the matching pack.
- If the handoff script cannot find a snapshot, look in the current cwd `conversation-output/`, then ask the user for the snapshot path.
- Current dialog: when the user says “把总结过的长对话导入当前对话，继续讨论 <topic>”, run `scripts/import_conversation_handoff.py --topic <topic>`, read the latest snapshot, routing index, and matching pack. Do not copy the full old conversation.
- Cross-user transfer: sender runs `scripts/export_conversation_handoff.py`; receiver runs `scripts/import_conversation_handoff.py --source <zip> --topic <topic>`. Transfer only the compact handoff zip, never the full conversation.

Summary scope rule:

- When the user asks to summarize the long conversation, stop the current SKILL editing task first.
- Cover the whole current conversation unless the user explicitly asks for one topic only.
- If the full transcript is not available, ask the user to export it. Do not fabricate a transcript that only contains the current SKILL task.
- Enforce transcript scope: default command requires `conversation_scope: whole-dialog` in the transcript header. Use `--scope topic` only when the user explicitly asks for one topic, and require `conversation_scope: topic`.
- When continuing a migrated conversation, show the snapshot’s last assistant answer first, then stop and let the user decide the next step. Do not automatically rerun old skill-editing or distillation tasks.
- The handoff scripts print `last_answer=...`; display that content and stop. Do not continue old tasks after printing it.
- Priority note: in a local high-priority Skill project, another Skill may intercept “继续老版综合思维讨论”. Remind the user to call Skill Architect explicitly. In other dialogs, run the handoff finder first and stop after showing `last_answer`.
- If trigger or priority is uncertain, do not run long project analysis. Ask the user or remind them to use the explicit Skill Architect command.
- Fast import mode: when the user says “快速导入已总结长对话”, run `import_conversation_handoff.py`, show `last_answer`, and stop. Do not perform project analysis, routing calibration, distillation, or validation.

## Constraints

- Always back up before modifying.
- Externalize content; do not silently delete it.
- Do not report success when validation fails. Fix or roll back first.
- Keep identity, core judgment rules, protocols, and routing entry in the main `SKILL.md`.
- Python 3.9+ is required. There are no third-party dependencies.
- Never add original books, private logs, personal data, private paths, emails, phone numbers, or ID numbers to the distributed package.
- Report token savings as an estimate, not a billing promise.
