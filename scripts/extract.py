#!/usr/bin/env python3
"""Extract marked sections from SKILL.md and replace them with a short marker."""


try:
    import os as _boot_os, sys as _boot_sys
    _boot_sys.path.insert(0, _boot_os.path.dirname(_boot_os.path.abspath(__file__)))
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass

import argparse
import json
import sys
from pathlib import Path


def find_block(lines, start_marker, end_marker):
    start = None
    end = None
    for index, line in enumerate(lines):
        if start is None and line.startswith(start_marker):
            start = index
        elif start is not None and line.startswith(end_marker):
            end = index
            break
    if start is None or end is None:
        raise ValueError(f"block not found: {start_marker} -> {end_marker} (start={start} end={end})")
    return start, end


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill", required=True)
    parser.add_argument("--markers", action="append", help="start_marker|end_marker")
    parser.add_argument("--output", default="")
    parser.add_argument("--replace-marker", default="## 已外移说明\n\n内容已外移到独立文件。")
    parser.add_argument("--config", default="")
    args = parser.parse_args()

    skill = Path(args.skill)
    if not skill.is_file():
        print(f"SKILL_NOT_FOUND {skill}")
        return 2
    # errors="replace"：SKILL.md 被别的编辑器存成 GBK/混合编码时也不崩，
    # 只把非法字节换成 U+FFFD，其余内容照常外移。
    lines = skill.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)
    extracted_lines = 0
    outputs = 0

    if args.config:
        config_path = Path(args.config)
        if not config_path.is_file():
            print(f"CONFIG_NOT_FOUND {config_path}")
            return 2
        config = json.loads(config_path.read_text(encoding="utf-8", errors="replace"))
        for item in config.get("sections", []):
            start, end = find_block(lines, item["start"], item["end"])
            extracted_lines += end - start
            extracted_text = "".join(lines[start:end])
            replace_marker = item.get("replace_marker", args.replace_marker).replace("\\n", "\n")
            marker = replace_marker + "\n" if not replace_marker.endswith("\n") else replace_marker
            lines[start:end] = [marker]
            output = Path(item["output"])
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(extracted_text, encoding="utf-8")
            outputs += 1
    else:
        if not args.markers or not args.output:
            print("MISSING_ARGS use --markers/--output or --config")
            return 2
        replace_marker = args.replace_marker.replace("\\n", "\n")
        for spec in args.markers:
            start_marker, end_marker = spec.split("|", 1)
            start, end = find_block(lines, start_marker, end_marker)
            extracted_lines += end - start
            extracted_text = "".join(lines[start:end])
            marker = replace_marker + "\n" if not replace_marker.endswith("\n") else replace_marker
            lines[start:end] = [marker]
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(extracted_text, encoding="utf-8")
        outputs = 1

    skill.write_text("".join(lines), encoding="utf-8")
    print(f"extracted_lines={extracted_lines}")
    print(f"outputs={outputs}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except ValueError as exc:
        # 标记没找到：给错误码 3，调用方（self_test / 六步流程）能区分“参数错”和“标记错”。
        print(f"EXTRACT_FAILED {exc}")
        sys.exit(3)
