import wgconfig.wgexec as wgexec
import requests

server_pair_key = wgexec.generate_keypair()
external_ip = requests.get("https://ifconfig.me/ip").text
server_public_key = open('/etc/wireguard/publickey').read().strip()
server_private_key = open('/etc/wireguard/privatekey').read().strip()

wb_conf = f'''
[Interface]
PrivateKey = {server_private_key}
Address = 10.0.0.1/24
ListenPort = 51850
PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
'''

ip_ch = 2

for client in ["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta"]:
    client_public_key = open(f'/etc/wireguard/{client}/publickey').read().strip()
    client_private_key = open(f'/etc/wireguard/{client}/privatekey').read().strip()
    peer_to_server = f'''

[Peer]
PublicKey = {client_public_key}
AllowedIPs = 10.0.0.{ip_ch}/32 

'''
    wb_conf += peer_to_server

    peer_to_client = f'''
    [Interface]
    PrivateKey = {client_private_key}
    Address = 10.0.0.{ip_ch}/32
    DNS = 8.8.8.8
    MTU = 1500

    [Peer]
    PublicKey = {server_public_key}
    Endpoint = {external_ip}:51850
    AllowedIPs = 0.0.0.0/0
    PersistentKeepalive = 15
    '''

    key_for_client = open(f"/root/setup-wireguard/client/{client}.conf", "w").write(peer_to_client)
    ip_ch += 1

server_conf = open('/etc/wireguard/wg0.conf', "w").write(wb_conf)
