# Hugo configuration
OUTPUT_DIR := output
DOCKER_IMAGE := hvishwanath/hugo:v0.123.7-ext
#PROD_IMAGE := hvishwanath/kafka-site-md:1.2.0
PROD_IMAGE := us-west1-docker.pkg.dev/play-394201/kafka-site-md/kafka-site-md:1.6.0

.PHONY: build serve clean docker-image prod-image prod-run buildx-setup

# Setup buildx for multi-arch builds
buildx-setup:
	docker buildx create --name multiarch --driver docker-container --use || true
	docker buildx inspect multiarch --bootstrap

# Build the Docker image
docker-image:
	docker build -t $(DOCKER_IMAGE) . --push

# Build the static site using Docker
build: 
	docker pull $(DOCKER_IMAGE)
	docker run --rm -v $(PWD):/src $(DOCKER_IMAGE) \
		--minify \
		--destination $(OUTPUT_DIR)

# Serve the site locally using Docker (development)
serve: 
	docker pull $(DOCKER_IMAGE)
	docker run --rm -it -v $(PWD):/src -p 1313:1313 $(DOCKER_IMAGE) \
		server \
		--bind 0.0.0.0 \
		--destination $(OUTPUT_DIR) \
		--baseURL http://localhost:1313/ \
		--appendPort=true \
		--buildDrafts \
		--buildFuture

# Build production Nginx image for multiple architectures
prod-image: build buildx-setup
	docker buildx build \
		--platform linux/amd64,linux/arm64 \
		--tag $(PROD_IMAGE) \
		--file Dockerfile.prod \
		--push \
		.

# Run production image locally
prod-run: prod-image
	docker pull $(PROD_IMAGE)
	docker run --rm -p 8080:80 $(PROD_IMAGE)

# Clean the output directory and remove Docker images
clean:
	rm -rf $(OUTPUT_DIR)
	docker rmi $(DOCKER_IMAGE) $(PROD_IMAGE)
	docker buildx rm multiarch || true
