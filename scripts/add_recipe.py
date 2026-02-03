#!/usr/bin/env python3
import os
import sys
import datetime
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.panel import Panel
from rich import print

console = Console()

DOCS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../docs"))
RECIPES_DIR = os.path.join(DOCS_DIR, "recipes")

def get_categories():
    """Scan the recipes directory for subfolders (categories)."""
    if not os.path.exists(RECIPES_DIR):
        os.makedirs(RECIPES_DIR)
    
    categories = [d for d in os.listdir(RECIPES_DIR) 
                  if os.path.isdir(os.path.join(RECIPES_DIR, d)) and not d.startswith('.')]
    categories.sort()
    return categories

def slugify(text):
    return "".join(c if c.isalnum() else "-" for c in text.lower()).strip("-")

def main():
    console.print(Panel.fit("👨‍🍳 [bold green]New Recipe Wizard[/bold green] 👩‍🍳", border_style="green"))

    # 1. Get Details
    title = Prompt.ask("[bold]Recipe Title[/bold]")
    
    # 2. Choose Category
    categories = get_categories()
    if not categories:
        console.print("[yellow]No categories found. Creating a new one.[/yellow]")
        category = Prompt.ask("[bold]New Category Name[/bold] (e.g. Dinner)")
    else:
        console.print("\n[bold]Select Category:[/bold]")
        for idx, cat in enumerate(categories, 1):
            console.print(f"  [cyan]{idx}. {cat}[/cyan]")
        console.print(f"  [cyan]{len(categories)+1}. [New Category][/cyan]")
        
        cat_idx = IntPrompt.ask("Choose #", choices=[str(i) for i in range(1, len(categories) + 2)])
        
        if cat_idx == len(categories) + 1:
            category = Prompt.ask("[bold]New Category Name[/bold]")
        else:
            category = categories[cat_idx - 1]

    # 3. Metadata
    prep_time = Prompt.ask("[bold]Prep time[/bold] (e.g. 15 mins)", default="15 mins")
    cook_time = Prompt.ask("[bold]Cook time[/bold] (e.g. 30 mins)", default="30 mins")
    servings = Prompt.ask("[bold]Servings[/bold]", default="4")

    # 4. Generate File
    slug = slugify(title)
    cat_slug = slugify(category)
    
    target_dir = os.path.join(RECIPES_DIR, cat_slug)
    os.makedirs(target_dir, exist_ok=True)
    
    filename = f"{slug}.md"
    filepath = os.path.join(target_dir, filename)

    if os.path.exists(filepath):
        console.print(f"[red]Error: {filename} already exists![/red]")
        sys.exit(1)

    template = f"""---
title: {title}
description: Delicious {title} recipe
---

# {title}

<div class="recipe-meta">
  <span class="meta-item">⏱️ **Prep:** {prep_time}</span>
  <span class="meta-item">🍳 **Cook:** {cook_time}</span>
  <span class="meta-item">🍽️ **Yield:** {servings}</span>
</div>

## Ingredients
- [ ] Item 1
- [ ] Item 2

## Instructions
1. Step one...
2. Step two...

---
*Tags: #{cat_slug}*
"""

    with open(filepath, "w") as f:
        f.write(template)

    console.print(f"\n✅ [bold green]Recipe Created![/bold green] {filepath}")
    
    # 5. Open in Editor
    # Try VS Code, then standard open
    try:
        if os.system(f"code '{filepath}'") != 0:
            os.system(f"open '{filepath}'")
    except:
        pass

if __name__ == "__main__":
    main()
