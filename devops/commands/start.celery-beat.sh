#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

celery -A app beat -l $CELERY_BEAT_LOG_LEVEL
