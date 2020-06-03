
#! /usr/bin/bash

# docker build -t jeff-plots:latest .
docker run -v $(pwd):/usr/local/app jeff-plots:latest
