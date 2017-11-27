#!/bin/bash
service redis_6379 start
service mongod start

pip  install -r requirements.txt

cd houses_pipeline
python houses_monitor.py &
python houses_fetcher.py &

echo "========================================="
read -p "PRESS [ENTER] TO TERMINATE PROCESSES." PRESSKEY

kill $(jobs -p)