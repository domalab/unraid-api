#!/bin/bash
set -e

echo "Starting build process..."
echo "Ruby version: $(ruby -v)"

cd docs
echo "Installing dependencies..."
bundle install
echo "Building site..."
JEKYLL_ENV=production bundle exec jekyll build

echo "Build completed successfully!"
