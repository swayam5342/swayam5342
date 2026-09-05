from pathlib import Path
from github_api import get_github_stats
from xml.sax.saxutils import escape
import json


ROOT = Path(__file__).resolve().parent.parent


def format_number(number):
    return f"{number:,}"


def main():
    with open(ROOT / "data" / "profile.json", "r", encoding="utf-8") as f:
        profile = json.load(f)

    print("Fetching GitHub statistics...")

    stats = get_github_stats(profile["username"])

    currently = profile.get("currently", [])

    while len(currently) < 3:
        currently.append("")

    replacements = {
        "{{NAME}}": profile["name"],
        "{{USERNAME}}": profile["username"],
        "{{ROLE}}": profile["role"],
        "{{LOCATION}}": profile["location"],
        "{{UNIVERSITY}}": profile["university"],
        "{{REPOSITORIES}}": format_number(stats["repositories"]),
        "{{STARS}}": format_number(stats["stars"]),
        "{{FOLLOWERS}}": format_number(stats["followers"]),
        "{{FOLLOWING}}": format_number(stats["following"]),
        "{{CONTRIBUTIONS}}": format_number(stats["contributions"]),
        "{{CURRENT_1}}": currently[0],
        "{{CURRENT_2}}": currently[1],
        "{{CURRENT_3}}": currently[2],
    }

    replacements = {key: escape(str(value)) for key, value in replacements.items()}

    for theme in ["dark", "light"]:
        template_path = ROOT / "templates" / f"{theme}.svg"
        output_path = ROOT / "assets" / f"{theme}_mode.svg"

        template = template_path.read_text(encoding="utf-8")

        for key, value in replacements.items():
            template = template.replace(key, value)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(template, encoding="utf-8")

        print(f"Generated {output_path}")
        print(f"Size: {output_path.stat().st_size} bytes")


if __name__ == "__main__":
    main()
