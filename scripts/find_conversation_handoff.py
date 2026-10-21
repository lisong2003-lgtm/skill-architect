#!/usr/bin/env python3
"""Find the most recent conversation snapshot for a new chat."""


try:
    import os as _boot_os, sys as _boot_sys
    _boot_sys.path.insert(0, _boot_os.path.dirname(_boot_os.path.abspath(__file__)))
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass



import argparse
from pathlib import Path


def last_answer_text(snapshot):
    text = snapshot.read_text(encoding="utf-8", errors="ignore")
    marker = "## 老对话最后一段回答"
    if marker not in text:
        return "NOT_FOUND"
    section = text.split(marker, 1)[1].split("##", 1)[0].strip()
    return section or "NOT_FOUND"


def candidates(search_base):
    roots = [Path.cwd()]
    if search_base:
        roots.append(Path(search_base).resolve())

    found = []
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("conversation-snapshot.md"):
            if "conversation-output" in path.parts:
                found.append(path)
    return sorted(found, key=lambda p: p.stat().st_mtime, reverse=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--search-base", default="")
    args = parser.parse_args()

    latest = candidates(args.search_base)
    if not latest:
        print("CONVERSATION_HANDOFF_NOT_FOUND")
        raise SystemExit(1)

    snapshot = latest[0]
    index = snapshot.parent / "routing-index.md"
    print(f"snapshot={snapshot}")
    print(f"index={index}")
    print(f"last_answer={last_answer_text(snapshot)}")
    print(f"found={len(latest)}")
    print("CONVERSATION_HANDOFF_OK")


if __name__ == "__main__":
    main()
