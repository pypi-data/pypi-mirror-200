from datetime import datetime, timedelta
from functools import partial
from subprocess import run
from time import mktime

import feedparser

from rssnotify.config import config


def parse_rss(
    url: str, timestamp: float, kw: list[str]
) -> list[tuple[str, str]]:
    urls: list[tuple[str, str]] = []
    rss = feedparser.parse(url)

    for entry in filter(
        lambda e: mktime(e.published_parsed) > timestamp, rss.entries
    ):
        if any(k for k in kw if k in entry.title.upper()):
            urls.append((entry.title, entry.link))
    return urls


def parse_all() -> bool:
    returncode = True

    timestamp = (
        datetime.now() - timedelta(hours=config.since_hours)
    ).timestamp()

    news: list[tuple[str, str]] = list(
        *map(
            partial(parse_rss, timestamp=timestamp, kw=config.keywords),
            config.urls,
        )
    )

    if not config.command:
        return returncode

    for topic in news:
        cmd = [
            arg.replace("$TITLE", topic[0]).replace("$LINK", topic[1])
            for arg in config.command
        ]
        print(cmd)
        returncode &= run(cmd).returncode == 0

    return returncode
