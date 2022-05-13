#!/usr/bin/env bash

set -euxo pipefail

docker build -t kafka-site-preview .

docker run -it --rm --name mypreview -p 8080:80 -v "$PWD":/usr/local/apache2/htdocs/ kafka-site-preview
