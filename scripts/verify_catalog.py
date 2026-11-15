# SPDX-FileCopyrightText: 2026 Tip of the Aero contributors
# SPDX-License-Identifier: Apache-2.0
from catalog import discover

if __name__ == "__main__":
    tools = discover()
    assert tools, "No tools registered"

    for folder, data in tools:
        print(f"OK: {data['id']} ({data['version']})")
