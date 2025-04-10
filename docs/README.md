# Unraid API Documentation

This directory contains the documentation for the Unraid API Python library. The documentation is built using Jekyll and the Just the Docs theme, and is deployed to Cloudflare Pages.

## Deployment

The documentation is automatically deployed to Cloudflare Pages when changes are pushed to the main branch.

### Cloudflare Pages Setup

1. Log in to the [Cloudflare dashboard](https://dash.cloudflare.com/) and select your account.
2. In Account Home, select **Workers & Pages** > **Create**.
3. Select the **Pages** tab.
4. Select **Connect to Git**.
5. Select your GitHub repository and then select **Begin setup**.
6. In the **Build settings** section, configure the following:
   - Production branch: `main`
   - Build command: `cd docs && bundle install && bundle exec jekyll build`
   - Build output directory: `docs/_site`
   - Environment variables:
     - `RUBY_VERSION`: `3.3.0`
     - `JEKYLL_ENV`: `production`
7. Click **Save and Deploy**.

### Manual Deployment

To manually deploy the documentation to Cloudflare Pages:

1. Install the Cloudflare Pages CLI:
   ```bash
   npm install -g wrangler
   ```
2. Authenticate with Cloudflare:
   ```bash
   wrangler login
   ```
3. Build the documentation:
   ```bash
   cd docs
   bundle exec jekyll build
   ```
4. Deploy to Cloudflare Pages:
   ```bash
   wrangler pages publish _site --project-name unraid-api-docs
   ```

## Structure

The documentation is organized as follows:

- `index.md`: Home page
- `content/`: Documentation content
  - `getting-started/`: Getting started guides
  - `api/`: API reference
  - `cli/`: Command-line interface documentation
  - `home-assistant/`: Home Assistant integration documentation
- `assets/`: Static assets
  - `css/`: Custom CSS
  - `js/`: Custom JavaScript
  - `images/`: Images
- `_layouts/`: Layout templates
  - `default.html`: Default layout template
  - `home.html`: Home page layout template
- `_includes/`: Reusable components
  - `head.html`: HTML head content
  - `header.html`: Page header
  - `footer.html`: Page footer
  - `nav.html`: Navigation menu
- `_config.yml`: Jekyll configuration
- `_headers`: HTTP headers for Cloudflare Pages
- `_redirects`: URL redirects for Cloudflare Pages
- `Gemfile`: Ruby dependencies
- `build.sh`: Build script for Cloudflare Pages
