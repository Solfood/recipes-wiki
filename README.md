# recipes-wiki

Static page hosting favorite recipes. Built with [MkDocs](https://www.mkdocs.org/).

## Setup

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run locally:**
    ```bash
    mkdocs serve
    ```
    Open [http://localhost:8000](http://localhost:8000) in your browser.

3.  **Deploy:**
    The site is automatically deployed to GitHub Pages via GitHub Actions on push to `main`.
    To deploy manually:
    ```bash
    mkdocs gh-deploy
    ```

## Contributing (Adding Recipes)

The easiest way to add a new recipe is to use the generator script. This ensures the formatting is correct.

```bash
./new_recipe.sh "Recipe Name" category
```

**Example:**
```bash
./new_recipe.sh "Spicy Tacos" mexican
```
This will create `docs/recipes/mexican/spicy-tacos.md` pre-filled with the template.
