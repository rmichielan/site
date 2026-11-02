# Riccardo Michielan — Academic Research Website

Public site: https://rmichielan.github.io/site/

This is a static GitHub Pages website containing research information, publications, a CV, the PAiNe MSCA project and Interactive Papers. No custom domain or server-side framework is required.

## Publishing

Publish the contents of this folder at the root of the GitHub repository currently serving `/site/`. Keep the `assets/` and `interactive-papers/` directories intact. The static build uses `.nojekyll`.

For the **v1.1 SEO release**, including Google Search Console and migration from the old Google Sites address, read [SEO_DEPLOYMENT_GUIDE_v1.1.md](SEO_DEPLOYMENT_GUIDE_v1.1.md).

You can run `python3 tools/check_seo.py` to check all eight pages' metadata, the sitemap and the link-preview assets. The validator uses the Python standard library only.

The v1 visual design and interaction logic are unchanged by v1.1.
