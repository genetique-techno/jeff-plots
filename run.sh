
#! /usr/bin/bash

docker build -t jeff-plots:latest .
docker run -v $(pwd)/data:/usr/local/app/data jeff-plots:latest
