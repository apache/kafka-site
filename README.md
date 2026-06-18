# Apache Kafka Documentation Website

This repository contains the source for the Apache Kafka documentation website. The site is built using [Hugo](https://gohugo.io/) with the [Docsy](https://www.docsy.dev/) theme, providing a modern, maintainable, and feature-rich documentation experience.

## Structure of the Website

### Documentation Versioning

The documentation is organized by Kafka versions in the `content/en` directory:

```
content/en/
├── _index.md                 # Landing page
├── 42/                       # Latest version (4.2)
│   ├── apis/
│   ├── configuration/
│   ├── design/
│   └── ...
├── 41/                       # Previous version (4.1)
├── 40/                       # Version 4.0
└── ...
```

Each version directory contains the complete documentation for that specific Kafka release. The latest version (currently 4.2) is the default documentation shown to users.

> **Important**: The version-specific documentation (under directories like `42/`, `41/`, etc.) is sourced from the corresponding release branches in the [apache/kafka](https://github.com/apache/kafka) repository. The `docs` directory in each branch serves as the source of truth. During the website build process, this content is copied to the appropriate version directory. For more details, see [KIP-1133](https://cwiki.apache.org/confluence/display/KAFKA/KIP-1133%3A+AK+Documentation+and+Website+in+Markdown).

### Key Directories

- `assets/`: Contains customizations and overrides
  - `scss/`: Custom styling and theme variables
  - `icons/`: Custom icons and branding
  - `json/`: Search index configuration

- `layouts/`: Custom Hugo templates and overrides
  - `_default/`: Base templates
  - `partials/`: Reusable template components
  - `shortcodes/`: Custom Hugo shortcodes

- `data/`: JSON data files for dynamic content
  - `testimonials.json`: Powers the testimonials page
  - `committers.json`: Powers the committers page

### Features and Customizations

1. **Offline Search**: Enabled via `offlineSearch: true` in `hugo.yaml`, providing fast client-side search functionality
2. **Version Selector**: Allows users to switch between different Kafka versions
3. **Custom Shortcodes**: Located in `layouts/shortcodes/` for enhanced content formatting
4. **Custom Styling**: SCSS customizations in `assets/scss/`

## Updating the Documentation Website


### Adding documentation for a new release

When releasing a new documentation version (e.g., version 4.3 / "43"), follow these steps. For this example, we assume you are adding version **43** from the Kafka source branch `4.3`.

In the below examples, we assume the `apache/kafka` repository is checked out at `../kafka` relative to the `kafka-site` root.

#### 1. Setup Content Directory
Copy the documentation source files from the Kafka codebase to the website content directory, excluding images (which go to static). 

```bash
# Verify you are in the kafka-site root
mkdir -p content/en/43

# Copy docs from kafka repo (excluding images)
rsync -av --exclude 'images' ../kafka/docs/ content/en/43/
```

#### 2. Setup Static Assets
Copy images and Javadocs to the static directory. (`generated/` ships alongside the docs under `content/en/<version>/generated/` and is brought in by step 1's rsync.)

```bash
# Create versioned static directory
mkdir -p static/43

# Copy assets from kafka repo
cp -r ../kafka/docs/images static/43/
# Copy `javadoc` directory into `static/43`
```

#### 3. Run Replacement Script
Run the helper script to replace hardcoded version strings with dynamic placeholders (`{version}`) in the new content if needed. If we don't have any hardcoded version strings, we can skip this step.

```bash
./scripts/replace-version-links.sh 43
```

#### 4. Update Version Parameters in `hugo.yaml`
 
 Locate the **Version Configuration** block at the top of the `params` section (around line 245). Update the following fields:
 
 1.  `latest_version`: Set to the new version string (e.g., "43").
 2.  `latest_version_number`: Set to the new version number (e.g., "4.3").
 3.  `version`: Update to the new version (e.g., 4.3).
 4.  `url_latest_version`: Update the link (e.g., `/43/`).
 5.  `versions`:
     -   Add the new version to the top of the list.
     -   Mark the previous version as `archived_version: true`.
 
 ```yaml
   # Latest documentation version - UPDATE THIS WHEN RELEASING NEW VERSION
   latest_version: "43"
   latest_version_number: "4.3"
   
   # ...
   
   version: 4.3
 
   # ...
 
   url_latest_version: /43/
 
   # ...
 
   versions:
     - version: "4.3"
       url: /43/
     - version: "4.2"
       url: /42/
       archived_version: true
 ```

#### What Updates Automatically

Once you update the parameters above, the following are **automatically** updated:

**Menu Items:**
- DOCS → `/43/`
- Getting Started → `/43/getting-started/`
- APIs, Configuration, Design, Implementation, Operations, Security, Kafka Connect, Kafka Streams → all automatically updated

**Search Index:**
- The search index automatically includes the latest version directory (no manual update needed)
- Configured via offline search template `assets/json/offline-search-index.json`


### Managing Testimonials and Committers

#### Adding a New Testimonial

1. Add the company's logo to `static/images/powered-by/`
2. Add an entry to `data/testimonials.json`:
   ```json
   {
     "link": "https://company-website.com/",
     "logo": "company-logo.png",
     "logoBgColor": "#FFFFFF",
     "description": "Description of how the company uses Apache Kafka."
   }
   ```

#### Adding a New Committer

1. Add the committer's photo to `static/images/`
2. Add an entry to `data/committers.json`:
   ```json
   {
     "image": "/images/committer-photo.jpg",
     "name": "Committer Name",
     "title": "Committer, and PMC member",
     "linkedIn": "https://www.linkedin.com/in/committer/",
     "twitter": "https://twitter.com/committer",
     "github": "https://github.com/committer"
   }
   ```

The website uses Hugo's data templates to automatically generate the testimonials and committers pages from these JSON files. The templates are located in:
- `layouts/testimonials/`: Templates for rendering testimonials
- `layouts/community/`: Templates for rendering committer information

### Updating Content

1. For version-specific documentation:
   - Make changes in the appropriate version directory
   - Test changes locally before committing

2. For common content (e.g., landing page, community docs):
   - Edit files directly in `content/en/`

### Front Matter Guide

Detailed information about the Front Matter fields used in this site:

- `title`: The title of the page or post.
- `linkTitle`: (Optional) Short title used in sidebars and menus.
- `date`: Publication date (YYYY-MM-DD).
- `author`: Author name (often with GitHub handle). Typically used for blogs.
- `weight`: (Optional) Controls ordering in lists/menus (lower numbers appear first).
- `description`: (Optional) Brief summary for SEO and previews.
- `type`: Used to specify the layout type (e.g., `type: docs` for documentation pages).
- `aliases`: (Optional) List of old URLs that should redirect to this page.
- `url`: (Optional) Overrides the default URL path constructed from the filename.
- `redirect_to`: (Optional) Sets up a client-side meta-refresh redirect to an external URL.

For more details, see the [Hugo Front Matter Documentation](https://gohugo.io/content-management/front-matter/).

### Managing Redirects

#### Redirecting to an Internal URL

To redirect to an internal URL use the `aliases` Front Matter field.

Add one or more aliases to the page that should be the redirect destination.
See example in 4.2 blog entry content/en/blog/releases/ak-4.2.0.md (aliases used to preserve the initial blog url after it changed)

```yaml
---
title: Apache Kafka 4.2.0 Release Announcement
aliases:
  - /blog/2026/01/14/apache-kafka-4.2.0-release-announcement/
---
```

#### Redirecting to an External URL

To create a client-side redirect to an external URL, use the `redirect_to` Front Matter field.

1. Create a markdown file at the desired path (e.g., `content/en/KEYS.md` for `/KEYS`).
2. Add the `redirect_to` field in the Front Matter.

```yaml
---
title: KEYS Redirect
redirect_to: https://downloads.apache.org/kafka/KEYS
---
```

This generates a standard HTML meta-refresh redirect. Note that this is a client-side redirect; command-line tools like `curl` will not follow it automatically unless they parse the HTML.

### Dynamic Version Linking

To maintain version-agnostic documentation, we use a custom system that dynamically resolves version numbers in links and included files. This avoids the need to manually update hundreds of version strings (e.g., from "43" to "44") when releasing a new version.

The system relies on the special placeholder `{version}`.

#### How it Works

When the site is built, Hugo identifies the context of the current page (e.g., a file located in `content/en/43/`).
- If the page is in a versioned directory (like `43/`), `{version}` resolves to that version (`43`).
- If the page is outside a versioned directory (like `content/en/community/`), `{version}` falls back to the `latest_version` defined in `hugo.yaml`.

#### Supported Features

1.  **Markdown Links**:
    Use `{version}` in standard Markdown links.
    ```markdown
    [ConfigProvider]({version}/javadoc/org/apache/kafka/common/config/provider/ConfigProvider.html)
    => /43/javadoc/org/apache/kafka/common/config/provider/ConfigProvider.html
    ```
    *Implemented via the Render Hook: `layouts/_default/_markup/render-link.html`*

2.  **Include HTML Shortcode**:
    Use `{version}` in the `file` path for the `include-html` shortcode.
    ```markdown
    {{< include-html file="/static/{version}/generated/admin_client_config.html" >}}
    => reads content/en/43/generated/admin_client_config.html (4.2+)
       or /static/<v>/generated/... for older versions
    ```
    *Implemented in: `layouts/shortcodes/include-html.html`*

#### Helper Script

A script is available to automate the replacement of hardcoded version strings with dynamic placeholders for a specific version directory.

```bash
# Usage: ./scripts/replace-version-links.sh <version>
./scripts/replace-version-links.sh 43
```

This will recursively find and replace:
- `/<version>/javadoc` -> `/{version}/javadoc`
- `static/<version>/generated` -> `static/{version}/generated`
- `content/en/<version>/generated` -> `content/en/{version}/generated`

The `include-html` shortcode prefers the `content/en/<v>/generated/` location and falls back to `/static/<v>/generated/` for older versions whose files still live under `static/`.

### Adding a New Blog Post

Blog posts are located in `content/en/blog/`. The most common use case is adding a release announcement.

#### Adding a Release Blog Post

1. Create a new markdown file in `content/en/blog/releases/` using kebab-case for the filename (e.g., `ak-4.3.0.md`).
2. Add the required Front Matter. See the [Front Matter Guide](#front-matter-guide) for details on fields.

**Example Front Matter for a Release Post:**

```yaml
---
date: 2025-01-01
title: "Apache Kafka 4.3.0 Release Announcement"
linkTitle: "AK 4.3.0"
author: "Author Name (@github_handle)"
---
```

3. Write your content below the Front Matter.

## Build and Test

### Prerequisites

- Docker (20.10.0 or newer)
- Make

### Local Development

1. Start the development server with hot-reload:
   ```bash
   make serve
   ```
   This will:
   - Build the Hugo Docker image
   - Start a development server on http://localhost:1313
   - Watch for changes and automatically rebuild
   - Enable drafts and future posts

2. Build the site without starting the server:
   ```bash
   make build
   ```
   The built site will be available in the `output` directory.

### Production Build

1. Build and test the production image locally:
   ```bash
   make prod-run
   ```
   The site will be available at http://localhost:8080

2. Build production image for deployment:
   ```bash
   make prod-image
   ```
   This creates a multi-architecture Nginx image (ARM64 and AMD64) optimized for production.

### Cleaning Up

Remove built files and Docker images:
```bash
make clean
```

## Updating the website

After a GitHub PR was merged, the "Build and Deploy Site" GitHub Actions job, updates the [staging website](https://kafka.staged.apache.org/).
Please verify if all changes are correct.
Afterwards, you can re-run the same job manually via the GitHub WebUI, selecting "Check to update live website".


## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally using `make serve`
5. Submit a pull request

For more details about the migration to Markdown and the overall architecture, see [KIP-1133](https://cwiki.apache.org/confluence/display/KAFKA/KIP-1133%3A+AK+Documentation+and+Website+in+Markdown).
