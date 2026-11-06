# LSST AGN Science Collaboration website

Static site for the LSST AGN SC, published with GitHub Pages at <https://lsst-agnsc.github.io>.
It keeps the look of the former Drupal site at agn.science.lsst.org, but every page is a plain
Markdown file: edit it on GitHub, commit, and the site rebuilds in about a minute.

## Editing a page

| Page | File |
|---|---|
| Home | `index.md` |
| Meetings (list of all meetings) | `meetings/index.md` |
| One meeting (2025, 2022, 2020, 2018, 2017) | `meetings/<year>.md` |
| Previous Talks (linked from Meetings) | `meetings/talks.md` (list in the front matter, see below) |
| Projects (Project Proposal form) | `projects.md` |
| Documents | `documents.md` (list in the front matter, see below) |
| Members | `members.md` |
| Apply (Membership Application form) | `apply.md` |
| Contact | `contact.md` |
| Contact request pages | `project_join_request.md`, `publication_review.md`, `publication_dispute.md`, `general_inquiry.md` |
| Sidebar "Quick links" | `_includes/sidebar.md` |

Each file starts with a short header between `---` lines (the title), followed by Markdown.
A line break inside a paragraph is shown as a line break, so lists of names or programme
lines can be written one per line. Raw HTML is allowed if Markdown is not enough.

## Google Drive

The files live in two shared Drive folders, `documents` and `talks`. The only links to paste are
the two folder links, in `_data/drive.yml` (share each folder as "Anyone with the link"). Every
file name on the site then links to its folder. Direct per-file links are filled into
`_data/files.yml` automatically by the "Update Drive links" GitHub Action (Actions tab > Update
Drive links > Run workflow; it also runs weekly and whenever `drive.yml` changes). Locally the
same can be done with `python3 tools/drive_links.py`.

## Adding a document or talk

1. Upload the file to the `documents` or `talks` Drive folder.
2. In `_data/files.yml` add a line `"<file name>": ""` under the matching folder section
   (the Action fills in the link).
3. In `documents.md` or `meetings/talks.md` add an item under `items:`:

   ```yaml
   - title: Title shown on the page
     file: <file name>
   ```

Old links of the form `/sites/default/files/<file name>` keep working: each file in
`_legacy_files/` is a small page at that address that forwards to the file's Drive link, or to
its folder until the link is known. For a brand-new file that step is optional.

## Adding a meeting page

Every meeting with its own page lives in the `meetings/` folder, one file per year. Create
`meetings/2026.md` with a header like

```
---
title: "2026 meeting title"
---
```

and add an entry for it in `meetings/index.md` that links to `[this link](/meetings/2026/)`. The
address is the folder plus the file name. Meetings whose details are on an external site (2023,
2024, 2026) only need an entry in `meetings/index.md`.

## Menu and contact forms

- Menu entries: `_data/navigation.yml`.
- Online forms: six pages carry a form (`apply.md`, `projects.md`, `project_join_request.md`,
  `publication_review.md`, `publication_dispute.md`, `general_inquiry.md`), listed in
  `_data/forms.yml`. Paste a Google Form link into `url` there and the page embeds the form; until
  then it shows a notice. Each page ends with "What the form asks", the field list of the original
  web form, to mirror when building the Google Form. Entries with `contact: true` appear in the
  Contact dropdown.

## Previewing locally (optional)

Needs Ruby. Then:

```
bundle install
bundle exec jekyll serve
```

and open <http://localhost:4000>.

## Layout and style

`_layouts/default.html` holds the header, menu, sidebar and footer. `assets/css/site.css` is the
original theme CSS and should not need editing; put changes in `assets/css/extra.css`.
`_drive_upload/` (not in git) holds local copies of the old uploads in two folders, `documents/` and
`talks/`, matching the two Google Drive folders.
`CONVERSION_PLAN.md` describes how the site was converted. The content was taken from the
original Drupal database dump (November 2026), so it reflects the site's final state.
