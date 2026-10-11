# Outreach data is not public website code

The repository remains public; changing its visibility was not authorised. From this edition, current client/contact lists, action logs, suppression fingerprints, drafts, dossiers, generated registers and campaign state are **workspace/private-Drive data**, not files published in Git.

- `.gitignore` excludes the paths listed below. Removing tracking does not delete the working files.
- The active data is in the workspace and backed up as **10 · Private outreach sources** in the same Drive folder as 00–09.
- A fresh clone must restore that private source bundle to the repository root before running outreach tools. Do not invent an empty suppression registry or start a replacement contact list: missing safety files intentionally fail closed.
- Use only a trusted bundle from the user's Drive; inspect archive paths and reject absolute paths, `..` segments and symlinks before extraction. Do not publish the archive or client-specific reports.
- The website build remains usable without client data. Python outreach dependencies: `python3 -m pip install --break-system-packages -r requirements-outreach.txt`.
- `python3 -m unittest discover -s tests -p 'test_*.py'` runs fixture tests; private-dataset checks are skipped if their trusted files have not been restored.

Private paths: `docs/PROSPECTS.md`, `sales/prospects-2026.csv`, `sales/prospects-2026.json`, `sales/OUTREACH-LOG.csv`, `sales/SENT-RECORD.csv`, `sales/SUPPRESSION-LIST.json`, `sales/CAMPAIGN-ACTIVITY.json`, `sales/EMAIL-REWRITE-BRIEFS.json`, `sales/EMAIL-REWRITES.json`, `sales/EMAIL-REWRITES.md`, `sales/email-drafts/`, `sales/pitches/`, `sales/SHOP-DOSSIERS.md`, `sales/drive-clients-pricing.csv`, `sales/OUTREACH-REGISTER*.pdf`, `sales/DRIVE-RESUME.md`.

**Limits:** older Git revisions, the main branch, earlier public copies, caches, Gmail/Drive trash and recipient copies are not erased by untracking these files. Owner-only Drive permissions and Git exclusion reduce disclosure; neither is a legal opinion or proof that all privacy obligations are met. Sending remains paused pending the documented legal, privacy, source, tax and payment checks.
