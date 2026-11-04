# Plan: convert the LSST AGN SC Drupal site to a static, Markdown-edited GitHub Pages site

Written 2026-11-04, revised the same day after two decisions from Weixiang:

- **Content is edited as Markdown.** Each page (Home, Meetings, Members, Apply, ...)
  is one `.md` file. Nobody touches HTML to update the site.
- **Documents and talks live in Google Drive.** The website only links to them.
  The 444 MB of PDFs in this repo are not published by the new site.

Goal unchanged: keep the exact look and layout of agn.science.lsst.org, keep
every static page, drop everything that needed PHP.

## Status (2026-11-04)

Built on branch `static-site`, verified locally with Jekyll 3.10 (the version GitHub Pages runs).
Done: all nine pages as Markdown, Documents/Talks lists with description and date (Documents also lists the newer files from the server dump: 2025 publication policy v3, OpenProject guide, earlier charter revisions), Members
restored from the November 2024 archive, sidebar quick links, Contact placeholders, old
`?q=` addresses redirected, 52 legacy file stubs under `/sites/default/files/`, theme CSS
repaired (two syntax slips in the original broke its phone-size rules), mobile menu script.
Not done: Drive links (`_data/files.yml` is all empty strings), Google Form links
(`_data/forms.yml`), merge to `main`, enabling GitHub Pages. Local copies of the uploads are in
`_drive_upload/` (git-ignored), sorted into `documents/`, `talks/`, `meetings/`, `archive/`.

## 1. What we are starting from

- The live site (agn.science.lsst.org) is a **Drupal 7** site using the LSST
  `impact_theme`. As of 2026-11-04 it does not respond (connection timeout).
- This repo (branch `old`) is **not** the site. It is a dump of Drupal's
  `sites/default/files/` directory: aggregated CSS, uploaded PDFs/images,
  image-style derivatives, and leftovers from older themes (`mayo/`, `color/`).
  It contains **no page HTML**.
- The rendered pages survive in the **Wayback Machine**. Homepage snapshot:
  `http://web.archive.org/web/20261004190821/https://agn.science.lsst.org/`
  (append `id_` after the timestamp to get the raw, un-rewritten HTML).

## 2. Page inventory

| Page | Source | New file | Notes |
|---|---|---|---|
| Home | archived 2026-10 | `index.md` | plus the `?q=` redirect script |
| Meetings | archived | `meetings.md` | long text; converted from HTML to Markdown with pandoc, then tidied |
| 2025 meeting | archived 2025-08 | `meeting2025.md` | future meetings: add one `.md` each |
| Projects | archived | `projects.md` | one sentence |
| Documents | archived (Drupal View, 10 files) | `documents.md` | list of Drive links, see section 4 |
| Talks | archived (Drupal View, ~10 talks + LSST2018 session files) | `talks.md` | list of Drive links |
| Members | 404 on the live site | `members.md` | **comes back** as a page Weixiang edits; menu entry restored |
| Apply | archived | `apply.md` | static text |
| Contact | archived | `contact.md` | form links replaced, see section 5 |
| Contact > four webforms | not archived, Drupal webforms | none | dynamic; replaced on the Contact page |
| `/user`, login block, CAPTCHA, Admin Login | n/a | none | removed |

Menu: one YAML file, `_data/navigation.yml`. Adding a page is a one-line edit.

## 3. Layout to preserve

From the rendered HTML the skeleton is:

```
body.html.one-sidebar.sidebar-first
  #wrapper
    header#header        site logo, .global-profile icon links, nav#navigation > #main-menu (Contact has a dropdown)
    #main
      #primary > section#content > #breadcrumbs + #content-wrap (h1.page-title + body)
      aside#sidebar       only block was "User login"
    footer#footer-bottom  #footer-area, #bottom (.copyright, .credit)
```

This skeleton becomes `_layouts/default.html`. The Markdown body of each page is
dropped into `#content-wrap` exactly where Drupal put the node body, so the
theme CSS styles the generated `h2`, `p`, `ul`, `table` the same way.

Styling comes from five aggregated CSS files, all present in `css/`:

| File | Content |
|---|---|
| `css_xE-rWrJf…` | Drupal core system styles |
| `css_TsVRTbLF…` | comment / field styles |
| `css_wEkBe38b…` | ctools + lightbox2 |
| `css_y-HWnTHt…` | **impact_theme** (the actual look, 30 KB) |
| `css_Kh9ycgwj…` | css_injector tweaks (line-height, bold legends) |

