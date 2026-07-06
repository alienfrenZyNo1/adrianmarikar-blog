# Adrian Marikar Blog

A fast static personal blog for <https://adrianmarikar.com>, stored in GitHub and deployed as a small nginx Docker container through Coolify.

The site is intentionally simple: no CMS, no database, no build step, and no framework. A post is an HTML file, the homepage is an HTML file, and deployment is GitHub → Coolify → nginx.

## How the blog works

The blog is a static website served by nginx:

1. Source files live in this repository.
2. Coolify pulls the repository from GitHub.
3. The `Dockerfile` builds an `nginx:1.27-alpine` image.
4. nginx serves the static files from `/usr/share/nginx/html`.
5. Cloudflare sits in front of the VPS/domain.

There is no server-side rendering or runtime content generation. Every public page is already present as a file in the repository.

## Repository layout

```text
adrianmarikar-blog/
  index.html                  # Homepage and latest-post cards
  styles.css                  # Shared visual design system
  script.js                   # Small client-side polish
  feed.xml                    # RSS feed
  sitemap.xml                 # Search-engine sitemap
  robots.txt                  # Crawler rules and sitemap pointer
  llms.txt                    # AI/LLM-readable site summary
  404.html                    # Static not-found page
  Dockerfile                  # nginx container image
  nginx.conf                  # Static-site routing, headers, caching
  categories/                 # Hand-maintained category archive pages
  posts/                      # One HTML file per post
```

Important supporting files:

- `indexnow-key.txt` and `1f4e5dd73be99f3d3b631aa6db2f6eba.txt` support search/discovery verification workflows.
- `how-this-blog-is-built-and-maintained.html` is a legacy redirect page to the canonical post in `posts/`.

## Content model

The content model is manual and explicit:

- **Homepage:** `index.html`
- **Posts:** `posts/*.html`
- **Category archives:** `categories/*.html`
- **RSS:** `feed.xml`
- **Sitemap:** `sitemap.xml`
- **LLM/site summary:** `llms.txt`

When adding a new post, update all relevant discovery surfaces so browsers, feed readers, search engines, and LLM crawlers see the same site state.

## Adding or editing a post

For a new post:

1. Create a new HTML file under `posts/`.
2. Add the post card to `index.html`.
3. Add the post to any relevant `categories/*.html` page.
4. Add an `<item>` to `feed.xml`.
5. Add a `<url>` entry to `sitemap.xml`.
6. Update `llms.txt` if the new post should be summarised for AI readers.
7. Check canonical URLs, titles, descriptions, Open Graph/Twitter metadata, and article JSON-LD.
8. Commit and push to GitHub.
9. Let Coolify deploy, then verify the live URLs.

For an existing post:

1. Edit the relevant `posts/*.html` file.
2. Update `article:modified_time` and JSON-LD `dateModified` if the change is material.
3. Update `feed.xml`, `sitemap.xml`, category pages, or `llms.txt` only if the public listing/summary changed.
4. Verify locally before pushing.

## Visual design

Most styling lives in `styles.css`:

- dark high-contrast layout;
- neon/glass panels;
- shared header/footer styles;
- article cards;
- post typography;
- code block styling;
- responsive navigation and spacing.

Pages currently reference a cache-busted stylesheet path such as:

```html
<link rel="stylesheet" href="/styles.css?v=20260611-organic1">
```

If the CSS changes in a way that must be visible immediately, bump the query string in touched HTML pages to avoid stale browser/Cloudflare cache.

## JavaScript

`script.js` is intentionally small. It currently:

- fills an element with `id="year"` if present;
- tracks pointer position for CSS glow effects;
- computes a sticky-header anchor offset for in-page links;
- updates the offset on resize/orientation changes.

The site should remain usable without JavaScript.

## nginx behaviour

`nginx.conf` configures the production static server:

- serves files from `/usr/share/nginx/html`;
- uses `index.html` as the index page;
- returns `/404.html` for missing pages;
- redirects `/how-this-blog-is-built-and-maintained.html` to `/posts/how-this-blog-is-built-and-maintained.html`;
- removes trailing slashes from `.html/` URLs;
- sets security headers including CSP, HSTS, frame blocking, referrer policy, and permissions policy;
- caches static assets such as CSS, JS, and images for 30 days.

The CSP allows the site itself plus the analytics script/connect endpoint at `https://analytics.adrianmarikar.com`.

## Local development and testing

From the repository root:

```bash
# Build the same nginx image Coolify uses
docker build -t adrianmarikar-blog .

# Run locally on http://127.0.0.1:8088
docker run --rm -p 8088:80 adrianmarikar-blog
```

In another terminal:

```bash
curl -I http://127.0.0.1:8088/
curl -I http://127.0.0.1:8088/feed.xml
curl -I http://127.0.0.1:8088/sitemap.xml
```

Useful content checks:

```bash
# Parse XML files
python3 - <<'PY'
import xml.etree.ElementTree as ET
for path in ['feed.xml', 'sitemap.xml']:
    ET.parse(path)
    print(f'{path}: ok')
PY

# Find accidental secret-looking strings before committing
grep -RInE '(api[_-]?key|secret|password|token|BEGIN (RSA|OPENSSH|PRIVATE) KEY)' . \
  --exclude-dir=.git \
  --exclude=README.md
```

For HTML checks, open the changed files in a browser or use a simple local static server/container smoke test. Because the site is plain HTML, there is no package install step.

## Deployment

Production deployment is handled by Coolify from the GitHub repository.

Typical deployment loop:

```text
Edit files
  ↓
Run local checks / Docker build
  ↓
Commit to GitHub
  ↓
Push to main
  ↓
Coolify builds the Dockerfile and deploys the nginx container
  ↓
Verify live URLs on adrianmarikar.com
```

After deployment, verify at least:

```bash
curl -fsS https://adrianmarikar.com/ >/dev/null
curl -fsS https://adrianmarikar.com/feed.xml >/dev/null
curl -fsS https://adrianmarikar.com/sitemap.xml >/dev/null
curl -fsS https://adrianmarikar.com/robots.txt >/dev/null
```

For a new post, also verify:

```bash
POST=/posts/example-post.html
curl -fsS "https://adrianmarikar.com${POST}" >/dev/null
curl -fsS https://adrianmarikar.com/ | grep -F "${POST}"
curl -fsS https://adrianmarikar.com/feed.xml | grep -F "${POST}"
curl -fsS https://adrianmarikar.com/sitemap.xml | grep -F "${POST}"
```

## SEO and discovery checklist

Each public post should usually include:

- unique `<title>`;
- useful `<meta name="description">`;
- canonical URL;
- Open Graph metadata;
- Twitter card metadata;
- article JSON-LD with `datePublished`, `dateModified`, author, publisher, URL, and keywords;
- a link from the homepage or a category archive;
- RSS and sitemap entries.

Keep `robots.txt`, `sitemap.xml`, `feed.xml`, and `llms.txt` aligned with the public content you want crawled.

## Safety rules

- Do not commit secrets, API keys, private keys, deployment tokens, `.env` files, logs, or raw analytics exports.
- Keep the site static unless there is a deliberate reason to add runtime code.
- Do not add third-party scripts without checking the CSP in `nginx.conf`.
- Prefer explicit, inspectable HTML over hidden generators unless the site grows enough to justify a build pipeline.

## Related live pages

- Homepage: <https://adrianmarikar.com/>
- RSS feed: <https://adrianmarikar.com/feed.xml>
- Sitemap: <https://adrianmarikar.com/sitemap.xml>
- Build/maintenance post: <https://adrianmarikar.com/posts/how-this-blog-is-built-and-maintained.html>
