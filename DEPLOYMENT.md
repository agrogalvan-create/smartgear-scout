# SmartGear Scout — deployment runbook

## Recommended evaluation: Cloudflare Pages Free
Official documentation: https://developers.cloudflare.com/pages/ and https://developers.cloudflare.com/pages/platform/limits/

Cloudflare Pages supports Git-connected static-site deployments and its Free plan currently lists 500 builds/month. Confirm the current self-serve agreement and commercial-use suitability before activating.

## Launch steps (not yet performed)
1. Create/sign in to a Cloudflare account under the owner's control.
2. Create a Pages project using Git integration, selecting `agrogalvan-create/smartgear-scout` and `main`.
3. Configure no framework, production branch `main`, build command `python3 scripts/build_site.py`, and build output directory `dist`. This builds a public-only folder rather than uploading internal research, tests, or GitHub configuration. Confirm Python is available in the build image.
4. Confirm the assigned `*.pages.dev` URL and HTTPS.
5. Check homepage, About, Disclosure and all linked guides on mobile.
6. Only after URL verification, create a sitemap with that canonical origin, and submit to search engines.
7. Keep affiliate links inactive until program approval and disclosure review.

## Launch blockers
- Cloudflare account connection not authorized/available through current GitHub integration.
- No verified public production URL.
- Merchant approvals, payments, taxes and terms for Argentina still pending.
- No additional subscriptions or purchases authorized.

Do not claim deployment succeeded until the public URL is visited and checked.

## Search Console discovery (2026-11-17)
Google emailed confirmation that the property `https://agrogalvan-create.github.io/smartgear-scout/` was verified in Search Console. This **does not prove that the site is reachable or that Google has indexed any page**. Public URL availability must be tested independently. GitHub Pages may be unsuitable for a primarily commercial affiliate business under GitHub's service terms; do not assume it is the production host.

To generate a sitemap **only after confirming the actual live URL**:

```sh
python3 scripts/build_site.py
SITE_URL=https://CONFIRMED-HOST/CONFIRMED-PATH python3 scripts/generate_sitemap.py
```

The generator writes `dist/sitemap.xml` and appends the correct Sitemap directive to `dist/robots.txt`. Submit that verified sitemap URL in the matching Search Console property. Do not submit a URL on an unverified host.
