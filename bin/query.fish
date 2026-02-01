#!/usr/bin/env fish
# Fetches the root webpage of the webserver on port 8080.

http GET localhost:8080/
http POST localhost:8080/ message=hello
