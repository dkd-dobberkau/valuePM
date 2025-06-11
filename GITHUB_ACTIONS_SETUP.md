# GitHub Actions Setup Instructions

## Issue
The GitHub Actions workflow file `.github/workflows/ui-documentation.yml` cannot be pushed via OAuth app due to security restrictions. It requires manual addition by a repository admin.

## Solution
Repository admins should manually add the workflow file to enable automated UI documentation:

### Step 1: Enable GitHub Actions
1. Go to repository Settings → Actions → General
2. Enable "Allow all actions and reusable workflows" or configure as needed

### Step 2: Add the Workflow File
Create `.github/workflows/ui-documentation.yml` with the following content:

```yaml
# Copy the content from the local file:
# .github/workflows/ui-documentation.yml
```

Or copy the file directly from the local repository after cloning.

### Step 3: Verify Setup
1. Commit any change to `src/ui/` or `src/api/` directories
2. Check Actions tab to see if workflow runs
3. Review artifacts and GitHub Pages deployment

## What This Workflow Does
- Automatically generates UI screenshots when UI code changes
- Creates comprehensive documentation with embedded images
- Performs visual regression testing
- Deploys documentation to GitHub Pages
- Comments on PRs with documentation previews

## Manual Alternative
If GitHub Actions cannot be used, run locally:
```bash
make ui-docs        # Generate UI documentation
make visual-test    # Run visual regression tests
```

## Files Affected
- `.github/workflows/ui-documentation.yml` - Main workflow
- `scripts/generate_ui_docs.py` - Screenshot generator
- `scripts/visual_regression_test.py` - Visual testing
- `docs/ui/` - Generated documentation output
- 