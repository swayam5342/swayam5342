import json
from pathlib import Path

from github_api import get_github_stats


ROOT = Path(__file__).parent.parent

DATA_FILE = ROOT / "data" / "profile.json"

DARK_TEMPLATE = ROOT / "templates" / "dark.svg"
LIGHT_TEMPLATE = ROOT / "templates" / "light.svg"

DARK_OUTPUT = ROOT / "assets" / "dark_mode.svg"
LIGHT_OUTPUT = ROOT / "assets" / "light_mode.svg"


def load_profile():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def format_number(number):
    return f"{number:,}"


def generate_svg(template_path, output_path, values):
    content = template_path.read_text(encoding="utf-8")

    for key, value in values.items():
        placeholder = "{{" + key.upper() + "}}"

        content = content.replace(placeholder, str(value))

    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(content, encoding="utf-8")


def main():
    profile = load_profile()

    print("Fetching GitHub statistics...")

    stats = get_github_stats(profile["username"])

    values = {
        "name": profile["name"],
        "username": profile["username"],
        "role": profile["role"],
        "location": profile["location"],
        "repositories": format_number(stats["repositories"]),
        "stars": format_number(stats["stars"]),
        "followers": format_number(stats["followers"]),
        "following": format_number(stats["following"]),
        "contributions": format_number(stats["contributions"]),
        "current_1": profile["currently"][0],
        "current_2": profile["currently"][1],
        "current_3": profile["currently"][2],
    }

    print("Generating dark profile...")

    generate_svg(DARK_TEMPLATE, DARK_OUTPUT, values)

    print("Generating light profile...")

    generate_svg(LIGHT_TEMPLATE, LIGHT_OUTPUT, values)

    print("Profile successfully generated.")


if __name__ == "__main__":
    main()
