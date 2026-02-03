#!/usr/bin/env python3
import os

DOCS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../docs"))
RECIPES_DIR = os.path.join(DOCS_DIR, "recipes")

def get_title(filepath):
    """Extract title from frontmatter or first H1."""
    try:
        with open(filepath, "r") as f:
            lines = f.readlines()
            
        # Strategy 1: Frontmatter title
        in_frontmatter = False
        for line in lines:
            line = line.strip()
            if line == "---":
                if not in_frontmatter:
                    in_frontmatter = True
                else:
                    break # End of frontmatter
            if in_frontmatter and line.startswith("title:"):
                return line.replace("title:", "").strip().strip('"')

        # Strategy 2: First H1
        for line in lines:
            if line.startswith("# "):
                return line.replace("# ", "").strip()
                
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    
    # Strategy 3: Filename
    return os.path.basename(filepath).replace(".md", "").replace("-", " ").title()

def main():
    if not os.path.exists(RECIPES_DIR):
        print("No recipes directory found.")
        return

    categories = [d for d in os.listdir(RECIPES_DIR) 
                  if os.path.isdir(os.path.join(RECIPES_DIR, d)) and not d.startswith('.')]
    
    print(f"Found categories: {categories}")

    for cat in categories:
        cat_dir = os.path.join(RECIPES_DIR, cat)
        recipes = [f for f in os.listdir(cat_dir) if f.endswith(".md") and f != "index.md"]
        recipes.sort()
        
        # Generate Index Content
        cat_title = cat.title()
        content = [f"# 📂 {cat_title}", "", "Here are the recipes in this collection:", ""]

        if not recipes:
            content.append("*No recipes added yet!*")
        else:
            for recipe_file in recipes:
                title = get_title(os.path.join(cat_dir, recipe_file))
                link = recipe_file
                content.append(f"- [{title}]({link})")

        index_path = os.path.join(cat_dir, "index.md")
        with open(index_path, "w") as f:
            f.write("\n".join(content))
        
        print(f"✅ Generated index for {cat}: {len(recipes)} recipes.")

if __name__ == "__main__":
    main()