They are concatenated into `assets/css/site.css` with `url()` paths rewritten.

Assets the CSS needs that are **not** in this repo:

- `sites/all/themes/impact_theme/images/*` (menu_bg, stripes, crosslines-pattern,
  public/project/science icons, select-arrow, search-button, social icons, …).
  Eight are confirmed archived on Wayback; fetch all 17 and see what lands.
- `modules/file/icons/application-pdf.png` and `x-office-presentation.png`
  (Drupal core, GPL): fetch from Wayback or the Drupal 7 source. Used for the
  file icons on the Documents and Talks lists.
- Theme JS: `slide.js` archived; `main-menu.js`, `responsive_menus_simple.js`,
  `jquery.cycle`, favicon **not** archived. Only the Contact dropdown and the
  mobile menu need JS; replace with a few lines of vanilla JS or pure CSS.
- `/misc/*.png` and lightbox images are admin-only; those rules are deleted.

## 4. Documents and Talks as Google Drive links

Old look: each entry was an article block with a title, a PDF icon and the file
name as a link. To keep that look without HTML editing, each list page is a
Markdown file whose **front matter holds the list** and a `list` layout renders
the old markup:

```markdown
---
title: Documents
layout: list
items:
  - title: The LSST AGN Science Collaboration Charter (Current)
    file: AGN_SC_Charter_Apr2024.pdf
    url: https://drive.google.com/file/d/<id>/view
  - title: LSST AGN Science Collaboration Roadmap (Current)
    file: LSST_AGN_SC_Roadmap_260722.pdf
    url: https://drive.google.com/file/d/<id>/view
---
Optional intro text in Markdown goes here.
```

Adding a talk is three lines. The icon is picked from the file extension.
Fallback if even that is too much structure: a plain Markdown bullet list of
links, at the cost of the icons and article blocks.

Drive setup needed from Weixiang:

1. Upload the files (list below) to a Drive folder, one subfolder each for
   `documents` and `talks`.
2. Share the folder as "Anyone with the link, Viewer". Per-file links then work
   for visitors who are not signed in.
3. Send the folder link. I collect the per-file links and fill in the YAML.
   To replace a file later, use Drive's "Manage versions" so the link stays the same.

**File names stay exactly as they are now.** Every list entry keeps `file:`
equal to the old upload name, and `url:` is the Drive link for that same name.
In effect the old `/sites/default/files/<name>` becomes
`https://drive.google.com/file/d/<id>/view` for `<name>`, nothing else changes.
Until the Drive links arrive, `url:` stays empty and the list renders the file
name without a link, so the pages can be built and checked now.

Files referenced by the archived pages (all present in this repo):

- Documents: `AGN_SC_Charter_Apr2024.pdf`, `AGN_SC_Charter_Supplement_Apr2024_0.pdf`,
  `AGN_SC_Code_of_Conduct_May2020.pdf`, `AGN_SC_Publication_Policy_May2020.pdf`,
  `LSST_AGN_SC_Roadmap_260722.pdf`, `LSST_AGN_SC_Roadmap_v1p0.pdf`,
  `2023-01-17_scWelcome_1.pdf`, `2014-10-agn_roadmap.pptx`,
  `2013-09-11-lsstcam13-shemmer.pdf`, `2020-06-lsst-agn-sc-mim-plan01.txt`.
- Talks: `2019-06-Brandt-Lyon-LSST-01.pdf`, `Brandt-Santiago-LSST-02.pdf`,
  `Brandt-Cambridge-LSST-Fusion-01.pdf`, `Brandt-LSST-Brazil-01.pdf`,
  `Brandt-Athena-Madrid-01.pdf`, `Brandt-Lorentz.pdf`, `Photoz2_Peters.pdf`,
  `richards-2017-02.pdf`, the eight `LSST_AGN_SC_2017_*.pdf` and
  `Abstract_*.txt` pairs, the LSST2018 session files (`010-schindler`,
  `020-reed`, `030-anguita`, `040-bauer`, session photo, audio, `IMG_2086.JPG`).
- Thirteen files no page references (older charter versions, OpenProject guide,
  2025 publication policy v3, `pop.jpg`, `adFSD.jpg`, `issc-logo.png`, ...):
  upload them to Drive too, in an `archive` subfolder, and drop them from the repo.

Repo result: no PDFs in git. Only the logo and theme images stay.

## 5. Dynamic parts and their replacements

