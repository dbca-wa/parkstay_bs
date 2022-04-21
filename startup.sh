#!/bin/bash

# Start the first process
env > /etc/.cronenv
sed -i 's/\"/\\"/g' /etc/.cronenv

echo "Starting Cron"
service cron start &
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start cron: $status"
  exit $status
fi

echo "Starting Nginx"
service nginx start &
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start nginx: $status"
  exit $status
fi

/bin/bash
