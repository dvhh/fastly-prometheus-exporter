#!/bin/bash
set -euxo pipefail

python3 endpoint.py &
while true
do
	# collect and format metrics
	python3 collect_rt_metrics.py -j 10 "${FASTLY_API_KEY}" | python3 formatter.py --input entries - --input config metrics_list.json> output.txt
	# pre-generate compressed metrics
	gzip -9kf output.txt
	rm -f metrics.txt && rm -f metrics.txt.gz && mv output.txt metrics.txt && mv output.txt.gz metrics.txt.gz
	sleep 15
done
