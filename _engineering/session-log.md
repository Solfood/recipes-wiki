# Session Log

Append-only continuity log.

---

### 2026-04-24 - Session 1

- Markers: `RW-DX-0001`
- Objective: Bootstrap the engineering scaffold onto the recipes-wiki repo.
- Work completed: Created CLAUDE.md, policies/project-policy.yaml, _engineering/work-index.md, _engineering/session-log.md, _engineering/decisions/DEC-0001.md. Added _engineering/experiments/ placeholder. Scaffold files placed under _engineering/ (not docs/) to avoid conflicts with MkDocs site content. This is a cross-cutting item across the Solfood GitHub Pages suite (SUITE-DX-0001).
- Verification: All placeholder values replaced; scaffold structure matches engineering-scaffold-template. Policy reflects actual tech stack (Python 3, MkDocs Material 9+). Risk tolerance set to low — static content site. `suite` block correctly references bluray and Willowbrook.
- Decisions made: DEC-0001 — adopt engineering scaffold for AI-assisted development. Low risk.
- Open issues/blockers: None.
- Next actions: Start next real work item — candidate improvements: category index generation script resilience, new recipe categories, search configuration enhancements.
- References: engineering-scaffold-template, SUITE-DX-0001

---

### 2026-04-25 - Session 2

- Markers: `RW-FIX-0001`, `RW-DX-0002`, `RW-DX-0003`, `RW-DX-0004`, `RW-ARCH-0001`, `RW-ARCH-0002`
- Objective: Session-opening improvement audit — surface and fix latent quality issues across content, tooling, and CI.
- Work completed:
  - **RW-FIX-0001**: Removed `** **` formatting artifacts from 4 recipe files (honey-orange-glazed-salmon, shrimp-salad, full-sour-pickles, lacto-fermented-red-onions). Artifact was a leftover `** ` token before field values in `!!! info` blocks, introduced by a previous bulk-migration script.
  - **RW-DX-0002 + RW-ARCH-0002**: Repurposed `.github/workflows/ci.yml` from a legacy `mkdocs gh-deploy --force` deployer into a read-only `build-check` workflow (`mkdocs build --strict`). Added `pull_request` trigger, removed dead `master` branch trigger, dropped `contents: write` permission, pinned Python to `"3.11"` to match `deploy.yml`.
  - **RW-DX-0003**: Replaced `os.system(f"code '{filepath}'"` shell injection in `scripts/add_recipe.py` with `subprocess.run(["code", filepath])`.
  - **RW-DX-0004**: Sorted categories list in `generate_category_indexes.py` for deterministic output; added trailing newline to generated index files.
  - **RW-ARCH-0001**: Uncommented `git-revision-date-localized` plugin in `mkdocs.yml`; added `fetch-depth: 0` to `deploy.yml` checkout so the plugin has full git history in CI.
- Verification: `mkdocs build --strict` passed locally with zero errors. Category indexes regenerated correctly (7 categories, correct recipe counts).
- Decisions made: None requiring a DEC file — all items low-risk, reversible, no non-obvious design choices.
- Open issues/blockers: None.
- Next actions: Add recipes to the poultry category (currently empty). Consider standardizing "TBD" texture-target fields as recipes are updated.
- References: Plan file `alright-let-s-look-for-tranquil-star.md`

---

### 2026-11-08 - Session 3

- Markers: `RW-DATA-0001`
- Objective: Add Guinness Beef Stew recipe; user cooks it with tri-tip, so document substitute cuts.
- Work completed: Added `docs/recipes/beef/guinness-beef-stew.md` (template format, metric) with a Cut Options table and tri-tip timing warning. Regenerated category indexes.
- Verification: `mkdocs build --strict` passed (Documentation built in 2.68 seconds, no warnings beyond git-revision timestamps on uncommitted indexes).
- Decisions made: None (low risk content addition).
- Open issues/blockers: None.
- Next actions: Poultry category still empty.

---

### 2026-11-10 - Session 4

- Markers: `RW-ARCH-0003`, `RW-DATA-0002`
- Objective: Replace the MkDocs site with Mealie (DEC-0002), importing every recipe without loss.
- Work completed:
  - **RW-DATA-0002**: `scripts/import_to_mealie.py` (stdlib only) parses the 10 recipes and creates/overwrites them in Mealie via its API. `--dry-run` prints the parsed JSON.
  - **RW-ARCH-0003**: DEC-0002 written. Homelab branch `mealie` swaps `recipes-web` for Mealie v3.30.0 on `:8082`.
- Verification:
  - Dry-run word coverage: every word of every source file appears in that recipe's parsed output, except field labels mapped to fields (Yield/Prep/Cook time) and the `:gluten_free:` emoji code (tag "Gluten-Free" kept).
  - Imported into a scratch Mealie v3.30.0 on the laptop (:9925): 10 recipes created; a second run overwrote them in place (still 10, same slugs). Read-back of guinness-beef-stew showed ingredient section titles, titled steps with the tri-tip callout as a blockquote, and the Cut Options table as a note.
  - `mkdocs build` not run: no `docs/` content changed.
- Decisions made: DEC-0002 (medium risk; threat model inside).
- Open issues/blockers: cutover needs the homelab PR merged by the owner.
- Next actions: stop `recipes-web`, merge the homelab PR, run the import against recipes.local:8082, change the default Mealie admin password, then mark RW-ARCH-0003 DONE and archive this repo (owner's call).
