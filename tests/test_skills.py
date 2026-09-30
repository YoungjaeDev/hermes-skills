"""Offline checks for the public Hermes skill collection. Run: python tests/test_skills.py"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {"orca-collab", "interview-methodology", "dev-flow", "session-handoff"}
REQUIRED_SECTIONS = ("when to use", "procedure", "pitfalls", "verification")


def check_skill(name: str) -> None:
    path = ROOT / name / "SKILL.md"
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"{name}: frontmatter must start at byte zero"
    marker = text.find("\n---\n", 4)
    assert marker > 0, f"{name}: closing frontmatter marker missing"
    frontmatter, body = text[4:marker], text[marker + len("\n---\n") :]
    for field in ("name", "description", "version", "license", "platforms", "metadata"):
        assert re.search(rf"^{field}:\s*.+", frontmatter, re.M), f"{name}: missing {field}"
    declared = re.search(r"^name:\s*['\"]?([\w-]+)", frontmatter, re.M)
    assert declared and declared.group(1) == name, f"{name}: name/dir mismatch"
    description = re.search(r"^description:\s*(.+)$", frontmatter, re.M)
    assert description and len(description.group(1)) <= 1024, f"{name}: description too long"
    assert all(platform in frontmatter for platform in ("windows", "linux", "macos")), f"{name}: incomplete platform support"
    for heading in REQUIRED_SECTIONS:
        assert re.search(rf"^##\s+{re.escape(heading)}\b", body, re.I | re.M), f"{name}: missing {heading}"
    assert len(body.strip()) >= 500, f"{name}: empty or stub skill"
    assert "C:/dev/" not in text and "C:\\dev\\" not in text, f"{name}: machine path leaked"
    assert "xion-zenith" not in text.lower(), f"{name}: private-project example leaked"
    # Only explicit relative links belong to THIS skill. A plain `references/...`
    # may intentionally name a reference in another Hermes skill.
    for rel in re.findall(r"`\./((?:references|scripts)/[^`\s]+)`", body):
        rel = rel.rstrip(".,;:)")
        assert (path.parent / rel).is_file(), f"{name}: missing support file {rel}"
    print(f"PASS {name} ({len(text)} chars)")


def main() -> None:
    actual = {p.name for p in ROOT.iterdir() if p.is_dir() and (p / "SKILL.md").exists()}
    assert actual == EXPECTED, f"skill inventory mismatch: expected {EXPECTED}, found {actual}"
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for name in sorted(EXPECTED):
        check_skill(name)
        assert f"YoungjaeDev/hermes-skills/{name}" in readme, f"README: install command for {name} missing"
    assert (ROOT / "LICENSE").read_text(encoding="utf-8").startswith("MIT License")
    print(f"PASS collection ({len(actual)} skills, README, license)")


if __name__ == "__main__":
    main()
