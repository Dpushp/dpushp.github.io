# Updating your GitHub Pages website

Your repository: https://github.com/Dpushp/dpushp.github.io
Your website: https://dpushp.github.io/

## 1. Replace the old website with this version

You do not need to delete or rename your repository.

1. Extract `Durgakant_Pushp_Academic_Website.zip` on your computer.
2. Open the extracted folder. You should see `index.html`, `research.html`, `publications.html`, `style.css`, `script.js`, `videos.js`, `assets/`, and the other files.
3. Open your GitHub repository and select the `main` branch.
4. Click **Add file → Upload files**.
5. Drag the CONTENTS of the extracted folder into the upload area, including the `assets`, `data`, and `checks` folders. Do not upload the ZIP or wrap everything in an extra folder. Preserve the subfolders when dragging them.
6. GitHub will replace existing files with matching paths. In particular, the new root `index.html`, `style.css`, and `script.js` replace the old versions. New pages and folders are added. Old unreferenced files can remain; they are not used by this template.
7. Enter the commit message `Update academic website` and commit directly to `main`. If your repository requires a pull request, merge that request into `main` instead.
8. Open **Settings → Pages**. The source should be **Deploy from a branch**, with **main** and **/ (root)**. Save if needed. If you currently use a custom Actions publishing workflow, switch to branch publishing for these prebuilt files.
9. Wait for the Pages deployment to finish in **Actions**, then open https://dpushp.github.io/. Use Ctrl+Shift+R to refresh cached files.

The root `index.html` should appear directly in the repository's file list. The `assets` folder must also be uploaded. A missing assets folder causes broken photos and CV links.

## 2. Replace or add a research video (NO rebuild required)

All video URLs are in the root file **videos.js**. The same setting is used on project pages and publication video links, including video slots that are currently empty.

Current settings:

```javascript
window.RESEARCH_VIDEOS = {
  "povnav": "https://youtu.be/wVwIQdXpUM8",
  "context-policy": "https://www.youtube.com/watch?v=Ial-EDNPSe0",
  "bounded-drones": "https://youtu.be/iD6xyyxQCGI",
  "hybrid-system": "https://youtu.be/LlW-ylcU0mk",
  "miniugv2": "",
  "racing": "",
  "embodiment-search": ""
};
```

After compiling and uploading your own video to YouTube:

1. Copy its YouTube URL. The video must be public or unlisted to be viewable by website visitors.
2. In GitHub, open **videos.js** and click the pencil icon (**Edit this file**).
3. Replace the URL between quotes next to the matching project. For example, set the `racing` value to your racing video's URL. Keep the project key, quotes, and commas.
4. Click **Commit changes** and commit to `main`.
5. After Pages redeploys, refresh the relevant project page. Its video section and publication video links update automatically. No Python command or website rebuild is needed.

Use an empty string `""` to hide a project's video. Full YouTube watch, youtu.be, Shorts, live, and embed URLs are accepted, as are 11-character YouTube video IDs. Other video providers are not supported by this player.

Videos load after the visitor clicks Play. If the owner disables embedding or YouTube requires account access, use the separate **Watch on YouTube** link beneath the player. Paper association was verified; playback availability depends on YouTube.

## 3. Replace your picture (NO rebuild required)

The uploaded lab photograph is included unchanged at:

`assets/images/profile.png`

Replace that file with a new PNG using the same name. The homepage uses CSS `object-fit` and `object-position` to fit the photograph; the original image file is not cropped or edited. Contact displays the full image.

To adjust the homepage framing, edit `.portrait img` in `style.css`. Its current `object-position` is `56% 30%`.

If your new image has a different format or filename, update its paths in `build.py` and run the build command below. Alternatively, export the new image as `profile.png`.

## 4. Update your CV (NO rebuild required for the download)

Replace **assets/Durgakant_Pushp_CV.pdf** with your new PDF, keeping the filename. The same download works from the homepage, CV, and Contact pages.

The included PDF is compiled from your uploaded CV source. Its editable LaTeX source is **assets/Durgakant_Pushp_CV.tex**. Replace the PDF with your preferred final CV whenever ready. The web CV is a separate summary; updating the PDF alone does not change that summary.

## 5. Edit content and generate pages

All pages are prebuilt and work on GitHub Pages without installing anything. For systematic content changes, edit these files locally:

