#!/bin/bash

set -e
set -x

TMP_FILENAME="$(cat /proc/sys/kernel/random/uuid)-$(basename $1)"
OUT_FILENAME="$(basename $1 .tif)-epsg-3857-lzw-tiled.tif"

# Copy TIF to bind mount that maps to ephemeral storage
aws s3 cp --quiet "$1" "/data/$TMP_FILENAME"

# Warp to Web Mercator projection, LZW compression, with tiling enabled
gdalwarp -overwrite -t_srs epsg:3857 -co COMPRESS=LZW -co TILED=YES "/data/$TMP_FILENAME" "/data/$OUT_FILENAME"

# Copy processed TIF back to S3
aws s3 cp --quiet "/data/$OUT_FILENAME" "$(dirname $1)/"

# Clean up
rm "/data/$TMP_FILENAME" "/data/$OUT_FILENAME" 
