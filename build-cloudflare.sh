#!/bin/bash
set -e

echo "Starting Cloudflare Pages build process..."
echo "Ruby version: $(ruby -v)"

# Change to the docs directory
cd docs

# Install dependencies
echo "Installing dependencies..."
gem install bundler
bundle config set --local path 'vendor/bundle'
bundle install

# Add base64 gem to silence warnings and ensure theme is installed
gem install base64
gem install just-the-docs -v "0.7.0"

# Create a symlink to the theme's assets to ensure they're available
mkdir -p _sass
ln -sf "$(bundle info --path just-the-docs)/_sass" _sass/just-the-docs

# Create _site directory if it doesn't exist
mkdir -p _site

# Build the site with minimal configuration
echo "Building site for Cloudflare Pages..."

# Create a temporary _config_build.yml file that uses the theme directly
cat > _config_build.yml << EOL
title: Unraid API Documentation
description: Documentation for the Unraid API Python library
baseurl: ""
url: ""

# Build settings
markdown: kramdown
plugins:
  - jekyll-feed
  - jekyll-seo-tag

# Theme settings
theme: just-the-docs
color_scheme: light

# Aux links for the upper right navigation
aux_links:
  "Unraid API on GitHub":
    - "https://github.com/domalab/unraid-api"

# Makes Aux links open in a new tab
aux_links_new_tab: true

# Back to top link
back_to_top: true
back_to_top_text: "Back to top"

# Footer content
footer_content: "Copyright &copy; 2025 domalab. Distributed under an <a href=\"https://github.com/domalab/unraid-api/blob/main/LICENSE\">MIT license.</a>"

# Heading anchor links
heading_anchors: true

# Enable or disable the site search
search_enabled: true

# Set the search token separator
search_tokenizer_separator: /[\s/]+/
EOL

# Build with the simplified config
JEKYLL_ENV=production bundle exec jekyll build --config _config_build.yml

# Ensure .nojekyll file exists in the output directory
touch _site/.nojekyll

echo "Build completed successfully!"
