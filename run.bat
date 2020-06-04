docker build -t jeff-plots .
docker run -v %CD%:/usr/local/app jeff-plots:latest
