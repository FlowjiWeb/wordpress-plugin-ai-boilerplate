#!/bin/bash
#
# Deploy {{PLUGIN_NAME}} to production
#
# Usage: ./scripts/deploy.sh [environment]
# Environment: production (default)

set -e

# Configuration
PLUGIN_DIR="plugin"
BUILD_NAME="{{PLUGIN_SLUG}}.tar.gz"
SSH_KEY="{{SSH_KEY_PATH}}"  # e.g., "$HOME/.ssh/your_ssh_key"
SSH_PORT="{{SSH_PORT}}"     # e.g., "22" or custom port
SSH_USER="{{SSH_USER}}"     # e.g., "username"
SSH_HOST="{{SSH_HOST}}"     # e.g., "ssh.yourserver.com"
REMOTE_PATH="{{REMOTE_PLUGIN_PATH}}"  # e.g., "~/www/yoursite.com/public_html/wp-content/plugins/{{PLUGIN_SLUG}}"

ENVIRONMENT="${1:-production}"

echo "🚀 Deploying {{PLUGIN_NAME}} to $ENVIRONMENT..."

# Verify SSH key exists
if [ ! -f "$SSH_KEY" ]; then
    echo "❌ SSH key not found: $SSH_KEY"
    echo "Configure SSH_KEY in this script or add to your SSH config"
    exit 1
fi

# Build tarball
echo "📦 Building plugin tarball..."
cd "$PLUGIN_DIR"
tar -czf "../$BUILD_NAME" \
    --exclude='AGENTS.md' \
    --exclude='CLAUDE.md' \
    --exclude='README.md' \
    .
cd ..

if [ ! -f "$BUILD_NAME" ]; then
    echo "❌ Build failed: $BUILD_NAME not created"
    exit 1
fi

echo "✅ Build complete: $BUILD_NAME"

# Upload to server
echo "📤 Uploading to $ENVIRONMENT..."
scp -i "$SSH_KEY" -P "$SSH_PORT" \
    "$BUILD_NAME" \
    "$SSH_USER@$SSH_HOST":~/

if [ $? -ne 0 ]; then
    echo "❌ Upload failed"
    rm "$BUILD_NAME"
    exit 1
fi

echo "✅ Upload complete"

# Extract on server
echo "🔧 Extracting on server..."
ssh -i "$SSH_KEY" -p "$SSH_PORT" \
    "$SSH_USER@$SSH_HOST" \
    "cd $REMOTE_PATH && \
     tar -xzf ~/$BUILD_NAME && \
     rm ~/$BUILD_NAME"

if [ $? -ne 0 ]; then
    echo "❌ Extraction failed"
    rm "$BUILD_NAME"
    exit 1
fi

echo "✅ Extraction complete"

# Cleanup local build
rm "$BUILD_NAME"
echo "🧹 Cleaned up local build artifact"

echo "✅ Deployment to $ENVIRONMENT complete!"
echo ""
echo "ℹ️  Verify deployment at:"
echo "   {{WORDPRESS_ADMIN_URL}}"
