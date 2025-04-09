# Deploying to Cloudflare Pages

This guide explains how to deploy the Unraid API documentation to Cloudflare Pages.

## Prerequisites

Before you begin, you'll need:

1. A Cloudflare account
2. A GitHub account
3. The repository cloned to your local machine

## Setting Up Cloudflare Pages

### 1. Log in to Cloudflare Dashboard

Go to [Cloudflare Dashboard](https://dash.cloudflare.com/) and log in to your account.

### 2. Create a New Pages Project

1. Click on "Pages" in the sidebar
2. Click "Create a project"
3. Select "Connect to Git"

### 3. Connect Your GitHub Repository

1. Click "Connect GitHub"
2. Authorize Cloudflare to access your GitHub account
3. Select the repository containing the Unraid API documentation

### 4. Configure Build Settings

Configure the build settings as follows:

- **Project name**: `unraid-api-docs` (or your preferred name)
- **Production branch**: `main`
- **Build command**: `cd docs && bundle install && bundle exec jekyll build`
- **Build output directory**: `docs/_site`
- **Root directory**: `/` (leave as default)

### 5. Environment Variables

Add the following environment variables:

- `RUBY_VERSION`: `3.1.2`
- `JEKYLL_ENV`: `production`

### 6. Advanced Build Settings

Under "Advanced build settings", add the following:

- **Build cache**: Enable
- **Web Analytics**: Enable if desired

### 7. Save and Deploy

Click "Save and Deploy" to start the deployment process.

## Custom Domain (Optional)

To use a custom domain for your documentation:

1. Go to your Pages project in the Cloudflare Dashboard
2. Click on "Custom domains"
3. Click "Set up a custom domain"
4. Enter your domain name and follow the instructions

## Continuous Deployment

Cloudflare Pages automatically deploys your documentation when you push changes to the main branch. You can also set up preview deployments for pull requests.

### Preview Deployments

Preview deployments are automatically created for pull requests. To enable this:

1. Go to your Pages project in the Cloudflare Dashboard
2. Click on "Settings"
3. Under "Builds & deployments", enable "Preview deployments"

## Monitoring Deployments

You can monitor your deployments in the Cloudflare Dashboard:

1. Go to your Pages project
2. Click on "Deployments"
3. View the status of your deployments

## Troubleshooting

If you encounter issues with your deployment:

### Build Failures

1. Check the build logs in the Cloudflare Dashboard
2. Verify that your build command and output directory are correct
3. Make sure all dependencies are properly installed

### Custom Domain Issues

1. Verify that your DNS records are correctly configured
2. Check for SSL/TLS certificate issues
3. Allow time for DNS changes to propagate

### Content Issues

1. Check that your Jekyll configuration is correct
2. Verify that your Markdown files have the correct front matter
3. Test your site locally before deploying

## Local Testing

To test your documentation locally before deploying:

```bash
cd docs
bundle install
bundle exec jekyll serve
```

This will start a local server at http://localhost:4000 where you can preview your documentation.
