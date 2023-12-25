#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

celery -A app worker -l $CELERY_LOG_LEVEL -P gevent -c $CELERY_CONCURENCY
