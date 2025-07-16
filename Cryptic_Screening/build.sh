#!/bin/bash

# Build script with metadata and provenance
set -e

# Get build metadata
BUILD_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
VCS_REF=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
VERSION=${VERSION:-1.1.0}

echo "Building Cryptic Screening Docker images..."
echo "Build Date: $BUILD_DATE"
echo "VCS Ref: $VCS_REF"
echo "Version: $VERSION"
echo "Note: Original code by degregory, Dockerfile by Andreas Wilke and Claude"

# Build single-platform images with metadata
echo "Building AMD64 image..."
docker buildx build \
    --platform linux/amd64 \
    --build-arg BUILD_DATE="$BUILD_DATE" \
    --build-arg VCS_REF="$VCS_REF" \
    --build-arg VERSION="$VERSION" \
    -t wilke/cryptic-screening:amd64 \
    --load \
    .

echo "Building ARM64 image..."
docker buildx build \
    --platform linux/arm64 \
    --build-arg BUILD_DATE="$BUILD_DATE" \
    --build-arg VCS_REF="$VCS_REF" \
    --build-arg VERSION="$VERSION" \
    -t wilke/cryptic-screening:arm64 \
    --load \
    .

# Build and push multi-platform manifest
echo "Building and pushing multi-platform manifest..."
docker buildx build \
    --platform linux/amd64,linux/arm64 \
    --build-arg BUILD_DATE="$BUILD_DATE" \
    --build-arg VCS_REF="$VCS_REF" \
    --build-arg VERSION="$VERSION" \
    -t wilke/cryptic-screening:latest \
    -t wilke/cryptic-screening:$VERSION \
    --push \
    .

echo "Build completed successfully!"
echo "Images created and pushed:"
echo "  - wilke/cryptic-screening:amd64 (Intel/AMD64)"
echo "  - wilke/cryptic-screening:arm64 (Apple Silicon/ARM64)"
echo "  - wilke/cryptic-screening:latest (multi-platform manifest)"
echo "  - wilke/cryptic-screening:$VERSION (versioned multi-platform manifest)"