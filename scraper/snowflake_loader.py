"""Loads scraped Reddit posts into Snowflake using MERGE (upsert)."""

import logging
import os
from dotenv import load_dotenv
import snowflake.connector

logger = logging.getLogger(__name__)


def get_connection():
    load_dotenv()
    return snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        role=os.getenv("SNOWFLAKE_ROLE"),
    )


def load_posts(posts: list[dict]) -> int:
    if not posts:
        return 0

    conn = get_connection()
    cursor = conn.cursor()

    # MERGE/UPSERT -> update or insert of not exisiting,
    # makes pipeline idempotent (safe to re-run without duplicates or side effects))
    merge_sql = """
        MERGE INTO RAW.REDDIT_POSTS AS target
        USING (SELECT %s AS post_id, %s AS title, %s AS author, %s AS score, 
                      %s AS num_comments, %s AS url, %s AS permalink, 
                      %s AS created_utc, %s AS scraped_at, CURRENT_DATE() AS load_date) AS source
        ON target.post_id = source.post_id AND target.load_date = source.load_date
        WHEN MATCHED THEN UPDATE SET
            score = source.score,
            num_comments = source.num_comments,
            scraped_at = source.scraped_at
        WHEN NOT MATCHED THEN INSERT 
            (post_id, title, author, score, num_comments, url, permalink, created_utc, scraped_at, load_date)
        VALUES 
            (source.post_id, source.title, source.author, source.score, source.num_comments, 
             source.url, source.permalink, source.created_utc, source.scraped_at, source.load_date)
    """

    rows_affected = 0
    for post in posts:
        cursor.execute(
            merge_sql,
            (
                post["post_id"],
                post["title"],
                post["author"],
                post["score"],
                post["num_comments"],
                post["url"],
                post["permalink"],
                post["created_utc"],
                post["scraped_at"],
            ),
        )
        rows_affected += 1

    conn.commit()
    cursor.close()
    conn.close()

    logger.info("Loaded %d posts to Snowflake", rows_affected)
    return rows_affected
