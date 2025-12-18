import re
import sys
import argparse
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin

REDIRECT_FILE = '../layouts/shortcodes/doc-redirect.html'
BASE_URL = 'http://localhost:1313/41/'

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

def check_url(target_path):
    """
    Checks if the target path exists on the server using urllib.
    Returns (status_code, anchor_found, error_msg)
    """
    path_part = target_path
    anchor = None
    if '#' in target_path:
        path_part, anchor = target_path.split('#', 1)

    url = urljoin(BASE_URL, path_part)
    
    try:
        with urlopen(url, timeout=2) as response:
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

def main():
    print(f"Parsing {REDIRECT_FILE}...")
    redirects = parse_redirects(REDIRECT_FILE)
    print(f"Found {len(redirects)} redirects.")
    
    print(f"Checking against {BASE_URL}...")
    
    success_count = 0
    fail_count = 0
    warning_count = 0 

    for key, target in redirects.items():
        status, anchor_ok, msg = check_url(target)
        
        if status == 200:
            if anchor_ok:
                print(f"[PASS] {key} -> {target}")
                success_count += 1
            else:
                print(f"[WARN] {key} -> {target} (Page OK, {msg})")
                warning_count += 1
        else:
            print(f"[FAIL] {key} -> {target} ({msg})")
            fail_count += 1
            
    print("-" * 30)
    print(f"Summary: PASS={success_count}, WARN={warning_count}, FAIL={fail_count}")
    
    if fail_count > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
