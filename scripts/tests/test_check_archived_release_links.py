import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from scripts.check_archived_release_links import find_bad_links, main


class CheckArchivedReleaseLinksTest(unittest.TestCase):
    def check(self, content):
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as test_file:
            test_file.write(content)
            path = Path(test_file.name)

        try:
            return find_bad_links(path)
        finally:
            path.unlink()

    def test_allows_archive_apache_links_in_archived_releases(self):
        bad_links = self.check(
            """\
## Archived Releases

### 4.2.0

* [Release Notes](https://archive.apache.org/dist/kafka/4.2.0/RELEASE_NOTES.html)
* Source download: [kafka-4.2.0-src.tgz](https://archive.apache.org/dist/kafka/4.2.0/kafka-4.2.0-src.tgz)
"""
        )

        self.assertEqual([], bad_links)

    def test_rejects_closer_lua_links_in_archived_releases(self):
        bad_links = self.check(
            """\
## Archived Releases

### 4.2.0

* Source download: [kafka-4.2.0-src.tgz](https://www.apache.org/dyn/closer.lua/kafka/4.2.0/kafka-4.2.0-src.tgz?action=download)
"""
        )

        self.assertEqual(
            [
                (
                    5,
                    "4.2.0",
                    "https://www.apache.org/dyn/closer.lua/kafka/4.2.0/kafka-4.2.0-src.tgz?action=download",
                )
            ],
            bad_links,
        )

    def test_rejects_scheme_relative_active_download_link(self):
        bad_links = self.check(
            """\
## Archived Releases

### 4.2.0

* Source: [src](//downloads.apache.org/kafka/4.2.0/src.tgz)
"""
        )

        self.assertEqual(
            [(5, "4.2.0", "//downloads.apache.org/kafka/4.2.0/src.tgz")],
            bad_links,
        )

    def test_rejects_downloads_apache_links_in_archived_releases(self):
        bad_links = self.check(
            """\
## Archived Releases

### 4.2.0

* Source signature: [asc](https://downloads.apache.org/kafka/4.2.0/kafka-4.2.0-src.tgz.asc)
"""
        )

        self.assertEqual(
            [(5, "4.2.0", "https://downloads.apache.org/kafka/4.2.0/kafka-4.2.0-src.tgz.asc")],
            bad_links,
        )

    def test_rejects_dlcdn_apache_links_in_archived_releases(self):
        bad_links = self.check(
            """\
## Archived Releases

### 4.2.0

* Source download: [src](https://dlcdn.apache.org/kafka/4.2.0/kafka-4.2.0-src.tgz)
"""
        )

        self.assertEqual(
            [(5, "4.2.0", "https://dlcdn.apache.org/kafka/4.2.0/kafka-4.2.0-src.tgz")],
            bad_links,
        )

    def test_allows_apache_keys_link_in_archived_releases(self):
        bad_links = self.check(
            """\
## Archived Releases

### 4.2.0

* Verify with [KEYS](https://downloads.apache.org/kafka/KEYS).
"""
        )

        self.assertEqual([], bad_links)

    def test_rejects_case_insensitive_host_with_explicit_port(self):
        bad_links = self.check(
            """\
## Archived Releases

### 4.2.0

* Source signature: [asc](HTTPS://DOWNLOADS.APACHE.ORG:443/kafka/4.2.0/kafka-4.2.0-src.tgz.asc)
"""
        )

        self.assertEqual(
            [
                (
                    5,
                    "4.2.0",
                    "HTTPS://DOWNLOADS.APACHE.ORG:443/kafka/4.2.0/kafka-4.2.0-src.tgz.asc",
                )
            ],
            bad_links,
        )

    def test_allows_non_release_download_links_in_archived_releases(self):
        bad_links = self.check(
            """\
## Archived Releases

### 4.2.0

* Docker image: [apache/kafka:4.2.0](https://hub.docker.com/layers/apache/kafka/4.2.0).
* Blog post: [announcement](https://kafka.apache.org/blog/2026/02/17/apache-kafka-4.2.0-release-announcement/)
* Upgrade Notes: [upgrade](https://kafka.apache.org/42/getting-started/upgrade/)
"""
        )

        self.assertEqual([], bad_links)

    def test_allows_active_download_links_in_supported_releases(self):
        bad_links = self.check(
            """\
## Supported releases

### 4.3.0

* Source download: [kafka-4.3.0-src.tgz](https://www.apache.org/dyn/closer.lua/kafka/4.3.0/kafka-4.3.0-src.tgz?action=download)
* Source signature: [asc](https://downloads.apache.org/kafka/4.3.0/kafka-4.3.0-src.tgz.asc)

## Archived Releases

### 4.2.0

* Source download: [kafka-4.2.0-src.tgz](https://archive.apache.org/dist/kafka/4.2.0/kafka-4.2.0-src.tgz)
"""
        )

        self.assertEqual([], bad_links)

    def test_stops_at_next_h2_after_archived_releases(self):
        bad_links = self.check(
            """\
## Archived Releases

### 4.2.0

* Source download: [kafka-4.2.0-src.tgz](https://archive.apache.org/dist/kafka/4.2.0/kafka-4.2.0-src.tgz)

## Other Links

* Active download example: [src](https://downloads.apache.org/kafka/4.3.0/kafka-4.3.0-src.tgz.asc)
"""
        )

        self.assertEqual([], bad_links)

    def test_ignores_active_download_links_in_fenced_code_blocks(self):
        bad_links = self.check(
            """\
## Archived Releases

### 4.2.0

```text
https://downloads.apache.org/kafka/4.2.0/src.tgz
```
* Source: [src](https://archive.apache.org/dist/kafka/4.2.0/src.tgz)
"""
        )

        self.assertEqual([], bad_links)

    def test_accepts_indented_archived_header_with_hugo_id(self):
        bad_links = self.check(
            """\
   ## Archived Releases {#archived-releases}

   ### 4.2.0

* Source: [src](https://archive.apache.org/dist/kafka/4.2.0/src.tgz)
"""
        )

        self.assertEqual([], bad_links)

    def test_rejects_missing_archived_releases_section(self):
        with self.assertRaisesRegex(ValueError, "missing required"):
            self.check("## Supported releases\n")

    def test_main_reports_missing_section_without_traceback(self):
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as test_file:
            test_file.write("## Supported releases\n")
            path = Path(test_file.name)

        stderr = io.StringIO()
        try:
            with contextlib.redirect_stderr(stderr):
                exit_code = main([str(path)])
        finally:
            path.unlink()

        self.assertEqual(2, exit_code)
        self.assertIn("missing required '## Archived Releases' section", stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())

    def test_main_reports_missing_file_without_traceback(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "missing-kafka-downloads.md"
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                exit_code = main([str(path)])

        self.assertEqual(2, exit_code)
        self.assertIn("unable to read file", stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
