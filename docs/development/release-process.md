---
title: Release Process
description: Learn about the release process for the Unraid API
---

# Release Process

This document outlines the process for releasing new versions of the Unraid API package.

## Versioning

The Unraid API follows [Semantic Versioning](https://semver.org/) (SemVer):

- **Major version** (X.0.0): Incompatible API changes
- **Minor version** (0.X.0): New functionality in a backward-compatible manner
- **Patch version** (0.0.X): Backward-compatible bug fixes

## Release Checklist

Before starting the release process, ensure:

1. All planned features for the release are completed
2. All tests are passing
3. Documentation is updated to reflect new features or changes
4. Changelog is updated with all significant changes
5. Any breaking changes are clearly documented

## Release Process Steps

### 1. Prepare the Release

```bash
# Ensure you're on the main branch with latest changes
git checkout main
git pull origin main

# Create a release branch
git checkout -b release/vX.Y.Z
```

### 2. Update Version

Update the version number in:

- `setup.py`
- `unraid_api/__init__.py`
- Any other relevant files that contain version information

### 3. Update Changelog

Ensure the `CHANGELOG.md` file is updated with all significant changes:

- New features
- Bug fixes
- Performance improvements
- Breaking changes
- Deprecations

Format the changelog entry like:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New feature 1
- New feature 2

### Changed
- Change 1
- Change 2

### Fixed
- Bug fix 1
- Bug fix 2

### Deprecated
- Deprecated feature 1

### Removed
- Removed feature 1
```

### 4. Create Pull Request

```bash
# Commit the changes
git add .
git commit -m "Prepare release vX.Y.Z"

# Push the branch
git push origin release/vX.Y.Z
```

Create a pull request from `release/vX.Y.Z` to `main` on GitHub.

### 5. Review and Testing

Before merging:

- Ensure CI/CD pipelines pass
- Conduct a final code review
- Run any manual tests if necessary
- Verify documentation is accurate

### 6. Merge and Tag

Once approved:

1. Merge the pull request into `main`
2. Pull the latest changes to your local repository:

```bash
git checkout main
git pull origin main
```

3. Create and push a Git tag:

```bash
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin vX.Y.Z
```

### 7. Build and Publish

#### Building the Package

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build the package
python -m build
```

#### Publishing to PyPI

```bash
# Upload to PyPI
python -m twine upload dist/*
```

#### Publishing to GitHub Releases

Create a new release on GitHub:

1. Go to the "Releases" section of your GitHub repository
2. Click "Draft a new release"
3. Select the tag you just created
4. Title the release "vX.Y.Z"
5. Copy the relevant section from `CHANGELOG.md` into the description
6. Attach the built distribution files
7. Publish the release

## Post-Release Process

### 1. Update Development Version

After releasing, update the version in the main branch to the next development version:

```bash
# Update version in relevant files to X.Y.(Z+1)-dev
git checkout main
# Edit files to increment version
git add .
git commit -m "Bump version to X.Y.(Z+1)-dev"
git push origin main
```

### 2. Announce the Release

Announce the new release on:

- Project README
- Documentation site
- Community forums
- Social media channels

### 3. Monitor for Issues

After a release:

- Monitor for any issues reported by users
- Be prepared to make hotfix releases if critical issues are found

## Hotfix Process

For critical issues that need immediate fixing:

1. Create a hotfix branch from the release tag:

```bash
git checkout vX.Y.Z
git checkout -b hotfix/vX.Y.Z+1
```

2. Fix the issue and commit the changes
3. Update version numbers to X.Y.(Z+1)
4. Update the changelog
5. Create a pull request, get it reviewed and merged
6. Tag and release as described in steps 6-7 above

## Release Candidates

For major releases, consider using release candidates:

1. Follow the release process, but version as `X.Y.Z-rc1`, `X.Y.Z-rc2`, etc.
2. Publish release candidates to PyPI and GitHub
3. Gather feedback and fix issues in subsequent release candidates
4. When stable, release the final version

## Release Automation

The project uses GitHub Actions for automating parts of the release process:

- Running tests on all PRs
- Building and publishing to PyPI when a new tag is pushed
- Generating release notes

## Release Schedule

- **Patch releases**: As needed for bug fixes
- **Minor releases**: Approximately every 1-2 months
- **Major releases**: As needed for significant changes, with advance notice

## Planning Future Releases

Feature planning and roadmap discussions happen in:

- GitHub issues labeled with "feature"
- Regular planning meetings
- Community feedback forums

## Rolling Back a Release

If a critical issue is found in a release and a hotfix isn't immediately possible:

1. Add a warning to the documentation
2. Consider yanking the release from PyPI:

```bash
pip install twine
twine delete unraid-api==X.Y.Z
```

3. Post clear instructions for users about downgrading to the previous version

## Version Support Policy

- Latest major version: Full support for features and bug fixes
- Previous major version: Bug fixes only for 6 months
- Older versions: No support 