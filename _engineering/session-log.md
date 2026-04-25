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
