#!/bin/bash
set -e

mongosh <<EOF
use admin

use videoMetadataDb
db.createCollection("video_frames", { capped: false });
EOF