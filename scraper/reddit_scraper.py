"""Fetches top posts from a subreddit using Reddit's JSON endpoint."""

import logging
import requests
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


def fetch_top_posts(
    subreddit: str = "ArtificialInteligence", limit: int = 5
) -> list[dict]:
    url = f"https://www.reddit.com/r/{subreddit}/top/.json?limit={limit}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }

    logger.info("Fetching top %d posts from r/%s", limit, subreddit)
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    posts = []
    for child in response.json()["data"]["children"]:
        post = child["data"]
        posts.append(
            {
                "post_id": post["id"],
                "title": post["title"],
                "author": post["author"],
                "score": post["score"],
                "num_comments": post["num_comments"],
                "url": post["url"],
                "permalink": f"https://reddit.com{post['permalink']}",
                "created_utc": datetime.fromtimestamp(
                    post["created_utc"], tz=timezone.utc
                ),
                "scraped_at": datetime.now(timezone.utc),
            }
        )

    logger.info("Fetched %d posts", len(posts))
    return posts
