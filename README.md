# Apache Kafka Documentation Website

This repository contains the source for the Apache Kafka documentation website. The site is built using [Hugo](https://gohugo.io/) with the [Docsy](https://www.docsy.dev/) theme, providing a modern, maintainable, and feature-rich documentation experience.

## Structure of the Website

### Documentation Versioning

The documentation is organized by Kafka versions in the `content/en` directory:

```
content/en/
├── _index.md                 # Landing page
├── 40/                       # Latest version (4.0)
│   ├── apis/
│   ├── configuration/
│   ├── design/
│   └── ...
├── 39/                       # Previous version (3.9)
├── 38/                       # Version 3.8
└── ...
```

Each version directory contains the complete documentation for that specific Kafka release. The latest version (currently 4.0) is the default documentation shown to users.

> **Important**: The version-specific documentation (under directories like `40/`, `39/`, etc.) is sourced from the corresponding release branches in the [apache/kafka](https://github.com/apache/kafka) repository. The `docs` directory in each branch serves as the source of truth. During the website build process, this content is copied to the appropriate version directory. For more details, see [KIP-1133](https://cwiki.apache.org/confluence/display/KAFKA/KIP-1133%3A+AK+Documentation+and+Website+in+Markdown).

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

### Adding a New Version

1. Create a new directory in `content/en/` for the new version (e.g., `41/` for version 4.1)
2. Update `hugo.yaml` to add the new version:
   ```yaml
   versions:
     - version: "4.1"         # Add new version at the top
       url: /41/
     - version: "4.0"         # Update previous latest
       url: /40/
       archived_version: true  # Mark as archived
     # ... other versions ...
   ```
3. Update the latest version pointer:
   ```yaml
   params:
     version: 4.1             # Update version number
     url_latest_version: /41/ # Update latest version URL
   ```

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

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally using `make serve`
5. Submit a pull request

For more details about the migration to Markdown and the overall architecture, see [KIP-1133](https://cwiki.apache.org/confluence/display/KAFKA/KIP-1133%3A+AK+Documentation+and+Website+in+Markdown).
