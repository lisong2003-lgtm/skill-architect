#!/usr/bin/env bash
# extract 跨平台 CLI 入口（macOS / Linux；Windows 用 scripts/extract.cmd 或 python scripts/extract.py）。
exec python3 "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/extract.py" "$@"
