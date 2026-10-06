"""Create ignored local-only Compose configuration without overwriting user settings."""

import secrets
from pathlib import Path

root = Path(__file__).resolve().parents[1]
target = root / ".env"
if target.exists():
    content = target.read_text(encoding="utf-8")
    if not any(line.startswith("PPM_JWT_SECRET=") for line in content.splitlines()):
        with target.open("a", encoding="utf-8", newline="\n") as output:
            output.write("\nPPM_JWT_SECRET=" + secrets.token_hex(48) + "\n")
        print("Added missing local JWT key; existing settings preserved.")
    else:
        print(".env already exists; preserved.")
else:
    content = "# Generated local development credentials. Do not commit.\n"
    for name in ("POSTGRES", "OWNER", "APP"):
        content += f"PPM_{name}_PASSWORD={secrets.token_hex(24)}\n"
    content += (
        "PPM_WEB_PORT=3000\nPPM_API_PORT=8000\nPPM_POSTGRES_PORT=15432\nPPM_REDIS_PORT=16379\n"
    )
    content += "PPM_JWT_SECRET=" + secrets.token_hex(48) + "\n"
    with target.open("x", encoding="utf-8", newline="\n") as output:
        output.write(content)
    print("Created .env with random local credentials; values not displayed.")
