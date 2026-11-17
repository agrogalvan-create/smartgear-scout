# SmartGear Scout — deployment runbook

## Recommended evaluation: Cloudflare Pages Free
Official documentation: https://developers.cloudflare.com/pages/ and https://developers.cloudflare.com/pages/platform/limits/

Cloudflare Pages supports Git-connected static-site deployments and its Free plan currently lists 500 builds/month. Confirm the current self-serve agreement and commercial-use suitability before activating.

## Deployment configuration (completed by owner)
1. Create/sign in to a Cloudflare account under the owner's control.
2. Create a Pages project using Git integration, selecting `agrogalvan-create/smartgear-scout` and `main`.
3. Configure no framework, production branch `main`, build command `python3 scripts/build_site.py`, and build output directory `dist`. This builds a public-only folder rather than uploading internal research, tests, or GitHub configuration. Confirm Python is available in the build image.
4. Confirm the assigned `*.pages.dev` URL and HTTPS.
5. Check homepage, About, Disclosure and all linked guides on mobile.
6. Only after URL verification, create a sitemap with that canonical origin, and submit to search engines.
7. Keep affiliate links inactive until program approval and disclosure review.

## Remaining business and verification items
- Merchant approvals, payments, taxes and terms for Argentina remain pending.
- Search Console indexing is not yet confirmed.
- Production smoke-check workflow must report a successful run before health is claimed.
- No additional subscriptions or purchases authorized.

## Search Console discovery (2026-11-17)
Google emailed confirmation that the property `https://agrogalvan-create.github.io/smartgear-scout/` was verified in Search Console. This **does not prove that the site is reachable or that Google has indexed any page**. Public URL availability must be tested independently. GitHub Pages may be unsuitable for a primarily commercial affiliate business under GitHub's service terms; do not assume it is the production host.

To generate a sitemap for the already-confirmed live URL:

```sh
python3 scripts/build_site.py
python3 scripts/build_site.py
```

The generator writes `dist/sitemap.xml` and appends the correct Sitemap directive to `dist/robots.txt`. Submit that verified sitemap URL in the matching Search Console property. Do not submit a URL on an unverified host.

## Confirmed Cloudflare deployment (2026-11-17)
The owner supplied a Cloudflare Pages dashboard screenshot showing successful production deployments for `main` and automatic deployments enabled. The assigned domain is `https://smartgear-scout.pages.dev`. A green deployment status confirms the platform build/deployment completed; independent HTTP content verification and Search Console indexing remain separate checks.

### Production sitemap setup
The build script defaults to the confirmed production URL `https://smartgear-scout.pages.dev`; an optional Cloudflare Pages production environment variable `SITE_URL` can override it. The build script generates `dist/sitemap.xml` and adds the sitemap directive to `dist/robots.txt` during the next deployment. Do not submit the sitemap to Google until its URL is reachable. The previously verified Search Console property for GitHub Pages does **not** cover the new `pages.dev` URL; add and verify a new URL-prefix property for `https://smartgear-scout.pages.dev/` before submitting `https://smartgear-scout.pages.dev/sitemap.xml`.

## Search Console status and next checks (2026-11-17)
The owner verified the Cloudflare Pages URL-prefix property by uploading an HTML ownership file. Keep this file at the site root and in the build output so ownership remains verified. The production sitemap opened in a browser and listed the published editorial pages. Search Console initially reported `Couldn't fetch` / `Couldn't read sitemap` and zero discovered pages; a later live URL inspection confirmed that the homepage is available to Google and can be indexed. This is not yet proof of actual indexing. The owner then hit Google's daily manual indexing request quota; wait for quota reset rather than repeatedly submitting.

Next checks: inspect the existing sitemap submission after Google has had time to re-fetch it; compare its actual URL with `https://smartgear-scout.pages.dev/sitemap.xml`; use URL Inspection live test on the sitemap or homepage as appropriate; check Pages > indexing for crawl results over the next few days. Do not infer an XML failure from the browser message `This XML file does not appear to have any style information`; that message is normal for XML. The sitemap generator now excludes Google ownership verification HTML files while preserving those files in deployment output.

