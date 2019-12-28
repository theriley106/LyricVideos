#!/bin/bash
ffmpeg -framerate 30 -i temp/frame%05d.jpg Project.mp4
ffmpeg -i Project.mp4 -i audio.mp3 -c copy -map 0:v:0 -map 1:a:0 final.mp4
mv final.mp4 $1