#!/usr/bin/env python3
"""One-shot import of the recipes-wiki Markdown recipes into Mealie (RW-DATA-0002).

    python3 scripts/import_to_mealie.py --dry-run            # print parsed JSON, touch nothing
    MEALIE_URL=http://recipes.local:8082 MEALIE_USER=... MEALIE_PASSWORD=... \
        python3 scripts/import_to_mealie.py                  # create/overwrite in Mealie

Mapping (MkDocs Markdown -> Mealie):
  # H1                          -> name
  first italic/plain paragraph  -> description
  !!! info "Recipe Details"     -> recipeYield / prepTime / cookTime; other lines -> "Details" note
  ## Ingredients  ### X / **X:** -> ingredient section titles; list items -> ingredient notes
  ## Method       ### N. X       -> one step titled X
                  ### X (other)  -> its numbered items become steps, first titled X
                  numbered list  -> one step per item
  ### Notes/Tips/Calculating... -> recipe notes
  ## H2 after Method w/ list     -> more steps (e.g. "Assemble & Bake")
  other ## sections, admonitions -> recipe notes (Markdown, tables kept)
  folder                        -> category;  *Tags: #a, #b*  -> tags
Re-running overwrites recipes with the same slug, so it is safe to repeat.
Standard library only.
"""
import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "docs" / "recipes"
NOTE_HEADING = re.compile(r"note|tip|calculat|troubleshoot", re.I)
ADMONITION = re.compile(r'^(!!!|\?\?\?\+?)\s+(\w+)(?:\s+"([^"]*)")?\s*$')
NUMBERED = re.compile(r"^\d+\.\s+")
STEP_HEADING = re.compile(r"^(?:step\s+)?\d+[.:]\s*(.*)$", re.I)


def convert_admonitions(lines):
    """Turn indented MkDocs admonitions into ('admonition', title, body) blocks."""
    out, i = [], 0
    while i < len(lines):
        m = ADMONITION.match(lines[i])
        if not m:
            out.append(lines[i])
            i += 1
            continue
        title = m.group(3) or m.group(2).capitalize()
        body, i = [], i + 1
        while i < len(lines) and (lines[i].startswith("    ") or not lines[i].strip()):
            body.append(lines[i][4:] if lines[i].startswith("    ") else "")
            i += 1
        out.append(("admonition", title, "\n".join(body).strip()))
    return out


def as_markdown(items):
    """Render a mix of plain lines and admonition blocks as Markdown text."""
    parts = []
    for it in items:
        if isinstance(it, tuple):
            quoted = "\n".join("> " + l if l else ">" for l in it[2].splitlines())
            parts.append(f"> **{it[1]}**\n>\n{quoted}")
        else:
            parts.append(it)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(parts)).strip()


def plain(text):
    """Ingredient lines are shown as plain text in Mealie: drop emphasis and links."""
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = text.replace("**", "")
    text = re.sub(r"(?<![\w*])\*([^*]+)\*(?![\w*])", r"\1", text)
    return text.strip()


def split_numbered(lines):
    """Split lines into (preamble, [item, ...]) on top-level '1. ' items."""
    pre, items = [], []
    for l in lines:
        if isinstance(l, str) and NUMBERED.match(l):
            items.append([NUMBERED.sub("", l, count=1)])
        elif items:
            items[-1].append(l[4:] if isinstance(l, str) and l.startswith("    ") else l)
        else:
            pre.append(l)
    return pre, items


def split_on(lines, prefix):
    """Split lines into [(heading or None, body_lines)] on headings starting with prefix."""
    sections = [[None, []]]
    for l in lines:
        if isinstance(l, str) and l.startswith(prefix) and not l.startswith(prefix + "#"):
            sections.append([l[len(prefix):].strip(), []])
        else:
            sections[-1][1].append(l)
    return [(h, b) for h, b in sections if h is not None or any(
        (x.strip() if isinstance(x, str) else True) for x in b)]


