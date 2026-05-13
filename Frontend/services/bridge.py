from __future__ import annotations

from datetime import datetime
from pathlib import Path


BRIDGE_FILE_NAME = "AlphaForgeV3_bridge_state.txt"


def get_bridge_file_path() -> Path:
    appdata = Path.home() / "AppData" / "Roaming"
    common_dir = appdata / "MetaQuotes" / "Terminal" / "Common" / "Files"
    common_dir.mkdir(parents=True, exist_ok=True)
    return common_dir / BRIDGE_FILE_NAME


def write_bridge_state(payload: dict[str, str]) -> Path:
    bridge_file = get_bridge_file_path()
    lines = [
        "bridge_status=ready",
        f"updated_at={datetime.now().isoformat(timespec='seconds')}",
    ]
    for key, value in payload.items():
        normalized = str(value).replace("\r", " ").replace("\n", " ").strip()
        lines.append(f"{key}={normalized}")

    bridge_file.write_text("\n".join(lines) + "\n", encoding="cp1252")
    return bridge_file
