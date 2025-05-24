FROM ubuntu:22.04 AS builder

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Install Go and build dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Go
RUN curl -OL https://go.dev/dl/go1.22.2.linux-arm64.tar.gz && \
    tar -C /usr/local -xzf go1.22.2.linux-arm64.tar.gz && \
    rm go1.22.2.linux-arm64.tar.gz

# Set Go environment variables
ENV PATH="/usr/local/go/bin:${PATH}"
ENV GOPATH="/go"
ENV PATH="${GOPATH}/bin:${PATH}"

# Install Hugo
RUN go install -tags extended github.com/gohugoio/hugo@v0.123.7

FROM ubuntu:22.04

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Install Node.js, npm and other dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g npm@latest \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy Go from builder
COPY --from=builder /usr/local/go /usr/local/go

# Set Go environment variables
ENV PATH="/usr/local/go/bin:${PATH}"
ENV GOPATH="/go"
ENV PATH="${GOPATH}/bin:${PATH}"

# Create working directory
WORKDIR /src

# Copy Hugo from builder
COPY --from=builder /go/bin/hugo /usr/local/bin/hugo

# Install global dependencies
RUN npm install -g postcss postcss-cli autoprefixer

# Copy entrypoint script
COPY scripts/entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

# Verify installations
RUN node --version && \
    npm --version && \
    npx --version && \
    hugo version && \
    go version

EXPOSE 1313

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"] 