import re
import sys
import os
import argparse
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin

ROOT_URL = 'http://localhost:1313'

# paths relative to this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REDIRECT_FILE = os.path.join(SCRIPT_DIR, '../layouts/shortcodes/doc-redirect.html')
CONTENT_DIR = os.path.join(SCRIPT_DIR, '../content/en')

# Sample of deep streams paths to verify
STREAMS_PATHS = [
    "streams",
    "streams/upgrade-guide",
    "streams/developer-guide",
    "streams/core-concepts",
    "streams/quickstart",
    "streams/architecture"
]

def get_versions():
    """Scans content directory for version folders (starting with digits)."""
    versions = []
    try:
        if not os.path.exists(CONTENT_DIR):
            print(f"Warning: {CONTENT_DIR} not found. scanning skipped.")
            return []
        
        for item in os.listdir(CONTENT_DIR):
            if os.path.isdir(os.path.join(CONTENT_DIR, item)) and re.match(r'^\d+', item):
                versions.append(item)
    except Exception as e:
        print(f"Error scanning versions: {e}")
    
    # Sort versions loosely (alpha sort is distinct from numeric but sufficient for list)
    return sorted(versions)

def parse_redirects(file_path):
    """Parses the JS object map from the shortcode file."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        sys.exit(1)
    
    match = re.search(r'var hashIncludedMap = \{([\s\S]*?)\};', content)
    if not match:
        print(f"Error: Could not find hashIncludedMap in {file_path}")
        return {}

    map_content = match.group(1)
    redirects = {}
    
    # Regex to find key-value pairs: "#key": "value"
    pattern = re.compile(r'"(#[^"]+)":\s*"([^"]+)"')
    
    for line in map_content.splitlines():
        m = pattern.search(line)
        if m:
            redirects[m.group(1)] = m.group(2)
            
    return redirects

def check_url(url):
    """
    Checks if the target url exists on the server using urllib.
    Returns (status_code, anchor_found, error_msg)
    """
    path_part = url
    anchor = None
    if '#' in url:
        # split just the anchor
        base, anchor = url.split('#', 1)
        # we check the base url
        check_target = base
    else:
        check_target = url
        
    try:
        with urlopen(check_target, timeout=2) as response:
            status = response.getcode()
            content = response.read().decode('utf-8', errors='ignore')
            
            if anchor:
                # Naive check for anchor in HTML
                if f'id="{anchor}"' in content or f'name="{anchor}"' in content:
                    return status, True, None
                else:
                    return status, False, f"Anchor #{anchor} not found in page"
            
            return status, True, None

    except HTTPError as e:
        return e.code, False, f"HTTP {e.code}"
    except URLError as e:
        return 0, False, f"Connection Failed: {e.reason}"
    except Exception as e:
        return 0, False, str(e)

def verify_single_redirect(source_path, target_path, description):
    """
    Verifies that:
    1. Source path exists (should be the shadow file serving redirect)
    2. Target path exists (the destination content)
    """
    # Check Source
    source_url = urljoin(ROOT_URL, source_path)
    s_status, _, s_msg = check_url(source_url)
    
    # Check Target
    target_url = urljoin(ROOT_URL, target_path)
    t_status, t_anchor_ok, t_msg = check_url(target_url)
    
    res = {
        "desc": description,
        "source": source_path,
        "target": target_path,
        "s_ok": s_status == 200,
        "t_ok": t_status == 200 and t_anchor_ok,
        "s_msg": s_msg,
        "t_msg": t_msg
    }
    return res

def main():
    print(f"Parsing {REDIRECT_FILE}...")
    redirects = parse_redirects(REDIRECT_FILE)
    print(f"Found {len(redirects)} hash-map redirects.")
    
    versions = get_versions()
    print(f"Found versions: {versions}")
    
    if not versions:
        # Fallback if content dir not found or empty
        print("No versions found. Defaulting to '41' for testing.")
        versions = ['41']

    # We generally treat the last one as latest for this script's purpose if we need a default,
    # but actual logic relies on site config.
    # For global /documentation/ check, we assume '41' (latest) is target. 
    # TODO: parse config for latest_version if needed. Hardcoding for now.
    LATEST_VERSION = '41'
    
    results = []
    
    print("-" * 50)
    print("Verifying Versioned Hash Redirects (Sample: First and Last version)")
    # Test a subset of versions to avoid thousands of requests
    test_versions = [versions[0], versions[-3], versions[-2], versions[-1]] if len(versions) > 4 else versions
    
    # Add LATEST_VERSION to test if not present (to verify global redirect logic)
    if LATEST_VERSION not in test_versions:
        test_versions.append(LATEST_VERSION)
        
    for ver in test_versions:
        print(f"Checking hash redirects for version: {ver}")
        # For each hash, Source: /{ver}/documentation/#{key} -> Target: /{ver}/{value}
        # Note: We can't check Source existence for hash-only diff easily with urllib without full path,
        # but the source file is /{ver}/documentation/_index.md used for ALL hashes.
        # So we verify /{ver}/documentation/ once.
        
        doc_root = f"/{ver}/documentation/"
        s_res = verify_single_redirect(doc_root, f"/{ver}/getting-started/introduction", f"Doc Root {ver}")
        if not s_res["s_ok"]:
             print(f"[FAIL] {doc_root} missing (Shadow file).")
        
        # Now verify targets for all hashes for this version
        for key, path_suffix in redirects.items():
            target = f"/{ver}/{path_suffix}"
            t_res = verify_single_redirect(doc_root + key, target, f"{doc_root}{key}")
            # We ignore source status here as we checked root above, focus on target
            if t_res["t_ok"]:
                 # print(f"[PASS] {key} -> {target}")
                 pass
            else:
                 print(f"[FAIL] {doc_root}{key} -> {target} : {t_res['t_msg']}")
                 results.append(t_res)

    print("-" * 50)
    print("Verifying Deep Streams Redirects")
    
    # 1. Versioned
    for ver in test_versions:
        for path in STREAMS_PATHS:
            # removing 'documentation/' from /{ver}/documentation/streams/... -> /{ver}/streams/...
            source = f"/{ver}/documentation/{path}"
            target = f"/{ver}/{path}"
            
            # For 'streams' (no slash), it might redirect to streams/
            # For this test, we construct source/target precisely.
            
            res = verify_single_redirect(source, target, f"Deep Link {ver} {path}")
            if res["s_ok"] and res["t_ok"]:
                print(f"[PASS] {source} -> {target}")
            else:
                msg = []
                if not res["s_ok"]: msg.append(f"Source missing ({res['s_msg']})")
                if not res["t_ok"]: msg.append(f"Target missing ({res['t_msg']})")
                print(f"[FAIL] {source} -> {target} : {', '.join(msg)}")
                results.append(res)
                
    # 2. Global (latest)
    print("Verifying Global Deep Streams Redirects")
    for path in STREAMS_PATHS:
        # /documentation/streams/... -> /41/streams/...
        source = f"/documentation/{path}"
        target = f"/{LATEST_VERSION}/{path}"
        
        res = verify_single_redirect(source, target, f"Deep Link Global {path}")
        if res["s_ok"] and res["t_ok"]:
            print(f"[PASS] {source} -> {target}")
        else:
            msg = []
            if not res["s_ok"]: msg.append(f"Source missing ({res['s_msg']})")
            if not res["t_ok"]: msg.append(f"Target missing ({res['t_msg']})")
            print(f"[FAIL] {source} -> {target} : {', '.join(msg)}")
            results.append(res)
            
    print("-" * 50)
    print("Verifying Legacy documentation.html")
    # /documentation.html#design -> /41/design/design/#motivation (hash map check)
    # We check source existence
    source_legacy = "/documentation.html"
    l_res = verify_single_redirect(source_legacy, source_legacy, "Legacy Root") # Target is itself for existence check, or verify redirect target?
    # verify_single_redirect checks content at target.
    # To verify partial functionality we can just check if source returns 200.
    # But verify_single_redirect logic: source_url check (s_ok), target_url check (t_ok).
    # We can check a known mapping.
    
    known_hash = "#design"
    # From doc-redirect: "#design": "design/design/"
    target_path = f"/{LATEST_VERSION}/design/design/" 
    
    # We can't verify hash client side logic with this script easily, but we verify page existence.
    l_res = verify_single_redirect(source_legacy, target_path, "Legacy documentation.html link")
    
    if l_res["s_ok"]:
         print(f"[PASS] {source_legacy} exists.")
    else:
         print(f"[FAIL] {source_legacy} missing.")
         results.append(l_res) # Force failure if missing

    # Versioned Legacy .html
    print("Verifying Versioned documentation.html (Sample: First and Last version)")
    if versions:
        # Check first, last to sample
        sample_versions = [versions[0], versions[-1]]
        for v in sample_versions:
             url = urljoin(ROOT_URL, f"/{v}/documentation.html")
             status, _, _ = check_url(url)
             if status == 200:
                 print(f"[PASS] /{v}/documentation.html exists.")
             else:
                 print(f"[FAIL] /{v}/documentation.html : HTTP {status}")
                 results.append({"source": f"/{v}/documentation.html", "s_ok": False, "s_msg": f"HTTP {status}"})

    print("-" * 50)
    print("Verifying Streams .html Alias")
    # /documentation/streams/architecture.html -> /41/streams/architecture (via populating streams + alias)
    # The source is the alias path. 
    # Since verifying actual redirect chain is hard without browser, we verify the alias target eventually resolves.
    # But verify_single_redirect takes source and target.
    # Source: /documentation/streams/architecture.html
    # Target: /43/streams/architecture/ (Latest version is 4.3 now per user edit)
    # The content logic redirects path /documentation/streams/... to /{latest/version}/streams/...
    
    # Check one example
    s_html = "/documentation/streams/architecture.html"
    t_html = f"/{LATEST_VERSION}/streams/architecture/"
    
    # We anticipate:
    # 1. architecture.html -> architecture/ (Hugo Alias) -> 200 OK (with doc-redirect)
    # 2. architecture/ executes JS -> redirects to /{latest}/streams/architecture/
    # This script verifies static reachability.
    
    # Note: Hugo aliases are HTML files with meta refresh. verify_redirects check_url might just return 200 for the alias file itself.
    # That is sufficient to prove the alias FILE exists.
    
    a_res = verify_single_redirect(s_html, s_html, "Streams .html Alias Existence")
    if a_res["s_ok"]:
        print(f"[PASS] {s_html} alias exists.")
    else:
        print(f"[FAIL] {s_html} alias missing.")
        results.append(a_res)

    print("-" * 50)
    if not results:
        print("SUCCESS: All checked redirects passed verification.")
        sys.exit(0)
    else:
        print(f"FAILURE: {len(results)} checks failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
