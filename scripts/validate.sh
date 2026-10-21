#!/usr/bin/env bash
# validate 跨平台 CLI 入口（macOS / Linux；Windows 用 scripts/validate.cmd 或 python scripts/validate.py）。
exec python3 "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/validate.py" "$@"
