#!/bin/bash

if [ ! -f "package.json" ]; then
    echo '{
        "name": "hugo-site",
        "version": "1.0.0",
        "dependencies": {
            "autoprefixer": "10.4.14",
            "postcss": "8.4.21",
            "postcss-cli": "10.1.0"
        }
    }' > package.json
fi

if [ ! -f "postcss.config.js" ]; then
    echo 'module.exports = {
        plugins: [
            require("autoprefixer")
        ]
    }' > postcss.config.js
fi

npm install

# Run hugo with all arguments
hugo "$@" 