# GitHub Actions Workflows

## Active Workflows

### 🌐 Deploy GHOSTCORE Portal to GitHub Pages (`deploy-pwa.yml`)

This workflow builds and deploys the VES GHOSTCORE Portal as a Progressive Web App (PWA) to GitHub Pages.

**Triggers:**
- Push to `main` branch
- Manual dispatch via GitHub Actions UI

**What it does:**
1. Checks out the repository
2. Sets up Node.js 20
3. Installs dependencies with `npm ci`
4. Builds the PWA using Vite Pages mode (`npm run build:pages`)
5. Creates `.nojekyll` file to disable Jekyll processing
6. Uploads the `dist` folder as a Pages artifact
7. Deploys to GitHub Pages

**Requirements:**
- GitHub Pages must be enabled in repository settings
- Pages deployment source should be set to "GitHub Actions"

## Disabled Workflows

### 🜂 Ghost Breathe - Living System (`workflows_DISABLED/ghost-breathe.yml`)

Currently disabled. This workflow has scheduled tasks and automated commits that need review and fixes before enabling.

## Previous Issues

The repository had conflicting deployment workflows in the past; now Pages deploy is consolidated to one workflow:
- `jekyll-gh-pages.yml` - Jekyll-based deployment (removed)
- `static.yml` - Static file deployment (removed)
- `deploy-pwa.yml` - Vite/PWA deployment (active)

All three workflows used the same concurrency group (`"pages"`), which meant they would queue and conflict with each other during deployment. Additionally, only the PWA deployment workflow was appropriate for this Vite-based project structure.

These conflicts caused deployment failures. The solution was to:
1. Remove the Jekyll and static deployment workflows
2. Keep only the PWA deployment workflow (which matches the project structure)
3. Fix YAML formatting issues

## Testing

To test the build locally:
```bash
npm ci
npm run build
```

The built files will be in the `dist/` directory.
