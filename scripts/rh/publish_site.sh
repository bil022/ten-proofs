#!/usr/bin/env bash
# Copy the explorer website into a clone of bil022/riemann-explorer, which
# GitHub Pages publishes at https://bil022.github.io/riemann-explorer/.
#
# Usage: scripts/rh/publish_site.sh <riemann-explorer clone>
# Then commit and push in that clone. Its own README.md and .nojekyll are kept.
set -euo pipefail
dest=$(cd "$1" && pwd)
cd "$(dirname "$0")"
rsync -a --delete --exclude=.git --exclude=README.md --exclude=.nojekyll site/ "$dest/"
git -C "$dest" status --short | tail -5
