#!/bin/bash 
## Download response files

## Download one per epoch for 8M:
curl -L --digest --user vjs@uoregon.edu:bvbc0gOlZHWjykZc --output /Users/vjs/research/treeslandslides/data/response_files/xml/8M_resp.xml "https://service.earthscope.org/ph5ws/station/1/query?net=8M&level=resp"
sleep 10
echo 'downloaded 8M'

## Download one per epoch for 3F:
curl -L --digest --user vjs@uoregon.edu:bvbc0gOlZHWjykZc --output /Users/vjs/research/treeslandslides/data/response_files/xml/3F_resp.xml "https://service.earthscope.org/ph5ws/station/1/query?net=3F&level=resp"

echo 'downloaded 3F'
