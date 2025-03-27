# Publishing to PyPI via GitHub Actions

This repository is set up to automatically publish to PyPI when a new release is created on GitHub. This document explains how to create releases and how the trusted publisher integration works.

## Trusted Publisher Integration

This project uses PyPI's OpenID Connect (OIDC) integration with GitHub Actions. This means:

- No need to store API tokens in GitHub secrets
- More secure publishing workflow
- Authentication is handled automatically via OIDC

The integration has already been set up with the following parameters:
- PyPI Project Name: `unraid-api`
- GitHub Owner: `domalab`
- Repository name: `unraid-api`
- Workflow name: `publish.yml`

## Creating a Release

To trigger a new package release:

1. Update the version number in `setup.py`
2. Commit and push your changes
3. Go to the GitHub repository web interface
4. Click on "Releases" in the right sidebar
5. Click "Draft a new release"
6. Create a new tag with the format `v{version}` (e.g., `v0.1.2`)
7. Set the release title (usually the same as the tag)
8. Add release notes describing the changes
9. Click "Publish release"

The GitHub Action will automatically:
1. Build the package
2. Authenticate with PyPI using OIDC
3. Upload the package to PyPI
4. The new version will be available via `pip install unraid-api`

## Manual Release (if needed)

If you need to publish manually:

```bash
# Install build tools
pip install build twine

# Build the package
python -m build

# Upload to PyPI (requires PyPI API token)
twine upload dist/* --username __token__ --password your_token_here
```

## Checking Release Status

1. Visit the "Actions" tab in your GitHub repository to see the status of the workflow
2. Check on PyPI: https://pypi.org/project/unraid-api/ 