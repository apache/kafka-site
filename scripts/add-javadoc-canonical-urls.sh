#!/bin/bash

# Script to add or update <link rel="canonical"> tags in all Javadoc HTML files
# across all versions, pointing to the latest version that contains each page.
#
# For pages that exist in the latest stable version, the canonical URL points there.
# For pages removed in newer versions (e.g., deprecated APIs), the canonical URL
# points to the newest version that still contains the page.
#
# Usage: ./scripts/add-javadoc-canonical-urls.sh [latest_version]
# Example: ./scripts/add-javadoc-canonical-urls.sh 42
#
# If no version argument is provided, reads latest_version from hugo.yaml.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SITE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Determine latest version
if [ -n "$1" ]; then
    LATEST_VERSION="$1"
else
    LATEST_VERSION=$(grep 'latest_version:' "$SITE_ROOT/hugo.yaml" | head -1 | sed 's/.*latest_version: *"\([^"]*\)".*/\1/')
    if [ -z "$LATEST_VERSION" ]; then
        echo "Error: Could not determine latest_version from hugo.yaml"
        exit 1
    fi
fi

echo "Latest version: $LATEST_VERSION"

# Detect platform for sed -i compatibility
if [[ "$OSTYPE" == "darwin"* ]]; then
    SED_INPLACE=(sed -i '')
else
    SED_INPLACE=(sed -i)
fi

STATIC_DIR="$SITE_ROOT/static"

# Build sorted list of versions (newest first).
# Version directory names: 082, 090, 0100, 0101, 0102, 0110, 10, 11, 20, ..., 42
# Sort by mapping to a comparable numeric value:
# Old scheme (3-4 digits): 082->82, 090->90, 0100->100, 0101->101, 0102->102, 0110->110
# New scheme (2 digits):   10->1000, 11->1100, 20->2000, ..., 42->4200
version_sort_key() {
    local v="$1"
    if [ ${#v} -ge 3 ]; then
        echo "$((10#$v))"
    else
        echo "$((10#$v * 100))"
    fi
}

ALL_VERSIONS=()
for d in "$STATIC_DIR"/*/javadoc; do
    [ -d "$d" ] || continue
    ALL_VERSIONS+=("$(basename "$(dirname "$d")")")
done

SORTED_VERSIONS=()
while IFS= read -r v; do
    SORTED_VERSIONS+=("$v")
done < <(for v in "${ALL_VERSIONS[@]}"; do echo "$(version_sort_key "$v") $v"; done | sort -rn -k1,1 | awk '{print $2}')

echo "Versions (newest first): ${SORTED_VERSIONS[*]}"

# Phase 1: Build a mapping file of relative_path -> canonical_version.
# For each unique page, the canonical version is the newest version containing it.
echo "Building canonical version map..."
CANON_MAP=$(mktemp)
trap "rm -f '$CANON_MAP'" EXIT

for VERSION in "${SORTED_VERSIONS[@]}"; do
    VERSION_DIR="$STATIC_DIR/$VERSION/javadoc"
    find "$VERSION_DIR" -name '*.html' -type f -print0 | while IFS= read -r -d '' HTML_FILE; do
        REL_PATH="${HTML_FILE#$VERSION_DIR/}"
        echo "$REL_PATH"
    done
done | awk -v versions="${SORTED_VERSIONS[*]}" '
BEGIN {
    n = split(versions, v, " ")
    for (i = 1; i <= n; i++) order[v[i]] = i
}
!seen[$0]++ { print $0 }
' > /dev/null

# Simpler approach: for each version (newest first), record paths not yet seen
for VERSION in "${SORTED_VERSIONS[@]}"; do
    VERSION_DIR="$STATIC_DIR/$VERSION/javadoc"
    find "$VERSION_DIR" -name '*.html' -type f -print0 | while IFS= read -r -d '' HTML_FILE; do
        REL_PATH="${HTML_FILE#$VERSION_DIR/}"
        echo "$REL_PATH	$VERSION"
    done
done | awk -F'\t' '!seen[$1]++ { print }' > "$CANON_MAP"

UNIQUE_PAGES=$(wc -l < "$CANON_MAP" | tr -d ' ')
echo "Found $UNIQUE_PAGES unique Javadoc pages across all versions."

# Phase 2: Apply canonical tags to all HTML files.
FILE_COUNT=0

for VERSION_DIR in "$STATIC_DIR"/*/javadoc; do
    [ -d "$VERSION_DIR" ] || continue

    echo "Processing $VERSION_DIR ..."

    while IFS= read -r -d '' HTML_FILE; do
        REL_PATH="${HTML_FILE#$VERSION_DIR/}"

        # Look up the canonical version for this relative path
        CANON_VERSION=$(grep -m1 "^${REL_PATH}	" "$CANON_MAP" | cut -f2)
        if [ -z "$CANON_VERSION" ]; then
            # Fallback: use latest version
            CANON_VERSION="$LATEST_VERSION"
        fi

        CANONICAL_URL="https://kafka.apache.org/${CANON_VERSION}/javadoc/${REL_PATH}"
        CANONICAL_TAG="<link rel=\"canonical\" href=\"${CANONICAL_URL}\">"

        if grep -qi 'rel="canonical"' "$HTML_FILE" 2>/dev/null; then
            "${SED_INPLACE[@]}" "s|<[Ll][Ii][Nn][Kk] [Rr][Ee][Ll] *=[\"'] *canonical[\"'][^>]*>|${CANONICAL_TAG}|g" "$HTML_FILE"
        else
            "${SED_INPLACE[@]}" "s|<[Hh][Ee][Aa][Dd]>|&\n${CANONICAL_TAG}|" "$HTML_FILE"
        fi

        FILE_COUNT=$((FILE_COUNT + 1))
    done < <(find "$VERSION_DIR" -name '*.html' -type f -print0)
done

echo "Done! Processed $FILE_COUNT HTML files."
