# v1.1 — Search visibility and link previews

**Official site (no purchased domain required):** https://rmichielan.github.io/site/

This release contains only technical SEO, structured-data and share-preview changes. It does **not** modify the v1 design, CSS, JavaScript, interactive article content or research functionality.

## 1. Publish on GitHub Pages

1. Keep a backup or tag of the currently published v1 release.
2. Upload the **contents of this `site-main` folder**, not an extra parent `site-main/` folder, into the same repository root that already serves `/site/` (usually repository `site`, branch `main`, root folder). Overwrite existing files and include all new PNGs under `assets/social/`, `.nojekyll`, `sitemap.xml` and the updated HTML files.
3. Wait until GitHub Pages deploys, then open the following in a private/incognito window:
   - https://rmichielan.github.io/site/
   - https://rmichielan.github.io/site/research.html
   - https://rmichielan.github.io/site/publications.html
   - https://rmichielan.github.io/site/interactive-papers.html
   - https://rmichielan.github.io/site/interactive-papers/planted-cliques-rgg/
   - https://rmichielan.github.io/site/sitemap.xml
   - https://rmichielan.github.io/site/assets/social/planted-cliques-rgg.png
4. Run `python3 tools/check_seo.py` (Python 3, standard library only) in the repo root, optionally before committing.

**Expected result:** the 8 canonical URLs in the sitemap all begin `https://rmichielan.github.io/site/`. The old `riccardo1803.github.io/site` URLs have been removed from site metadata (the GitHub profile `github.com/riccardo1803` is still valid).

## 2. Google Search Console (manual account step)

1. Open https://search.google.com/search-console/ and add a property of type **URL prefix**, not **Domain**.
2. Enter exactly `https://rmichielan.github.io/site/` (including `/site/`).
3. Choose verification by **HTML file** if available. Download the exact `google....html` file that Google gives you, place it at the **repository root**, publish it and confirm that it is publicly reachable at `https://rmichielan.github.io/site/google....html` using the *exact actual filename*. Go back and click **Verify**. Do not rename, edit or delete the verification file. **Alternatively**, Google may offer an HTML `<meta name="google-site-verification" ...>` tag: paste the actual Google-issued tag in `index.html` inside `<head>`, publish and then verify. No verification token has been fabricated or placed in this release.
4. Under **Sitemaps**, submit `https://rmichielan.github.io/site/sitemap.xml` (or `sitemap.xml` if the form uses the property prefix).
5. Under **URL Inspection**, inspect the homepage and key pages (Research, Publications, About, Interactive Papers) and use **Request indexing** when the live URL is indexable. Monitor indexing reports over the next few weeks; submitting is not a guarantee of appearance or rank.

**Note about `robots.txt`:** the file `site/robots.txt` is *not* the host-level robots.txt. Robots files apply at the hostname root (`https://rmichielan.github.io/robots.txt`), not to GitHub project subfolders. This package intentionally does not claim to configure the host-level robots file. Search Console sitemap submission works independently.

## 3. Migrate readers from the old Google Sites website

Old site: https://sites.google.com/view/rmichielan/

A proper HTTP 301 cannot normally be configured for that Google-managed `sites.google.com` URL from the Google Sites editor. Do not claim this is a true redirect or install a fake redirect snippet.

**After the new GitHub site is published and verified:**

1. Edit your old Google Sites homepage, placing a large link in the top/first visible section. Suggested text:

   **Riccardo Michielan — My academic website has moved.**

   > My current academic website is now available at https://rmichielan.github.io/site/. Please visit the new site for research, publications, Interactive Papers, PAiNe, my CV and contact details.

2. Remove or de-emphasize obsolete research/contact details from the old homepage to avoid conflicting versions, and publish the Google Sites update. Keep the old address accessible as a signpost for visitors with saved links.
3. After Search Console confirms that Google is discovering/indexing the new site, optionally open Google Sites **Publish** (down arrow) → **Publish settings** → **Request public search engines to not display my site** → **Save**, and publish if prompted. This is only a request, not a guaranteed or immediate removal. If you're relying heavily on organic discovery through the old page, postpone this step until the new site appears in search.
4. Update external profile links on ORCID, Google Scholar, ResearchGate, institutional directories, conference bios and other pages under your control. In particular, the canonical website in these profiles should be the new GitHub Pages URL.
5. If you have access to Search Console for the old Google Sites URL, inspect its reports, but note that the Google Sites interface has limited redirect controls.

## 4. Check social previews

Once deployed, you can test public URLs (not `file://` or localhost) with:

- Facebook Sharing Debugger: https://developers.facebook.com/tools/debug/
- LinkedIn Post Inspector: https://www.linkedin.com/post-inspector/
- X/Twitter: share a URL in a new draft to inspect its preview (appearance depends on X availability/cache).

These services can cache old previews. Try their re-scrape/inspect features if you still see outdated cards. Each public page has one absolute `og:image` URL, `twitter:image`, a description, `og:image:alt` and the correct canonical.

## 5. Which files changed?

- Updated SEO metadata and JSON-LD in the 8 public HTML pages.
- Updated the editable source `src/pages/interactive-papers.html` so its SEO content is consistent with the compiled page.
- Updated `sitemap.xml` and `robots.txt`.
- Added five page-specific social previews: `research.png`, `publications.png`, `about.png`, `contacts.png`, `planted-cliques-rgg.png`.
- Added `.nojekyll` for direct static-file publishing.
- Added `tools/check_seo.py` as a repeatable static check.

The pre-existing social cards (`home.png`, `paine.png`, `interactive-papers.png`) were not changed. No CSS or application JavaScript was changed. Remember to propagate the SEO metadata if you regenerate compiled HTML from templates in the future.

## 6. Why these modifications help, and limitations

- Canonical consistency and a sitemap help crawlers understand the official addresses.
- Open Graph and Twitter metadata provide link preview content, but the platform chooses whether to render it.
- Schema.org `Person`, `WebSite`, `WebPage` and `ScholarlyArticle` describe established facts in machine-readable form; they do not guarantee special results or higher rankings.
- Crawlers and AI/LLM systems do not all use the same discovery methods. No `llms.txt` or AI-specific crawler exemptions have been added because they aren't required for regular Google indexing and cannot guarantee inclusion in AI answers.
- Search indexing and rankings ultimately depend on crawling, content and external links. Expect updates to take time.

## Sources

- Google Search Central: https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes
- Search Console verification: https://support.google.com/webmasters/answer/9008080
- Request reindexing: https://support.google.com/webmasters/answer/9012289
- Google Sites publishing and search opt-out: https://support.google.com/sites/answer/6372880
