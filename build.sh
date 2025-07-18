#!/bin/bash

# Build script for Bioinformatics Programs Suite
set -e

# Get build metadata
BUILD_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
VCS_REF=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
VERSION=${VERSION:-1.2.0}

echo "Building Bioinformatics Programs Suite Docker images..."
echo "Build Date: $BUILD_DATE"
echo "VCS Ref: $VCS_REF"
echo "Version: $VERSION"

# Check if Docker buildx is available
if ! docker buildx version > /dev/null 2>&1; then
    echo "Docker buildx not found. Creating builder instance..."
    docker buildx create --use --name multiarch
fi

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
echo ""
echo "Usage examples:"
echo "  docker run -v \$(pwd):/work wilke/cryptic-screening:latest"
echo "  docker run -v \$(pwd):/work wilke/cryptic-screening:latest SRA_fetch.py"
echo "  docker run -v \$(pwd):/work wilke/cryptic-screening:latest Workflow.sh"