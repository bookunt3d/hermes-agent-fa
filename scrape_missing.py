#!/usr/bin/env python3
"""Scrape ALL missing pages from Hermes Agent docs."""
import os
import re
import json
import subprocess
from pathlib import Path
from bs4 import BeautifulSoup

BASE_URL = "https://hermes-agent.nousresearch.com"
OUTPUT_DIR = Path("scraped_v2")
OUTPUT_DIR.mkdir(exist_ok=True)

# Read missing pages
missing = Path("/tmp/missing_pages.txt").read_text().strip().split("\n")
print(f"Scraping {len(missing)} missing pages...")

def fetch_page(path):
    url = f"{BASE_URL}{path}"
    result = subprocess.run(
        ["curl", "-s", "-L", "--max-time", "30", url],
        capture_output=True, text=True
    )
    return result.stdout

def extract_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    article = soup.find('article') or soup.find('main') or soup
    title = ""
    h1 = article.find('h1')
    if h1:
        title = h1.get_text(strip=True)
    
    lines = []
    for el in article.find_all(['h1','h2','h3','h4','h5','h6','p','pre','code','ul','ol','li','table','tr','td','th','blockquote']):
        tag = el.name
        if tag in ['h1','h2','h3','h4','h5','h6']:
            lvl = int(tag[1])
            txt = re.sub(r'\s*#$', '', el.get_text(strip=True))
            lines.append(f"\n{'#'*lvl} {txt}\n")
        elif tag == 'p':
            txt = el.get_text(strip=True)
            if txt:
                lines.append(f"\n{txt}\n")
        elif tag == 'pre':
            code = el.get_text()
            lines.append(f"\n```\n{code}\n```\n")
        elif tag == 'code' and el.parent and el.parent.name != 'pre':
            lines.append(f"`{el.get_text()}`")
        elif tag == 'table':
            rows = el.find_all('tr')
            for i, row in enumerate(rows):
                cells = [td.get_text(strip=True) for td in row.find_all(['td','th'])]
                lines.append("| " + " | ".join(cells) + " |")
                if i == 0:
                    lines.append("| " + " | ".join(["---"]*len(cells)) + " |")
            lines.append("")
        elif tag == 'ul':
            for li in el.find_all('li', recursive=False):
                lines.append(f"- {li.get_text(strip=True)}")
            lines.append("")
        elif tag == 'ol':
            for i, li in enumerate(el.find_all('li', recursive=False), 1):
                lines.append(f"{i}. {li.get_text(strip=True)}")
            lines.append("")
        elif tag == 'blockquote':
            lines.append(f"\n> {el.get_text(strip=True)}\n")
    
    result = '\n'.join(lines)
    result = re.sub(r'\n{3,}', '\n\n', result)
    return title, result.strip()

# Scrape in batches
batch_size = 10
for i in range(0, len(missing), batch_size):
    batch = missing[i:i+batch_size]
    for path in batch:
        slug = path.replace('/docs/', '').replace('/', '_')
        out_file = OUTPUT_DIR / f"{slug}.md"
        if out_file.exists() and out_file.stat().st_size > 100:
            print(f"  SKIP: {slug}")
            continue
        
        print(f"  [{i+1}/{len(missing)}] {path}...")
        html = fetch_page(path)
        if not html:
            print(f"    EMPTY!")
            continue
        
        title, content = extract_content(html)
        out_file.write_text(content, encoding='utf-8')
        print(f"    -> {out_file.name} ({len(content)} chars, title: {title})")

print(f"\nDone! Files in {OUTPUT_DIR}/")
