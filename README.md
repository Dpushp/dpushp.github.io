# Durgakant Pushp — academic website

A responsive static website for a robotics faculty application portfolio. No packages, build step, paid services, or database required.

## Publish on GitHub Pages

1. Create a **public** GitHub repository named `YOUR-USERNAME.github.io`, replacing `YOUR-USERNAME` with your actual GitHub username.
2. Upload the **contents** of this folder to the repository root. `index.html` must be at the top level, alongside `style.css`, `script.js`, `.nojekyll`, and the `assets` folder. Do not upload the ZIP itself.
3. Open repository **Settings → Pages**.
4. Under **Build and deployment**, choose **Deploy from a branch**, then select **main** and **/ (root)** and click **Save**.
5. Wait for the Pages deployment to finish. The site will be available at `https://YOUR-USERNAME.github.io/`.

GitHub instructions: https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site

## Edit

- Content and publications: `index.html`.
- Design and mobile layouts: `style.css`.
- Publication filtering: `script.js`.
- Downloadable CV: `assets/cv.pdf`.

The site uses relative file links, so it also works under a project repository URL.

## Content and review notes

The initial copy uses the CV source dated October 18, 2026 and the research statement dated October 16, 2026 supplied in ChatGPT. The CV is compiled from that source. No home address, telephone number, or referee contact information is included in the website text. The CV retains the supplied professional telephone number; remove it from `assets/cv.tex` and recompile if preferred before public release.

Before publishing, review paper titles, venue years, affiliation, and email. Research photos, a portrait, videos, and verified Google Scholar/ORCID/GitHub profile links can be added when supplied. No placeholder links or invented imagery are included. The site does not claim uncompleted research results.

## Local preview

Open `index.html` in a browser, or run `python3 -m http.server 8000` from this folder and visit `http://localhost:8000`.

## Validation

Local file links, section targets, publication categories, and JavaScript syntax were checked. The CV was compiled from LaTeX. Browser-based visual verification was unavailable in the creation environment; review the desktop and mobile layouts before release.
