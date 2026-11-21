import re
from dataclasses import dataclass


@dataclass
class Requirement:
    req_id: str
    description: str
    path: str = ""

_REQ_RE = re.compile(r"^\s*-\s*\*\*([A-Z]+-\d+)\*\*:\s*(.+?)\s*$")


def parse_requirements(path: str) -> list[Requirement]:
    """Parse requirement bullets from *path* in document order."""
    with open(path, encoding="utf-8") as requirements_file:
        return [
            Requirement(req_id=match.group(1), description=match.group(2), path=path)
            for line in requirements_file
            if (match := _REQ_RE.match(line))
        ]



if __name__ == "__main__":

    path = "input/requirements/requirements_power_window.md"

    requirements = parse_requirements(path)

    for req in requirements:
        print(f"{req.req_id}: {req.description} (from {req.path})")