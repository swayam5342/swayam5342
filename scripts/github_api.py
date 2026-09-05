import os
import requests


GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"


def get_github_stats(username: str) -> dict:
    token = os.getenv("GITHUB_TOKEN")

    if not token:
        raise RuntimeError("GITHUB_TOKEN environment variable is missing")

    headers = {"Authorization": f"Bearer {token}"}

    query = """
    query($username: String!) {
      user(login: $username) {

        repositories(
          first: 100
          ownerAffiliations: OWNER
        ) {
          totalCount

          nodes {
            stargazerCount
          }
        }

        followers {
          totalCount
        }

        following {
          totalCount
        }

        contributionsCollection {
          contributionCalendar {
            totalContributions
          }
        }
      }
    }
    """

    variables = {"username": username}

    response = requests.post(
        GITHUB_GRAPHQL_URL,
        headers=headers,
        json={"query": query, "variables": variables},
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    if "errors" in data:
        raise RuntimeError(data["errors"])

    user = data["data"]["user"]

    repositories = user["repositories"]["nodes"]

    total_stars = sum(repo["stargazerCount"] for repo in repositories)

    return {
        "repositories": user["repositories"]["totalCount"],
        "stars": total_stars,
        "followers": user["followers"]["totalCount"],
        "following": user["following"]["totalCount"],
        "contributions": (
            user["contributionsCollection"]["contributionCalendar"][
                "totalContributions"
            ]
        ),
    }
