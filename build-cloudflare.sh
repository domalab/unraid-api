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

# Add base64 gem to silence warnings
gem install base64

# Create _site directory if it doesn't exist
mkdir -p _site

# Build the site with minimal configuration
echo "Building site for Cloudflare Pages..."
JEKYLL_ENV=production bundle exec jekyll build --config _config.yml --baseurl ''

# Ensure .nojekyll file exists in the output directory
touch _site/.nojekyll

echo "Build completed successfully!"
