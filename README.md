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

## Features
*   **Interactive Ingredients:** Check off items as you shop or cook.
*   **Dark/Light Mode:** Automatically syncs with your system preference.
*   **Search:** Instant search across all recipes.