1. **Login block + CAPTCHA**: removed. The sidebar column is **kept** for now so
   the content width stays identical; it holds a static block written as a
   Markdown include (`_includes/sidebar.md`, quick links). Revisit after seeing it.
2. **Webforms** (join request, publication review/dispute, general inquiry):
   replaced by **Google Forms**. The form URLs are not ready yet, so
   `_data/forms.yml` holds one entry per request type with an empty `url:`.
   The Contact page lists a request type as a link only when its `url:` is
   filled in, and as plain text ("form coming soon") otherwise. Dropping in a
   Google Form link later is a one-line edit.
3. **Old `?q=` URLs**: a tiny script in `index.md` redirects `/?q=meetings` to
   `/meetings/` so links in old emails keep working.
4. **Old file URLs** (`/sites/default/files/X.pdf`): with files in Drive these
   cannot be preserved on the site itself. A `redirects` data file plus one
   generated page per old file name can forward to the Drive link; cheap to add,
   recommended for the charter and roadmap at least.

## 6. Target structure (branch `static-site`, merged to `main` when verified)

```
_config.yml                 site title, permalinks (/:title/), markdown settings
_data/navigation.yml        the menu
_layouts/default.html       header, menu, sidebar, footer (the Drupal skeleton)
_layouts/list.html          Documents/Talks renderer (front-matter items -> old markup)
_includes/sidebar.md        sidebar block (if kept)
index.md  meetings.md  meeting2025.md  projects.md  documents.md  talks.md
members.md  apply.md  contact.md
assets/css/site.css         the 5 CSS files concatenated
assets/images/              theme images, logo, file icons
assets/js/menu.js           dropdown + mobile menu
CONVERSION_PLAN.md  README.md (how to edit a page, add a talk, add a meeting)
```

GitHub Pages builds Jekyll on push; no tooling needed to publish. For local
preview, `bundle exec jekyll serve` (Ruby) or `python -m http.server` on a
one-off `jekyll build` output.

## 7. Steps

1. **Repo hygiene**: create `static-site` from `main`; delete the Drupal dump
   (`css/`, `color/`, `mayo/`, `ctools/`, `css_injector/`, `js/`, `uploads/`,
   `styles/`, `pictures/`, `.htaccess`, `.DS_Store`) after copying out the five
   CSS files and the logo; PDFs leave the repo once they are in Drive.
2. **Harvest from Wayback** into a scratch folder: the 8 pages, `/meeting2025`,
   archived `node/NN` detail pages, theme images, `slide.js`, file icons.
3. **Layout**: build `default.html` from the archived homepage; strip login
   form, CAPTCHA, RDF spans, Drupal form ids; menu from `navigation.yml`;
   concatenate CSS and fix `url()` paths; write `menu.js`.
4. **Pages**: convert each archived body to Markdown with pandoc, hand-tidy
   (the Drupal editor left inline font-size spans and empty paragraphs; those
   go). `members.md` starts as a stub for Weixiang to fill.
5. **Lists**: write `list.html` and the `documents.md` / `talks.md` front matter
   from the archived Views output, with `url:` pointing at the repo copy until
   the Drive links arrive, then swap.
6. **Dynamic parts** per section 5 once the two open decisions are in.
7. **Verify**: local build, screenshots against the Wayback snapshot at
   desktop, tablet and phone widths, link checker over every href including
   every Drive link (fetched anonymously to prove sharing works).
8. **Deploy**: merge to `main`, enable Pages (main, root). `CNAME` only if
   `agn.science.lsst.org` DNS will point here (DNS change by LSST/Rubin IT).

## 8. Still needed, but not blocking the build

1. Drive folder link, once the files are uploaded and shared. Fills in the
   `url:` fields of `documents.md` and `talks.md`.
2. Google Form links for the four contact request types. Fills in `_data/forms.yml`.

## Decided

- Jekyll, with all page content in Markdown files. (Weixiang, 2026-11-04)
- Documents and talks hosted in Google Drive; the site only links. (Weixiang, 2026-11-04)
- Files therefore leave the repo; the legacy `sites/default/files/` path is replaced by redirect pages where it matters.
- Members returns as an editable Markdown page.
- Sidebar column kept for now with a static quick-links block; review once visible. (Weixiang, 2026-11-04)
- Contact request types go to Google Forms; placeholders until the form links exist. (Weixiang, 2026-11-04)
- File names unchanged; each old `/sites/default/files/<name>` link becomes the Drive link for that file. (Weixiang, 2026-11-04)
