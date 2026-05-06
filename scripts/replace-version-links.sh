#!/bin/bash

# Script to replace hardcoded version links with {version} placeholder
# Usage: ./scripts/replace-version-links.sh <version>

set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <version>"
    echo "Example: $0 39"
    exit 1
fi

VERSION=$1
CONTENT_DIR="content/en/$VERSION"

if [ ! -d "$CONTENT_DIR" ]; then
    echo "Error: Directory $CONTENT_DIR does not exist."
    exit 1
fi

echo "Processing version: $VERSION in $CONTENT_DIR"

# 1. Replace Javadoc links
# Pattern: /<VERSION>/javadoc -> /{version}/javadoc
echo "Replacing /$VERSION/javadoc with /{version}/javadoc..."
find "$CONTENT_DIR" -name "*.md" -type f -print0 | xargs -0 sed -i '' "s|/$VERSION/javadoc|/{version}/javadoc|g"

# 2. Strip the legacy static include prefix so include-html calls become
#    version-relative (resolved by the shortcode against content/en/<v>/generated).
# Pattern: file="/static/<VERSION>/generated/ -> file="generated/
echo "Rewriting include-html paths to version-relative form..."
find "$CONTENT_DIR" -name "*.md" -type f -print0 | xargs -0 sed -i '' "s|file=\"/static/$VERSION/generated/|file=\"generated/|g"
find "$CONTENT_DIR" -name "*.md" -type f -print0 | xargs -0 sed -i '' "s|file=\"/static/{version}/generated/|file=\"generated/|g"

echo "Done!"
