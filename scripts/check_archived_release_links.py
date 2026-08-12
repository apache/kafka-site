#!/usr/bin/env python3

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


ARCHIVED_RELEASES_HEADER = re.compile(
    r"^[ \t]{0,3}##[ \t]+Archived Releases(?:[ \t]+\{#[^}]+\})?[ \t]*$",
    re.IGNORECASE,
)
NEXT_H2_HEADER = re.compile(r"^[ \t]{0,3}##[ \t]+")
RELEASE_HEADER = re.compile(r"^[ \t]{0,3}###[ \t]+(.+?)[ \t]*$")
FENCE_START = re.compile(r"^[ \t]{0,3}(`{3,}|~{3,})")
URL = re.compile(r"(?:https?:)?//[^)\s>]+", re.IGNORECASE)
ACTIVE_DOWNLOAD_HOSTS = {"dlcdn.apache.org", "downloads.apache.org"}
ACTIVE_REDIRECT_PATH = re.compile(r"^/dyn/closer\.lua/kafka/")


def archived_release_lines(lines):
    in_archived_releases = False
    fence_character = None
    fence_length = 0

    for line_number, line in enumerate(lines, start=1):
        if fence_character:
            closing_fence = re.fullmatch(
                rf"[ \t]{{0,3}}{re.escape(fence_character)}{{{fence_length},}}[ \t]*",
                line,
            )
            if closing_fence:
                fence_character = None
                fence_length = 0
            continue

        fence_match = FENCE_START.match(line)
        if fence_match:
            marker = fence_match.group(1)
            fence_character = marker[0]
            fence_length = len(marker)
            continue

        if ARCHIVED_RELEASES_HEADER.match(line):
            in_archived_releases = True
            continue

        if in_archived_releases and NEXT_H2_HEADER.match(line):
            break

        if in_archived_releases:
            yield line_number, line

    if not in_archived_releases:
        raise ValueError("missing required '## Archived Releases' section")


def is_active_download_url(url):
    parsed = urlparse(url)
    hostname = (parsed.hostname or "").lower()
    if hostname in ACTIVE_DOWNLOAD_HOSTS and parsed.path.startswith("/kafka/"):
        return parsed.path != "/kafka/KEYS"
    return hostname == "www.apache.org" and ACTIVE_REDIRECT_PATH.match(parsed.path) is not None


def find_bad_links(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    bad_links = []
    current_release = None

    for line_number, line in archived_release_lines(lines):
        release_match = RELEASE_HEADER.match(line)
        if release_match:
            current_release = release_match.group(1)

        for url in URL.findall(line):
            if is_active_download_url(url):
                bad_links.append((line_number, current_release, url))

    return bad_links


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Check that archived Kafka release links use archive.apache.org."
    )
    parser.add_argument(
        "downloads_file",
        nargs="?",
        default="content/en/community/downloads.md",
        help="Path to the downloads markdown file.",
    )
    args = parser.parse_args(argv)

    downloads_file = Path(args.downloads_file)
    try:
        bad_links = find_bad_links(downloads_file)
    except OSError as error:
        reason = error.strerror or str(error)
        print(f"{downloads_file}: unable to read file: {reason}", file=sys.stderr)
        return 2
    except ValueError as error:
        print(f"{downloads_file}: {error}", file=sys.stderr)
        return 2

    if not bad_links:
        print(f"{downloads_file}: archived release links use archive.apache.org")
        return 0

    print(
        "Archived release links must use https://archive.apache.org/dist/kafka/ "
        "instead of active download URLs.",
        file=sys.stderr,
    )
    for line_number, release, url in bad_links:
        release_label = release or "unknown release"
        print(f"{downloads_file}:{line_number}: {release_label}: {url}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
