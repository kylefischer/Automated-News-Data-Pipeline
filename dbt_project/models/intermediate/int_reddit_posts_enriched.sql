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
    load_date,
    round(num_comments / nullif(score, 0), 2) as engagement_ratio,
    row_number() over (partition by load_date order by score desc) as daily_rank
from {{ ref('stg_reddit_posts') }}
