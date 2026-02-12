select
    post_id,
    title,
    author,
    score,
    num_comments,
    engagement_ratio,
    url,
    permalink,
    created_utc,
    load_date,
    daily_rank
from {{ ref('int_reddit_posts_enriched') }}
where daily_rank <= 5
