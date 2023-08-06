#!/usr/bin/env sh

aws-spitzel 's3:List' --last-minute 300 \
| \
python3 samples/splunk-integration/generic-wrapper.py \
| \
while read -r line; do

    curl https://localhost:8088/services/collector \
        --insecure \
        -H "Authorization: Splunk $HEC_TOKEN" -d "$line" \
    &
done

wait