#!/usr/bin/env python3
from argparse import ArgumentParser
import requests

zerotier_base_url = 'https://my.zerotier.com/api/v1'
hetzner_base_url = "https://dns.hetzner.com/api/v1"

def get_clients(zt_token, zt_network_id):
    headers = {"Authorization": f'bearer {zt_token}'}
    url = zerotier_base_url + f'/network/{zt_network_id}/member'
    r = requests.get(url, headers=headers)
    if r.status_code <= 399:
        return [e for e in r.json() if e['config']['authorized'] and not e['hidden'] and len(e['config']['ipAssignments']) >= 1]

def configure_dns(clients, hetzner_zone_id, hetzner_token, delete=False):

    headers = {'Auth-API-Token': hetzner_token}
    records_url = hetzner_base_url + f'/records?zone_id={hetzner_zone_id}'
    record_id_url = hetzner_base_url + '/records/{record_id}'
    record_post_url = hetzner_base_url + '/records'

    r = requests.get(records_url, headers=headers)
    if r.status_code <= 399:
        existing_records = { e['name']: {'value': e['value'], 'id': e['id']} for e in r.json()['records'] if e['type'] == 'A' }
        client_names = list()

        for client in clients:
            client_name = f"{client['name']}.zt"
            client_names.append(client_name)
            client_ip = client['config']['ipAssignments'][0]

            payload = {
                "zone_id": hetzner_zone_id,
                "type": "A",
                "name": client_name,
                "value": client_ip,
                "ttl": 60
            }

            if client_name in existing_records:
                if client_ip != existing_records[client_name]['value']:
                    print(f'updating ip for {client_name}')
                    r = requests.put(record_id_url.format(record_id=existing_records[client_name]['id']), headers=headers, json=payload)
                else:
                    print(f'{client_name} already has {client_ip}')
            else:
                print(f'posting new ip {client_ip} for {client_name}')
                r = requests.post(url=record_post_url, headers=headers, json=payload)
        if delete:
            for record in existing_records.keys():
                if record.endswith('.zt') and record not in client_names:
                    requests.delete(url=record_id_url.format(record_id=existing_records[record]['id']), headers=headers)
                    print(f'deleted {record}, it was not found in zerotier anymore')
    else:
        return

def main():
    parser = ArgumentParser()
    parser.add_argument('--zerotier-token', '--ztt', dest='zt_token', required=True, help="Zerotier access token")
    parser.add_argument('--zerotier-network-id', '--ztni', dest='zt_network_id', required=True, help="Zerotier network id")
    parser.add_argument('--hetzner-token', '--ht', dest='hetzner_token', required=True, help="Hetzner api token")
    parser.add_argument('--hetzner-zone-id', '--hzi', dest='hetzner_zone_id', required=True, help="Hetzner zone id")
    parser.add_argument('--delete', '-d', action='store_true', help="sets flag to delete non existing entries")
    args = parser.parse_args()

    clients = get_clients(args.zt_token, args.zt_network_id)
    configure_dns(clients, args.hetzner_zone_id, args.hetzner_token, delete=args.delete)

if __name__ == '__main__':
    main()