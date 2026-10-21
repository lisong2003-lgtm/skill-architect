# SKILL.md Architect & Maintenance

> skill-architect (skill-architect) v0.3.3 · overseas-friendly lightweight layer. 中文版见 [README.md](README.md).

## What it is
Audits and refactors large SKILL.md files by extracting bulky sections into skill packs, generating a routing index, validating tests, and enabling rollback. It also turns long conversations into snapshots and reusable skill packs, and continues a new chat from the latest snapshot.

## When to use it
Use to slim, externalize, token-optimize or restructure a SKILL.md, summarize a long conversation, or continue from a saved conversation snapshot; do not use for simple wording compression.

## Quick start
```bash
python3 scripts/audit.py --skill /path/SKILL.md
python3 scripts/extract.py --skill /path/SKILL.md --config slim-config.json
python3 scripts/build_index.py --pack-dir packs --index index.md --root .
python3 scripts/validate.py --skill /path/SKILL.md --index index.md --root .
```

## Install across the three platforms
- **GitHub**: clone or download the repo, copy the skill folder into `$CODEX_HOME/skills/` (or `~/.claude/skills/` / your agent's skill directory).
- **SkillHub**: install the SkillHub lightweight package (text-only). The lightweight package removes platform-only launcher files (`.cmd`/`.ps1`, extensionless scripts and binary language models) and documents the Windows usage inside its own README; the GitHub full package keeps all platform launchers and assets.
- **ClawHub**: install the ClawHub full package, which keeps cross-platform launchers and assets.
- All platform packages serve the same canonical logic; platform copies never change the canonical code.

## Dependencies
Python 3.8+ standard library; no third-party runtime.

## Privacy
Run locally; files are read and written on your machine only.

## Boundaries / limitations
Refactors text structure; it cannot judge the semantic correctness of the skill content you move.

## License
CC-BY-NC-SA-4.0

---

## Culture note
- `--lang en|zh` controls UI/help/JSON message language (default `zh`); business algorithms are identical in both languages.
- For image-ocr, `--lang` remains the OCR language; UI language is `--ui-lang en|zh`.
- Local Chinese templates and plant/concept dictionaries are NOT replaced; overseas inputs can select alternatives via parameters (e.g. `--plant-library`, `--project-rules`) so existing Chinese users are unaffected.
- Review flags, confidence tiers and evidence coordinates are language-independent fields.
