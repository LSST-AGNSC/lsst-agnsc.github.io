# LSST AGN Science Collaboration website

Static site for the LSST AGN SC, published with GitHub Pages at <https://lsst-agnsc.github.io>.
It keeps the look of the former Drupal site at agn.science.lsst.org, but every page is a plain
Markdown file: edit it on GitHub, commit, and the site rebuilds in about a minute.

## Editing a page

| Page | File |
|---|---|
| Home | `index.md` |
| Meetings | `meetings.md` |
| 2025 meeting | `meeting2025.md` |
| Projects (Project Proposal form) | `projects.md` |
| Documents | `documents.md` (list in the front matter, see below) |
| Talks | `talks.md` (same) |
| Members | `members.md` |
| Apply (Membership Application form) | `apply.md` |
| Contact | `contact.md` |
| Contact request pages | `project_join_request.md`, `publication_review.md`, `publication_dispute.md`, `general_inquiry.md` |
| Sidebar "Quick links" | `_includes/sidebar.md` |

Each file starts with a short header between `---` lines (the title), followed by Markdown.
A line break inside a paragraph is shown as a line break, so lists of names or programme
lines can be written one per line. Raw HTML is allowed if Markdown is not enough.

## Adding a document or talk

1. Upload the file to the collaboration's Google Drive folder and copy its share link
   (right-click > Share > Copy link; the folder is shared as "Anyone with the link").
2. In `_data/files.yml` add a line `"<file name>": "<Drive link>"`.
3. In `documents.md` or `talks.md` add an item under `items:`:

   ```yaml
   - title: Title shown on the page
     file: <file name>
   ```

Old links of the form `/sites/default/files/<file name>` keep working: each file name in
`_data/files.yml` gets a small page at that address that forwards to the Drive link
(`_legacy_files/`). For a brand-new file that step is optional.

## Adding a meeting page

Create `meeting2026.md` with a header like

```
---
title: "2026 meeting title"
---
```

and link it from `meetings.md` as `[this page](/meeting2026/)`. The address is the file name.

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
`_drive_upload/` (not in git) holds local copies of the old uploads, sorted for Drive.
`CONVERSION_PLAN.md` describes how the site was converted. The content was taken from the
original Drupal database dump (November 2026), so it reflects the site's final state.
