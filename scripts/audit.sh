#!/usr/bin/env bash
# audit 跨平台 CLI 入口（macOS / Linux；Windows 用 scripts/audit.cmd 或 python scripts/audit.py）。
exec python3 "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/audit.py" "$@"
