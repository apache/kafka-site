# Apache Kafka Website
 
This `markdown` branch is used to hold the top-level documentation for the Apache Kafka website https://kafka.apache.org

# Building the website

This repository contains a Hugo-based static site with Docker support for both development and production environments. It includes multi-architecture build support for production deployments.

## Prerequisites

- Docker (20.10.0 or newer)
- Make
- Docker Hub account (for pushing images)

## Development

### Local Development Server

To start the local development server with hot-reload:

```bash
make serve
```

This will:
- Build the Hugo Docker image
- Start a development server on http://localhost:1313
- Watch for changes and automatically rebuild
- Enable drafts and future posts

### Building the Site Locally

To build the site without starting the server:

```bash
make build
```

The built site will be available in the `output` directory.

## Production

### Setting up Multi-architecture Builds

Before building production images, ensure your Docker installation is set up for multi-architecture builds:

1. Enable Docker experimental features (if not already enabled):
   ```bash
   # Add to ~/.docker/config.json
   {
     "experimental": "enabled"
   }
   ```

2. Install QEMU for multi-architecture support:
   ```bash
   docker run --privileged --rm tonistiigi/binfmt --install all
   ```

### Building Production Images

The production setup uses Nginx to serve the static files and supports both ARM64 and AMD64 architectures.

To build and push the production image:

```bash
make prod-image
```

This will:
- Build the Hugo site
- Create a multi-architecture Nginx image (ARM64 and AMD64)
- Push the image to Docker Hub

### Testing Production Image Locally

To test the production image locally:

```bash
make prod-run
```

The site will be available at http://localhost:8080

## Configuration

### Environment Variables

The following variables can be configured in the Makefile:

- `OUTPUT_DIR`: Directory for built files (default: `output`)
- `DOCKER_IMAGE`: Hugo builder image name
- `PROD_IMAGE`: Production Nginx image name

### Nginx Configuration

The Nginx configuration is located in `scripts/nginx.conf` and includes:
- Gzip compression
- Cache control headers
- Security headers
- Static file optimizations

## Cleaning Up

To clean up built files and Docker images:

```bash
make clean
```

This will:
- Remove the `output` directory
- Remove Docker images
- Clean up buildx builder instance

## Directory Structure

```
.
├── Dockerfile          # Hugo builder Dockerfile
├── Dockerfile.prod     # Production Nginx Dockerfile
├── Makefile           # Build automation
├── scripts/
│   └── nginx.conf     # Nginx configuration
└── content/           # Hugo content files
```
