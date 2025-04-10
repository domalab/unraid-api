#!/bin/bash
set -e

echo "Starting build process..."
echo "Ruby version: $(ruby -v)"

# Make sure we're using Ruby 3.3.0
if [[ $(ruby -v) != *"ruby 3.3"* ]]; then
  echo "Warning: Not using Ruby 3.3.x. This may cause issues."
fi

cd docs

echo "Installing dependencies..."
gem install bundler
bundle config set --local path 'vendor/bundle'
bundle install

echo "Building site..."
if [ "$CF_PAGES" = "1" ] || [ "$CLOUDFLARE_PAGES" = "1" ]; then
  echo "Building for Cloudflare Pages..."
  JEKYLL_ENV=production bundle exec jekyll build --config _config.yml,_config_production.yml --baseurl '' --trace
else
  echo "Building for local or other environment..."
  JEKYLL_ENV=production bundle exec jekyll build --trace
fi

# Ensure .nojekyll file exists in the output directory
touch _site/.nojekyll

echo "Build completed successfully!"
