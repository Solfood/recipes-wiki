#!/usr/bin/env python3
import os
import re
import glob

# Constants
DOCS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../docs/recipes"))

def parse_frontmatter(content):
    """
    Extracts YAML frontmatter and the rest of the content.
    Returns (metadata_dict, remaining_content)
    """
    frontmatter_regex = r"^---\s*\n(.*?)\n---\s*\n"
    match = re.match(frontmatter_regex, content, re.DOTALL)
    
    metadata = {}
    rest = content
    
    if match:
        yaml_content = match.group(1)
        rest = content[match.end():]
        
        for line in yaml_content.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip()
                
    return metadata, rest

def extract_meta_div(content):
    """
    Extracts metadata from the old <div class="recipe-meta"> format.
    Returns (meta_dict, remaining_content_without_div)
    """
    div_regex = r'<div class="recipe-meta">\s*(.*?)\s*</div>'
    match = re.search(div_regex, content, re.DOTALL)
    
    meta = {}
    if match:
        div_content = match.group(1)
        # Extract individual items
        # <span class="meta-item">⏱️ **Prep:** 15 mins</span>
        items = re.findall(r'<span class="meta-item">.*?(\*\*.*?:)\s*(.*?)</span>', div_content)
        for label, value in items:
            key = label.replace('*', '').replace(':', '').strip()
            meta[key] = value.strip()
            
        # Remove the div from content
        content = content.replace(match.group(0), '')
        
    return meta, content

def convert_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # 1. Parse Frontmatter
    fm_meta, content = parse_frontmatter(content)
    
    # 2. Extract HTML Meta if exists
    html_meta, content = extract_meta_div(content)
    
    # Combine metadata
    title = fm_meta.get('title', 'Untitled')
    description = fm_meta.get('description', '')
    
    # Defaults if not found in HTML meta
    prep = html_meta.get('Prep', 'TBD')
    cook = html_meta.get('Cook', 'TBD')
    yield_amount = html_meta.get('Yield', 'TBD')

    # 3. Clean up content (remove H1 if it duplicates title)
    # Remove H1 # Title regex
    content = re.sub(r'^#\s+.*?\n', '', content, flags=re.MULTILINE)
    
    # 4. Rename Instructions to Method
    content = re.sub(r'##\s+Instructions', '## Method', content)

    # 5. Reconstruct
    
    # Header
    new_content = f"# {title}\n"
    if description:
        new_content += f"*{description}*\n\n"
    elif title:
         new_content += f"*{title}*\n\n"

    # Metadata Block
    new_content += '!!! info "Recipe Details"\n'
    new_content += f"    *   **Yield:** {yield_amount}\n"
    new_content += f"    *   **Prep time:** {prep}\n"
    new_content += f"    *   **Texture target:** TBD\n" # Added placeholder to match tri-tip style if desired, or just stick to basics
    new_content += f"    *   **Cook time:** {cook}\n\n"
    
    # Content
    new_content += content.strip()
    new_content += "\n"

    return new_content

def main():
    # DOCS_DIR is relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    docs_dir = os.path.abspath(os.path.join(script_dir, "../docs/recipes"))
    
    print(f"Scanning {docs_dir}...")
    files = glob.glob(f"{docs_dir}/**/*.md", recursive=True)
    
    modified_count = 0
    for filepath in files:
        if 'tri-tip-chili.md' in filepath or os.path.basename(filepath) == 'index.md':
            continue
            
        try:
            with open(filepath, 'r') as f:
                content = f.read()
                
            if '!!! info "Recipe Details"' in content:
                print(f"Skipping {os.path.basename(filepath)} (already updated)")
                continue

            print(f"Updating {os.path.basename(filepath)}...")
            new_content = convert_file(filepath)
            
            with open(filepath, 'w') as f:
                f.write(new_content)
            modified_count += 1
        except Exception as e:
            print(f"Failed to update {filepath}: {e}")

    print(f"\nDone! Updated {modified_count} files.")

if __name__ == "__main__":
    main()
