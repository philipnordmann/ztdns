#!/bin/sh

while true; do
    /opt/ztdns/ztdns.py \
        --delete \
        --zerotier-token ${ZEROTIER_TOKEN} \
        --zerotier-network-id ${ZEROTIER_NETWORK_ID} \
        --hetzner-token ${HETZNER_TOKEN} \
        --hetzner-zone-id ${HETZNER_ZONE_ID}
    sleep ${UPDATE_RATE:-60}
done