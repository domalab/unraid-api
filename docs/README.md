# Unraid API Documentation

This directory contains the documentation for the Unraid API library, built with MkDocs and the Material theme.

## Development

To work on the documentation locally:

1. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Serve the documentation locally:
   ```bash
   mkdocs serve
   ```

3. Build the documentation:
   ```bash
   mkdocs build
   ```

## Structure

- `docs/` - Documentation source files
  - `assets/` - Custom CSS, JavaScript, and images
  - `getting-started/` - Getting started guides
  - `api-reference/` - API reference documentation
  - `advanced/` - Advanced usage guides
  - `cli/` - CLI documentation
  - `development/` - Development guides
  - `about/` - License and changelog

## Building and Deployment

The documentation is automatically built and deployed to GitHub Pages whenever changes are pushed to the main branch. The GitHub workflow is defined in `.github/workflows/docs.yml`. 