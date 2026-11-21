import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent / "src")
)

from validation_agent.helpers.requirements_parser import parse_requirements

# Purpose: test parse_requirements() in
# src/validation_agent/requirements_parser.py — the requirement
# bullet extraction from a markdown file. Fake files only, via
# tmp_path, no real requirements file.
#
# Scenarios:
#   1. test_parse_requirements_with_bullet — a file with a requirement
#      bullet returns it with the right ID; headers, plain text, and
#      bullets without a bold requirement ID are ignored.
#   2. test_parse_requirements_empty_bullet — a file with no matching
#      lines returns [].
#   3. test_parse_requirements_empty_file — an empty file returns [].



def test_parse_requirements_with_bullet(tmp_path):
    req_file = tmp_path / "requirements.md"
    req_file.write_text(
        "#Heading\n"
        "\n"
        "Some plain text.\n"
        "- A bullet without a bold ID.\n"
        "- **REQ-001**: this is the right requirement format.\n"
        "- **REQ-002**: this is the secound requirement.\n"
        "- **not-an-id**: similar to id format but not.\n",
        encoding="utf-8",
    )
    reqs = parse_requirements(str(req_file))
    assert len(reqs) == 2
    assert reqs[0].req_id == "REQ-001"
    assert reqs[1].description == "this is the secound requirement."
    assert reqs[0].path == str(req_file)


def test_parse_requirements_empty_bullet(tmp_path):
    req_file = tmp_path / "requirements.md"
    req_file.write_text(
        "#Heading\n"
        "\n"
        "No requirement bullets here.\n",
        encoding="utf-8"
    )
    reqs = parse_requirements(str(req_file))
    assert reqs == []

def test_parse_requirements_empty_file(tmp_path):
    req_file = tmp_path / "requirements.md"
    req_file.write_text(
        "",
        encoding="utf-8"
    )
    reqs = parse_requirements(str(req_file))
    assert reqs == []
