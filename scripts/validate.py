#!/usr/bin/env python3
"""Validate externalized SKILL structure, routing paths, and optional test prompts."""


try:
    import os as _boot_os, sys as _boot_sys
    _boot_sys.path.insert(0, _boot_os.path.dirname(_boot_os.path.abspath(__file__)))
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

# --test-command 里的这些可执行名统一换成当前解释器：
# Windows 上常常没有 python3 命令（只有 py / python），CI 里也不保证 PATH 一致。
_PY_ALIASES = {"python", "python3", "py"}


def build_argv(command: str) -> list[str]:
    """把 --test-command 解析成 argv 列表，交给 subprocess 直接 exec（不经 shell）。

    用列表执行意味着 `;`、`&&`、`|`、`$(...)` 都不会被解释成命令拼接，
    所以“用户传进来的测试命令”最多只能跑一条程序，不能被拼上第二条。
    """
    argv = shlex.split(command, posix=(os.name != "nt"))
    if not argv:
        raise ValueError("empty test command")
    exe_head = argv[0].replace("\\", "/").rsplit("/", 1)[-1].lower()
    if exe_head in _PY_ALIASES:
        argv = [sys.executable] + argv[1:]
    return argv


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill", required=True)
    parser.add_argument("--index", required=True)
    parser.add_argument("--test-prompts", default="")
    parser.add_argument("--root", default=str(Path.cwd()))
    parser.add_argument("--test-command", default="")
    args = parser.parse_args()

    ok = True
    skill = Path(args.skill)
    index = Path(args.index)
    root = Path(args.root)
    if not skill.exists():
        print(f"MISSING skill {skill}")
        ok = False
    if not index.exists():
        print(f"MISSING index {index}")
        ok = False

    if index.exists():
        text = index.read_text(encoding="utf-8", errors="ignore")
        paths = re.findall(r"`([^`]+)`", text)
        missing = [p for p in paths if not (root / p).exists()]
        for path in missing:
            print(f"MISSING indexed path {path}")
        if missing:
            ok = False
        else:
            print(f"indexed_paths={len(paths)}")

    if args.test_prompts:
        prompts_path = Path(args.test_prompts)
        if prompts_path.exists():
            data = json.loads(prompts_path.read_text(encoding="utf-8"))
            cases = data.get("test_cases", data if isinstance(data, list) else [])
            print(f"test_cases={len(cases)}")
        else:
            print(f"MISSING test-prompts {prompts_path}")
            ok = False

    if args.test_command:
        try:
            argv = build_argv(args.test_command)
        except ValueError as exc:
            print(f"test_command=INVALID ({exc})")
            print("VALIDATE_FAILED")
            sys.exit(1)
        # shell=False：只 exec 解析出的第一条程序，不解释管道/分号/重定向。
        result = subprocess.run(argv, shell=False, capture_output=True, text=True)
        if result.returncode == 0:
            print("test_command=OK")
        else:
            print(f"test_command=FAILED\n{result.stdout}\n{result.stderr}")
            ok = False

    print("VALIDATE_OK" if ok else "VALIDATE_FAILED")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
