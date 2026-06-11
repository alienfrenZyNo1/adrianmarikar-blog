# Adrian Marikar Blog

A fast static personal blog for https://adrianmarikar.com.

## Editing

- Home page: `index.html`
- Styling: `styles.css`
- Posts: `posts/*.html`
- RSS: `feed.xml`
- Sitemap: `sitemap.xml`

## Local test

```bash
docker build -t adrianmarikar-blog .
docker run --rm -p 8088:80 adrianmarikar-blog
curl http://127.0.0.1:8088/
```