def parse(path):
    raw = path.read_text(encoding="utf-8").splitlines()
    tags = []
    # Trailing "---" + "*Tags: #a, #b*" footer.
    for idx in range(len(raw) - 1, -1, -1):
        m = re.match(r"^\*Tags:\s*(.*)\*$", raw[idx].strip())
        if m:
            tags = [t.strip().lstrip("#") for t in m.group(1).split(",") if t.strip()]
            raw = raw[:idx]
            while raw and raw[-1].strip() in ("", "---"):
                raw.pop()
            break
    lines = convert_admonitions(raw)

    recipe = {"name": "", "description": "", "recipeYield": None, "prepTime": None,
              "cookTime": None, "recipeIngredient": [], "recipeInstructions": [],
              "notes": [], "tags": tags, "category": path.parent.name}
    details = []

    h2 = split_on(lines, "## ")
    head = h2[0][1] if h2 and h2[0][0] is None else []
    body_sections = h2[1:] if h2 and h2[0][0] is None else h2

    # Header: H1, description paragraph, Recipe Details admonition.
    for l in head:
        if isinstance(l, tuple):
            if l[1].lower() == "recipe details":
                for d in l[2].splitlines():
                    d = plain(d.lstrip("* ").strip())
                    m = re.match(r"([^:]+):\s*(.*)", d)
                    if not m:
                        continue
                    key, val = m.group(1).strip().lower(), m.group(2).strip()
                    if val.upper() == "TBD":
                        continue
                    if key == "yield":
                        recipe["recipeYield"] = val
                    elif key == "prep time":
                        recipe["prepTime"] = val
                    elif key == "cook time":
                        recipe["cookTime"] = val
                    elif key == "tags":  # ":pizza: Pizza, :bacon: Bacon"
                        recipe["tags"] += [re.sub(r":\w+:", "", t).strip() for t in val.split(",")]
                    else:
                        details.append(f"- **{m.group(1).strip()}:** {val}")
            else:
                recipe["notes"].append({"title": l[1], "text": l[2]})
        elif l.startswith("# "):
            recipe["name"] = l[2:].strip()
        elif l.strip():  # subtitle and any intro paragraphs
            d = l.strip()
            if d.startswith("*") and d.endswith("*"):
                d = d.strip("*").strip()
                if d.startswith("(") and d.endswith(")"):
                    d = d[1:-1]
            recipe["description"] = (recipe["description"] + "\n\n" + d).strip()
    if details:
        recipe["notes"].insert(0, {"title": "Details", "text": "\n".join(details)})

    seen_method = False
    for heading, body in body_sections:
        name = heading.lower()
        if name == "ingredients":
            title, loose = None, []
            for l in body:
                if isinstance(l, tuple):
                    recipe["notes"].append({"title": l[1], "text": l[2]})
                    continue
                s = l.strip()
                if s.startswith("### "):
                    title = s[4:].strip()
                elif re.fullmatch(r"\*\*[^*]+\*\*:?", s):
                    title = s.strip("*: ").rstrip(":")
                elif re.match(r"^[-*]\s+(\[ \]\s+)?", s):
                    note = plain(re.sub(r"^[-*]\s+(\[ \]\s+)?", "", s))
                    recipe["recipeIngredient"].append({"note": note, "title": title})
                    title = None
                elif s.startswith(">"):
                    loose.append(s.lstrip("> ").strip())
                elif s:
                    loose.append(s)
            if loose:
                recipe["notes"].append({"title": "Ingredient notes", "text": "\n\n".join(loose)})
        elif name == "method" or (seen_method and any(
                isinstance(l, str) and NUMBERED.match(l) for l in body)):
            if name != "method":  # e.g. "Assemble & Bake": more steps, titled
                body = [f"### {heading}"] + body
            seen_method = True
            # Callouts closing the section (Troubleshooting, Storage, Final Profile...)
            # are about the whole recipe, not the last step: make them notes.
            body = [l for l in body if not (isinstance(l, str) and l.strip() == "---")]
            trailing = []
            while body and (isinstance(body[-1], tuple) or not body[-1].strip()):
                l = body.pop()
                if isinstance(l, tuple):
                    trailing.insert(0, {"title": l[1], "text": l[2]})
            recipe["notes"] += trailing
            for sub, sbody in split_on(body, "### "):
                if sub and NOTE_HEADING.search(sub):
                    recipe["notes"].append({"title": sub.rstrip(":"), "text": as_markdown(sbody)})
                    continue
                m = STEP_HEADING.match(sub or "")
                if m:
                    recipe["recipeInstructions"].append(
                        {"title": m.group(1).strip(), "text": as_markdown(sbody)})
                    continue
                pre, items = split_numbered(sbody)
                pre_text = as_markdown(pre)
                if not items:
                    if pre_text:
                        recipe["recipeInstructions"].append({"title": sub or "", "text": pre_text})
                    continue
                for n, item in enumerate(items):
                    text = as_markdown(item)
                    if n == 0 and pre_text:
                        text = pre_text + "\n\n" + text
                    recipe["recipeInstructions"].append({"title": sub or "" if n == 0 else "", "text": text})
        else:
            recipe["notes"].append({"title": heading, "text": as_markdown(body)})
    return recipe


