select
    post_id,
    title,
    author,
    score,
    num_comments,
    url,
    permalink,
    created_utc,
    scraped_at,
    load_date
from {{ source('raw', 'reddit_posts') }}
