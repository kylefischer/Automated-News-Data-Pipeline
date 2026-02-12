"""Unit tests for the Reddit scraper using mocked HTTP responses."""

import sys
import os
from unittest.mock import patch, MagicMock
from datetime import timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scraper"))
from reddit_scraper import fetch_top_posts

MOCK_REDDIT_RESPONSE = {
    "data": {
        "children": [
            {
                "data": {
                    "id": "abc123",
                    "title": "Test Post About AI Breakthroughs",
                    "author": "test_user",
                    "score": 150,
                    "num_comments": 42,
                    "url": "https://example.com/ai-article",
                    "permalink": "/r/ArtificialInteligence/comments/abc123/test_post/",
                    "created_utc": 1707400000.0,
                }
            },
            {
                "data": {
                    "id": "def456",
                    "title": "Another AI Post",
                    "author": "another_user",
                    "score": 89,
                    "num_comments": 15,
                    "url": "https://example.com/another-article",
                    "permalink": "/r/ArtificialInteligence/comments/def456/another_post/",
                    "created_utc": 1707300000.0,
                }
            },
        ]
    }
}


def _mock_get(response_data=MOCK_REDDIT_RESPONSE):
    mock_response = MagicMock()
    mock_response.json.return_value = response_data
    mock_response.raise_for_status = MagicMock()
    return mock_response


@patch("reddit_scraper.requests.get")
def test_returns_correct_count(mock_get):
    mock_get.return_value = _mock_get()
    assert len(fetch_top_posts(limit=2)) == 2


@patch("reddit_scraper.requests.get")
def test_extracts_all_fields(mock_get):
    mock_get.return_value = _mock_get()
    post = fetch_top_posts()[0]
    expected = [
        "post_id",
        "title",
        "author",
        "score",
        "num_comments",
        "url",
        "permalink",
        "created_utc",
        "scraped_at",
    ]
    for field in expected:
        assert field in post, f"Missing field: {field}"


@patch("reddit_scraper.requests.get")
def test_parses_data_correctly(mock_get):
    mock_get.return_value = _mock_get()
    post = fetch_top_posts()[0]
    assert post["post_id"] == "abc123"
    assert post["title"] == "Test Post About AI Breakthroughs"
    assert post["score"] == 150
    assert (
        post["permalink"]
        == "https://reddit.com/r/ArtificialInteligence/comments/abc123/test_post/"
    )


@patch("reddit_scraper.requests.get")
def test_timestamps_are_utc(mock_get):
    mock_get.return_value = _mock_get()
    post = fetch_top_posts()[0]
    assert post["created_utc"].tzinfo == timezone.utc
    assert post["scraped_at"].tzinfo == timezone.utc


@patch("reddit_scraper.requests.get")
def test_calls_correct_url(mock_get):
    mock_get.return_value = _mock_get()
    fetch_top_posts(subreddit="MachineLearning", limit=10)
    called_url = mock_get.call_args[0][0]
    assert "MachineLearning" in called_url
    assert "limit=10" in called_url


@patch("reddit_scraper.requests.get")
def test_empty_response(mock_get):
    mock_get.return_value = _mock_get({"data": {"children": []}})
    assert fetch_top_posts() == []
