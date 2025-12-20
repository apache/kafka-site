import json
import argparse
import sys
import threading
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse, urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def extract_urls(data, urls_set):
    """
    Recursively traverse the JSON structure to find 'url' fields.
    Structure seems to be: list of objects, which have 'subtable' (list of objects) and 'url'.
    """
    if isinstance(data, list):
        for item in data:
            extract_urls(item, urls_set)
    elif isinstance(data, dict):
        if 'url' in data and data['url']:
            urls_set.add(data['url'])
        
        # Check for nested subtables or other structures
        for key, value in data.items():
            if isinstance(value, (list, dict)):
                extract_urls(value, urls_set)

def normalize_url(original_url, target_base):
    """
    Replaces the scheme and netloc of the original URL with the target base.
    """
    try:
        parsed_original = urlparse(original_url)
        # We only care about the path, query, fragment
        # Construct new url relative to target_base
        # urljoin handles base ending with / or not fairly well, but let's be explicit
        # If original path is absolute, it joins correctly.
        
        # However, we want to mirror the path exactly.
        # original: https://kafka.apache.org/documentation/
        # path: /documentation/
        # target: http://localhost:1313
        # result: http://localhost:1313/documentation/
        
        relative_path = parsed_original.path
        if parsed_original.query:
            relative_path += '?' + parsed_original.query
        if parsed_original.fragment:
            relative_path += '#' + parsed_original.fragment
            
        # Ensure target_base doesn't double slash if path starts with /
        if target_base.endswith('/') and relative_path.startswith('/'):
            final_url = target_base + relative_path[1:]
        elif not target_base.endswith('/') and not relative_path.startswith('/'):
             final_url = target_base + '/' + relative_path
        else:
            final_url = target_base + relative_path
            
        return final_url
    except Exception as e:
        print(f"Error normalizing URL {original_url}: {e}")
        return None

def check_url(target_url, timeout=5):
    """
    Checks if the URL is accessible.
    Returns (url, status, error_message)
    """
    try:
        # User agent might be needed if server blocks python-urllib, but for localhost likely fine.
        # Adding one just in case.
        req = Request(
            target_url, 
            headers={'User-Agent': 'Mozilla/5.0 (compatible; OldUrlChecker/1.0)'}
        )
        with urlopen(req, timeout=timeout) as response:
            return target_url, response.getcode(), None
    except HTTPError as e:
        return target_url, e.code, str(e)
    except URLError as e:
        return target_url, 0, str(e.reason)
    except Exception as e:
        return target_url, 0, str(e)

def main():
    parser = argparse.ArgumentParser(description="Verify old URLs against a new target server.")
    parser.add_argument('json_file', help="Path to the old paths JSON file.")
    parser.add_argument('--target', default="http://localhost:1313", help="Target base URL (default: http://localhost:1313)")
    parser.add_argument('--workers', type=int, default=10, help="Number of concurrent threads (default: 10)")
    
    args = parser.parse_args()
    
    print(f"Reading {args.json_file}...")
    try:
        with open(args.json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        sys.exit(1)
        
    urls_set = set()
    print("Extracting URLs...")
    extract_urls(data, urls_set)
    print(f"Found {len(urls_set)} unique URLs.")
    
    if not urls_set:
        print("No URLs found. Exiting.")
        sys.exit(0)
        
    print(f"Verifying against target: {args.target}")
    
    results = []
    failed_count = 0
    
    # Prepare list of URLs to check
    urls_to_check = []
    for old_url in urls_set:
        new_url = normalize_url(old_url, args.target)
        if new_url:
            urls_to_check.append((old_url, new_url))
            
    total = len(urls_to_check)
    print(f"Starting verification of {total} URLs with {args.workers} workers...")
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        # Submit all tasks
        future_to_url = {executor.submit(check_url, new_url): (old_url, new_url) for old_url, new_url in urls_to_check}
        
        completed = 0
        for future in as_completed(future_to_url):
            old_url, new_url = future_to_url[future]
            completed += 1
            
            # Simple progress meter
            if completed % 50 == 0:
                print(f"Progress: {completed}/{total} ({(completed/total)*100:.1f}%)")
                
            try:
                checked_url, status, error = future.result()
                if status == 200:
                    # Pass
                    pass
                else:
                    failed_count += 1
                    print(f"[FAIL] {status} {new_url} (Orig: {old_url}) Error: {error}")
                    results.append({
                        "original": old_url,
                        "target": new_url,
                        "status": status,
                        "error": error
                    })
            except Exception as e:
                 failed_count += 1
                 print(f"[ERROR] Exception checking {new_url}: {e}")

    duration = time.time() - start_time
    print("-" * 50)
    print(f"Verification complete in {duration:.2f} seconds.")
    print(f"Total checked: {total}")
    print(f"Passed: {total - failed_count}")
    print(f"Failed: {failed_count}")
    
    if failed_count > 0:
        print(f"\nExample Failures (First 5):")
        for fail in results[:5]:
            print(f"  {fail['status']} - {fail['target']} : {fail['error']}")
        sys.exit(1)
    else:
        print("All URLs verified successfully!")
        sys.exit(0)

if __name__ == "__main__":
    main()