class Mealie:
    def __init__(self, url, user, password):
        self.url = url.rstrip("/")
        form = urllib.parse.urlencode({"username": user, "password": password}).encode()
        self.token = json.load(urllib.request.urlopen(self.url + "/api/auth/token", form))["access_token"]

    def call(self, method, path, body=None):
        req = urllib.request.Request(self.url + path, method=method,
                                     data=None if body is None else json.dumps(body).encode(),
                                     headers={"Authorization": f"Bearer {self.token}",
                                              "Content-Type": "application/json"})
        with urllib.request.urlopen(req) as r:
            data = r.read()
            return json.loads(data) if data else None

    def organizer(self, kind, name):
        q = urllib.parse.urlencode({"search": name, "perPage": 100})
        for it in self.call("GET", f"/api/organizers/{kind}?{q}")["items"]:
            if it["name"].lower() == name.lower():
                return it
        return self.call("POST", f"/api/organizers/{kind}", {"name": name})

    def upsert(self, r):
        slug = self.call("POST", "/api/recipes", {"name": r["name"]})
        full = self.call("GET", f"/api/recipes/{slug}")
        full.update({
            "description": r["description"], "recipeYield": r["recipeYield"],
            "prepTime": r["prepTime"], "cookTime": r["cookTime"],
            "recipeIngredient": [{"note": i["note"], "display": i["note"], "title": i["title"],
                                  "quantity": 0, "unit": None, "food": None} for i in r["recipeIngredient"]],
            "recipeInstructions": [{"title": s["title"], "summary": "", "text": s["text"],
                                    "ingredientReferences": []} for s in r["recipeInstructions"]],
            "notes": r["notes"],
            "recipeCategory": [self.organizer("categories", r["category"].capitalize())],
            "tags": [self.organizer("tags", t) for t in r["tags"]],
        })
        self.call("PUT", f"/api/recipes/{slug}", full)
        return slug

    def delete_by_name(self, name):
        q = urllib.parse.urlencode({"search": name, "perPage": 100})
        for it in self.call("GET", f"/api/recipes?{q}")["items"]:
            if it["name"] == name:
                self.call("DELETE", f"/api/recipes/{it['slug']}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="print parsed recipes as JSON and exit")
    args = ap.parse_args()
    recipes = [parse(p) for p in sorted(ROOT.glob("*/*.md")) if p.name != "index.md"]
    if args.dry_run:
        json.dump(recipes, sys.stdout, indent=2, ensure_ascii=False)
        print()
        return
    m = Mealie(os.environ["MEALIE_URL"], os.environ["MEALIE_USER"], os.environ["MEALIE_PASSWORD"])
    for r in recipes:
        m.delete_by_name(r["name"])  # overwrite: same name -> fresh recipe, same slug
        slug = m.upsert(r)
        print(f"{slug}: {len(r['recipeIngredient'])} ingredients, "
              f"{len(r['recipeInstructions'])} steps, {len(r['notes'])} notes")


if __name__ == "__main__":
    main()