| File | What to change |
| --- | --- |
| `data/profile.json` | Name, role, affiliation, email, biography, research vision, teaching statement, profile links, and lab settings |
| `data/projects.json` | Research projects, project descriptions, images, resource URLs, and publication associations |
| `data/publications.json` | Publication records, authors, venues, years, paper links, and awards |
| `data/news.json` | News entries and dates |
| `videos.js` | YouTube video URLs; direct edit, no rebuild |
| `style.css` | Fonts, colors, spacing, responsiveness, and photo framing; direct edit, no rebuild |
| `build.py` | Page structure, CV summary entries, and teaching experience entries |

1. Open the extracted folder in VS Code or Cursor.
2. Edit the relevant JSON file. Keep valid JSON syntax: double quotes around strings, commas between entries, and no trailing comma.
3. Open a terminal in the website folder and run:

```bash
python3 build.py
```

On Windows, `py build.py` may be the appropriate command.

4. Run the local checks:

```bash
python3 checks/check_site.py
node checks/check_interactions.js
```

The second command is optional if Node.js is unavailable. Neither the site nor its build requires Node.js.

5. Open `index.html` in your browser to review the result. You can also run `python3 -m http.server 8000` and visit http://localhost:8000.
6. Upload the changed generated HTML files AND the edited source files to GitHub. Uploading only a JSON file does not regenerate the website on GitHub; run `build.py` first.

You can instead edit generated `.html` files directly on GitHub for a quick text change. However, `build.py` overwrites generated HTML on the next build, so make the same change in the source to retain it.

## 6. Add publications or project pages

To add a publication, copy one object in `data/publications.json`, assign a unique `id`, and fill in the record. Allowed kinds are `Journal`, `Conference`, `Preprint`, and `Other`. Set `project` to an existing project ID or an empty string. Run `python3 build.py` and upload the updated publications page and any other regenerated pages.

To add a research project, copy an object in `data/projects.json` and choose a unique lowercase `id`. Its page will be `project-YOUR-ID.html`. Put its image in `assets/images/`, and add a matching key in `videos.js`. Run `python3 build.py` and upload the generated files and image. `related` contains publication IDs from `data/publications.json`.

## 7. Convert to a lab website later

In `data/profile.json`, change:

```json
"mode": "lab",
"lab_name": "Your Confirmed Lab Name",
"lab_tagline": "Your Lab Research Area",
"lab_mission": "Your lab mission statement.",
"lab_photo": "assets/images/your-lab-photo.jpg"
```

Update institution, location, role, email, site URL, and biography as appropriate. Put the photograph at the path specified, or leave `lab_photo` empty. Add confirmed members to `people`:

```json
"people": [
  {
    "name": "Member Name",
    "group": "Graduate researchers",
    "role": "Ph.D. student",
    "interests": "Research interests"
  }
]
```

Run `python3 build.py`. Lab mode changes the branding and homepage, adds People to navigation, and presents the CV page as About / PI. Research projects and publications keep their existing URLs. No lab or group membership is claimed in the current personal version.

## 8. What was checked

- 15 generated HTML pages, including the 404 page.
- Local file links, images, section targets, one main heading per page, and image alternative text.
- Video URL parsing, invalid URL rejection, generated YouTube links, hidden empty video settings, click-to-load embedding, menu toggle, and both filter groups.
- JavaScript syntax and source JSON parsing.
- Alternate lab-mode generation.
- Browser-based visual QA was unavailable in the creation environment. Review desktop and mobile layouts after upload. The page design follows the approved preview.

## 9. Content provenance and review

Publication records use the uploaded CV source (`Pasted text(3).txt`, October 18, 2026). This includes the CV's MiniUGV2 ISER 2026 entry and the supplied ICRA 2026 title; venue-year and title conventions can be adjusted in `data/publications.json` if needed. The lab's publication page uses some different title/year conventions. The context-policy title retains the wording in the supplied CV.

The IJRR award is described as Q2 2025, consistent with its award period; the CV source lists its receipt under 2026. New research directions are labelled ongoing.

The four video URLs are taken from their associated papers:

- POVNav / Navigating the Wild: https://arxiv.org/html/2511.07750v1 (Supplementary Video)
- Context-generative policy: https://arxiv.org/pdf/2409.11604 (experimental video)
- Bounded-rational drones: https://arxiv.org/pdf/2307.15798 (experimental video)
- UAV–miniUGV hybrid: https://arxiv.org/pdf/2209.11704 (Supplementary Material)

No verified MiniUGV2 or racing supplementary YouTube URL was established in this pass; those settings are empty for your compiled videos. No Google Scholar, ORCID, or LinkedIn profile URL was inferred; add verified URLs to `data/profile.json` when ready.

See `ASSET_SOURCES.md` for research image attribution. The photograph is the image you uploaded, used unchanged.
