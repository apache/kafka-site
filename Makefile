# Hugo configuration
OUTPUT_DIR := output
HUGO_VERSION := 0.123.7
HUGO_BASE_IMAGE := ghcr.io/apache/kafka-site/hugo:v$(HUGO_VERSION)-ext-multiplatform
DOCKER_IMAGE := $(HUGO_BASE_IMAGE)

.PHONY: build serve clean docker-image ensure-hugo-image hugo-base-multi-platform buildx-setup ghcr-prod-image

# Setup buildx for multi-arch builds
buildx-setup:
	docker buildx create --name multiarch --driver docker-container --use || true
	docker buildx inspect multiarch --bootstrap

# Build the Docker image (single platform)
docker-image:
	docker build -t $(DOCKER_IMAGE) . --push

# Build and push multi-platform Hugo base image
hugo-base-multi-platform: buildx-setup
	docker buildx build \
		--platform linux/amd64,linux/arm64 \
		--tag $(HUGO_BASE_IMAGE) \
		--file Dockerfile.multiplatform \
		--build-arg BUILDKIT_INLINE_CACHE=1 \
		--push \
		.

# Pull the published Apache-owned Hugo image, or build it locally if it is not
# available yet (useful for first-time bootstrapping and PR validation).
ensure-hugo-image:
	docker pull $(DOCKER_IMAGE) || docker build -t $(DOCKER_IMAGE) -f Dockerfile.multiplatform .

# Build the static site using Docker
build: ensure-hugo-image
	docker run --rm -v $(PWD):/src $(DOCKER_IMAGE) \
		--minify \
		--destination $(OUTPUT_DIR)

# Serve the site locally using Docker (development)
serve: ensure-hugo-image
	docker run --rm -it -v $(PWD):/src -p 1313:1313 $(DOCKER_IMAGE) \
		server \
		--bind 0.0.0.0 \
		--destination $(OUTPUT_DIR) \
		--baseURL http://localhost:1313/ \
		--appendPort=true \
		--buildDrafts \
		--buildFuture

# Build and push production image to GHCR
ghcr-prod-image: build buildx-setup
	docker buildx build \
		--platform linux/amd64,linux/arm64 \
		--tag ghcr.io/$(shell basename $(shell git rev-parse --show-toplevel))/kafka-site-md:prod-$(shell git rev-parse --abbrev-ref HEAD) \
		--tag ghcr.io/$(shell basename $(shell git rev-parse --show-toplevel))/kafka-site-md:prod-$(shell git rev-parse --short HEAD) \
		--tag ghcr.io/$(shell basename $(shell git rev-parse --show-toplevel))/kafka-site-md:prod-$(shell date +%Y%m%d-%H%M%S) \
		--file Dockerfile.prod \
		--push \
		.

# Clean the output directory and remove Docker images
clean:
	rm -rf $(OUTPUT_DIR)
	docker rmi $(DOCKER_IMAGE) $(HUGO_BASE_IMAGE)
	docker buildx rm multiarch || true
