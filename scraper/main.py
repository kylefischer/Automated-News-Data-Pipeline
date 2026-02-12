"""Entry point: scrape Reddit and load to Snowflake."""

import logging
import sys

from reddit_scraper import fetch_top_posts
from snowflake_loader import load_posts

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def run_pipeline():
    posts = fetch_top_posts(subreddit="ArtificialInteligence", limit=5)
    logger.info("Found %d posts", len(posts))

    rows = load_posts(posts)
    logger.info("Pipeline complete: loaded %d posts", rows)


if __name__ == "__main__":
    run_pipeline()
