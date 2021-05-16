#!/bin/bash
# this script compresses videos in directory
for FILE in *; 
do  
    BASENAME=$(basename "$FILE"); 
    echo "--------- converting --------" $BASENAME
    ffmpeg -i "$FILE" -vcodec libx265 -crf 28 "$BASENAME.mp4"
done
