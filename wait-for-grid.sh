#!/bin/bash
# wait-for-grid.sh

set -e
echo Trying grid $GRID_HUB/status
while ! curl -sSL "$GRID_HUB/status" 2>&1 \
        | jq -r '.value.ready' 2>&1 | grep "true" >/dev/null; do
    echo Waiting for the Grid $GRID_HUB/status
    sleep 1
done

>&2 echo Selenium Grid $GRID_HUB is up.