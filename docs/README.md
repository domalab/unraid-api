# Unraid API Documentation

This directory contains the documentation for the Unraid API Python library. The documentation is built using Jekyll and the Just the Docs theme, and is deployed to Cloudflare Pages.

## Local Development

To run the documentation locally:

1. Install Ruby and Bundler
2. Install dependencies:
   ```bash
   cd docs
   bundle install
   ```
3. Start the local server:
   ```bash
   bundle exec jekyll serve
   ```
4. Open your browser to http://localhost:4000

## Deployment

The documentation is automatically deployed to Cloudflare Pages when changes are pushed to the main branch.

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
- `_config.yml`: Jekyll configuration
- `_headers`: HTTP headers for Cloudflare Pages
- `_redirects`: URL redirects for Cloudflare Pages
- `Gemfile`: Ruby dependencies
