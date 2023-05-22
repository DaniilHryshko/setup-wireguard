sudo apt update && apt upgrade -y

#Ставим Wireguard:
sudo apt install -y wireguard
sudo wg genkey | tee /etc/wireguard/privatekey | wg pubkey | tee /etc/wireguard/publickey
chmod 600 /etc/wireguard/privatekey
for element in Alpha Beta Gamma Delta Epsilon Zeta Eta
do
mkdir /etc/wireguard/$element/
wg genkey | tee /etc/wireguard/$element/privatekey | wg pubkey | tee /etc/wireguard/$element/publickey
done
mkdir /root/setup-wireguard/client
sudo ufw allow 51850
sudo apt-get -y install python3-pip
sudo pip3 install -r requirements.txt
python3 main.py

echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf
sysctl -p

systemctl enable wg-quick@wg0.service
systemctl start wg-quick@wg0.service
systemctl status wg-quick@wg0.service

