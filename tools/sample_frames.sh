#!/usr/bin/env bash
# Usage: sample_frames.sh VIDEO OUT_DIR [FPS]   -- samples FPS frames/second as JPEG, max width 1920
set -euo pipefail
v="$1"; out="$2"; fps="${3:-1}"
mkdir -p "$out"
ffmpeg -hide_banner -loglevel error -i "$v" -vf "fps=$fps,scale='min(1920,iw)':-2" -q:v 3 "$out/%06d.jpg"
ls "$out" | wc -l
