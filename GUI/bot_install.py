log = "FALSE"
verb = "TRUE"
bot_version = "1.0 (22-03-2022)"

bot_name = "VPNBot"
arc_name = "VPNBot.zip"

bot_install_commands = f"""
apt-get update
apt-get dist-upgrade -y
apt-get install python3.9 -y
apt-get install python3-pip -y
apt-get install python3.9-dev -y
apt-get install python3.9-venv -y
apt-get install python3-dotenv -y
apt-get install gcc -y
apt-get install zip unzip -y
apt-get install vnstat -y
if [[ -e /lib/systemd/system/{bot_name.lower()}.service || $(service {bot_name.lower()} status | grep -w active)  ]]
then
systemctl stop {bot_name.lower()}.service
systemctl disable {bot_name.lower()}.service
rm -rf /root/{bot_name}
rm /lib/systemd/system/{bot_name.lower()}.service
systemctl daemon-reload
fi
unzip /root/{arc_name}
mkdir /etc/vpn_handler
mv /root/vpn_handler /etc/vpn_handler/
chmod +x /etc/vpn_handler/vpn_handler
/etc/vpn_handler/vpn_handler scheduler install
rm /root/{arc_name}
python3.9 -m pip install -r /root/{bot_name}/requirements.txt
cd ~/ || exit 1
touch /lib/systemd/system/{bot_name.lower()}.service
cat > /lib/systemd/system/{bot_name.lower()}.service <<EOF
[Unit]
Description={bot_name} {bot_version}
After=network.target
[Service]
Type=simple
ExecStart=python3.9 /root/{bot_name}/app.py
Restart=on-failure
[Install]
WantedBy=multi-user.target
EOF
chmod 644 /lib/systemd/system/{bot_name.lower()}.service
systemctl daemon-reload
systemctl enable {bot_name.lower()}.service
systemctl stop {bot_name.lower()}.service
"""
