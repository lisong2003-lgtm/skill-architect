#!/usr/bin/env python3
"""Audit a SKILL.md and report large sections that may be externalized."""


try:
    import os as _boot_os, sys as _boot_sys
    _boot_sys.path.insert(0, _boot_os.path.dirname(_boot_os.path.abspath(__file__)))
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass

import argparse
import math
import re
import sys
from pathlib import Path

import i18n
from estimate_tokens import stats as token_stats


def section_stats(text):
    lines = text.splitlines()
    headings = []
    for index, line in enumerate(lines):
        if re.match(r"^#{1,4} ", line):
            headings.append((index, line.strip()))
    sections = []
    for i, (start, heading) in enumerate(headings):
        end = headings[i + 1][0] if i + 1 < len(headings) else len(lines)
        body = "\n".join(lines[start:end])
        sections.append(
            {
                "heading": heading,
                "start": start + 1,
                "end": end,
                "lines": end - start,
                "chars": len(body),
                "cjk": len(re.findall(r"[\u4e00-\u9fff]", body)),
            }
        )
    return lines, sections


def main():
    raw = sys.argv[1:]
    lang = i18n.argv_lang(raw)
    desc = ("Audit a SKILL.md and report large sections that may be externalized."
            if lang == "en"
            else "审计 SKILL.md，列出可外移的大块章节建议。")
    parser = argparse.ArgumentParser(description=desc)
    i18n.add_lang_arg(parser, default=lang)
    parser.add_argument("--skill", required=True,
                        help="path to SKILL.md" if lang == "en" else "SKILL.md 路径")
    parser.add_argument("--threshold", type=int, default=50,
                        help="min section lines to report (default 50)" if lang == "en" else "回报阈值（行数），默认 50")
    parser.add_argument("--output", default="",
                        help="write the report to this file (optional)" if lang == "en" else "结果写入文件（可选）")
    parser.add_argument("--compare", default="",
                        help="slimmed SKILL.md to compare estimated tokens against (step 1 of the six-step flow)"
                        if lang == "en"
                        else "瘦身后的 SKILL.md 路径：在第 1 步审计时直接给出前后 token 估算对比")
    args = parser.parse_args(raw)

    path = Path(args.skill)
    if not path.is_file():
        print(f"SKILL_NOT_FOUND {path}")
        return 2
    compare_path = Path(args.compare) if args.compare else None
    if compare_path is not None and not compare_path.is_file():
        print(f"COMPARE_NOT_FOUND {compare_path}")
        return 2

    text = path.read_text(encoding="utf-8", errors="replace")
    lines, sections = section_stats(text)
    candidates = [s for s in sections if s["lines"] >= args.threshold]

    report = [
        f"# Skill Architect Audit",
        "",
        f"- SKILL: {path}",
        f"- Total lines: {len(lines)}",
        f"- Sections: {len(sections)}",
        f"- Candidate externalizable sections (>= {args.threshold} lines): {len(candidates)}",
        "",
        "## Candidates",
        "",
        "| Lines | Heading | Start | End | CJK |",
        "| ---: | --- | ---: | ---: | ---: |",
    ]
    for section in candidates:
        report.append(
            f"| {section['lines']} | {section['heading']} | {section['start']} | {section['end']} | {section['cjk']} |"
        )
    if compare_path is not None:
        # 与 estimate_tokens.py 同一套口径：字符数 × tokens_per_char（默认 0.6）。
        before = token_stats(path)
        after = token_stats(compare_path)
        before_tokens = math.ceil(before["chars"] * 0.6)
        after_tokens = math.ceil(after["chars"] * 0.6)
        saved = before_tokens - after_tokens
        percent = (saved / before_tokens * 100.0) if before_tokens else 0.0
        report += [
            "",
            "## Token 估算对比（第 1 步一并给出）",
            "",
            f"- 原文件：{path}（{before['lines']} 行 / {before['chars']} 字符）",
            f"- 瘦身后：{compare_path}（{after['lines']} 行 / {after['chars']} 字符）",
            f"- 常驻上下文估算：{before_tokens} → {after_tokens} tokens，省 {saved}（{percent:.1f}%）",
            "- 口径：字符数 × 0.6，粗估不是计费承诺；区间可用 estimate_tokens.py --tokens-per-char 0.8 复核。",
        ]
    report_text = "\n".join(report) + "\n"

    if args.output:
        Path(args.output).write_text(report_text, encoding="utf-8")
    print(report_text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
