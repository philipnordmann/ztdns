# ZEROTIER DNS UPDATER
## Introduction
This project aims to update the hetzner dns api with the zerotier ip addresses so they are resolvable via DNS.

Currently only Hetzner as DNS provider is supported.

Addresses will be the name of your zerotier client with the postfix .zt and your dns entry e.g. foo.zt.bar.com

New records will be created, existing ones will only be updated. The script also allows you to remove records if the corresponding client where deleted.

## Using the script
You can use the script by just calling it directly with python.
To do so you have to have the requirements installed.

You can do this with `pip install -r requirements.txt`

Afterwads you have to define a few command line parameters, so you can authorize and configure the correct network and zone id.

see the usage:

```
usage: ztdns.py [-h] --zerotier-token ZT_TOKEN --zerotier-network-id ZT_NETWORK_ID --hetzner-token HETZNER_TOKEN --hetzner-zone-id HETZNER_ZONE_ID [--delete]

optional arguments:
  -h, --help            show this help message and exit
  --zerotier-token ZT_TOKEN, --ztt ZT_TOKEN
                        Zerotier access token
  --zerotier-network-id ZT_NETWORK_ID, --ztni ZT_NETWORK_ID
                        Zerotier network id
  --hetzner-token HETZNER_TOKEN, --ht HETZNER_TOKEN
                        Hetzner api token
  --hetzner-zone-id HETZNER_ZONE_ID, --hzi HETZNER_ZONE_ID
                        Hetzner zone id
  --delete, -d          sets flag to delete non existing entries
```

## Using the docker image
If you would like to just have a docker image running, that updates your records on a regular basis, there is an image available at `ghcr.io/philipnordmann/ztdns`.

This image will update your records every 60 seconds. Beware that the contianer will always have the `--delete` flag enabled.

To use the image either create a container like this:

```
docker run -d \
    --name=ztdns \
    -e ZEROTIER_TOKEN=<your zerotier api token> \
    -e ZEROTIER_NETWORK_ID=<your zerotier network id> \
    -e HETZNER_TOKEN=<your hetzner api token> \
    -e HETZNER_ZONE_ID=<your hertzner dns zone id> \
    ghcr.io/philipnordmann/ztdns:latest
```

or use a compose file like this:
```yaml
version: "3.3"
services:
  ztdns:
    image: ghcr.io/philipnordmann/ztdns:latest
    environment:
      - ZEROTIER_TOKEN=<your zerotier api token>
      - ZEROTIER_NETWORK_ID=<your zerotier network id>
      - HETZNER_TOKEN=<your hetzner api token>
      - HETZNER_ZONE_ID=<your hertzner dns zone id>
    restart: unless-stopped
```

### Tweaks
You can override the 60 second update rate by setting the environment variable `UPDATE_RATE` to the value you need in seconds.