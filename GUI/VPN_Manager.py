import datetime
import os.path

from GUI.ssh import SSH


class ServerStatus:
    connected: bool = False
    handler: bool = False
    openvpn: bool = False
    wireguard: bool = False
    shadowsocks: bool = False
    socks: bool = False


class VPNManager:

    def __init__(self):
        self.server = None
        self.server_status = ServerStatus()
        self.established: bool = False
        self.ip: str = ""
        self.port: int = 0
        self.login: str = ""
        self.passwd: str = ""

    def get_user(self):
        now = datetime.datetime.now()
        delta = (now - datetime.datetime(1970, 1, 1))
        return f"{str(delta.total_seconds()).split('.')[0]}{str(delta.microseconds)[0]}"

    def make_socks_file(self, filename: str):
        with open(filename, 'rt') as file:
            line = file.read().strip()
            user = line.split(":")[0]
            passwd = line.split(":")[-1]

        data = f"Proxy IP: {self.ip}\n" \
               f"Type: SOCKS5" \
               f"Port SOCKS5: 9999\n" \
               f"Port HTTPS: 9100\n" \
               f"Login: {user}\n" \
               f"Password: {passwd}"

        with open(f"{filename}.txt", 'wt') as file:
            file.write(data)

        os.remove(filename)

    async def get_server_status(self):
        if self.server is not None:
            self.server_status.connected = self.server.check_connect()
        else:
            self.server_status.connected = False

        if not self.server_status.connected:
            return ServerStatus()

        handler_check = self.server.shell(cmd='if [[ -e /etc/vpn_handler/vpn_handler ]]; then echo "OK"; fi')
        if handler_check.strip() == "OK":
            self.server_status.handler = True
        else:
            self.server_status.handler = False

        openvpn_check = self.server.shell(cmd='if [[ ! -z $(which openvpn) ]]; then echo "OK"; fi')
        if openvpn_check.strip() == "OK":
            self.server_status.openvpn = True
        else:
            self.server_status.openvpn = False

        wireguard_check = self.server.shell(cmd='if [[ ! -z $(which wg-quick) ]]; then echo "OK"; fi')
        if wireguard_check.strip() == "OK":
            self.server_status.wireguard = True
        else:
            self.server_status.wireguard = False

        shadowsocks_check = self.server.shell(cmd='if [[ ! -z $(which ss-server) ]]; then echo "OK"; fi')
        if shadowsocks_check.strip() == "OK":
            self.server_status.shadowsocks = True
        else:
            self.server_status.shadowsocks = False

        socks_check = self.server.shell(cmd='if [[ ! -z $(which 3proxy) ]]; then echo "OK"; fi')
        if socks_check.strip() == "OK":
            self.server_status.socks = True
        else:
            self.server_status.socks = False

        return self.server_status

    async def connect(self, ip: str = "", port: int = 0, login: str = "", passwd: str = "") -> str:
        if ip != "":
            self.ip = ip

        if port != 0:
            self.port = port

        if login != "":
            self.login = login

        if passwd != "":
            self.passwd = passwd

        result = ""
        if self.server is None or not self.server.established:
            self.server = SSH(ip=self.ip, port=self.port,
                              login=self.login, passwd=self.passwd)
            try:
                result = self.server.connect()
            except Exception as err:
                result = err
                self.server.established = False

            await self.get_server_status()

        return result

    async def disconnect(self) -> str:
        result = ""
        if self.server is not None and self.server.established:
            try:
                result = self.server.close()
            except Exception as err:
                result = err

            await self.get_server_status()

        return result

    async def install_manager(self):
        if self.server is None or not self.server.established:
            result = "???????????????????? ?? ???????????????? ???? ??????????????????????!"
            return result

        install_cmd = """
        wget https://github.com/izhatomic/VPNManager/releases/download/v1.1/vpn_handler
        chmod +x vpn_handler
        mkdir -p /etc/vpn_handler
        mv vpn_handler /etc/vpn_handler/
        /etc/vpn_handler/vpn_handler scheduler install
        apt-get update
        apt-get install vnstat -y
        apt-get install qrencode -y
        """

        try:
            self.server.shell(cmd=install_cmd)
        except Exception as err:
            result = "???????? ?????????????????????? ?? ??????????????!"
        else:
            try:
                check = self.server.shell(cmd="if [[ -e /etc/vpn_handler/vpn_handler ]]; then echo 'OK'; fi")
            except Exception as err:
                result = "???????? ?????????????????????? ?? ??????????????!"
                return result
            else:
                if check.strip() == "OK":
                    result = "VPNManager ????????????????????"
                else:
                    result = "???????????? ?????????????????? VPNManager"

        await self.get_server_status()
        return result

    async def install_service(self, service: str) -> [str, str]:
        if service.lower() not in ["openvpn", "wireguard", "shadowsocks", "socks"]:
            result = "???????????? ???????????????????????? ?????? ??????????????!"
            color = 'color: rgb(255, 0, 0);'
            return result, color

        if self.server is None or not self.server.established:
            result = "???????????????????? ?? ???????????????? ???? ??????????????????????!"
            color = 'color: rgb(255, 0, 0);'
            return result, color

        await self.get_server_status()

        if not self.server_status.handler:
            result = "???????????????? VPN ???? ????????????????????!"
            color = 'color: rgb(255, 0, 0);'
            return result, color
        else:
            try:
                self.server.shell(cmd=f"/etc/vpn_handler/vpn_handler {service.lower()} install")
            except Exception as err:
                result = f"???????????? ?????????????????? {service}.\n{err}"
                color = 'color: rgb(255, 0, 0);'
                return result, color

        await self.get_server_status()

        result = "?????????????? ????????????????????."
        color = 'color: rgb(0, 200, 0);'

        return result, color

    async def get_config(self, service: str):
        if service.lower() not in ["openvpn", "wireguard", "shadowsocks", "socks"]:
            result = "???????????? ???????????????????????? ?????? ??????????????!"
            color = 'color: rgb(255, 0, 0);'
            return result, color

        if self.server is None or not self.server.established:
            result = "???????????????????? ?? ???????????????? ???? ??????????????????????!"
            color = 'color: rgb(255, 0, 0);'
            return result, color

        await self.get_server_status()

        user = self.get_user()

        if service.lower() == "openvpn":
            ext = ".ovpn"
        elif service.lower() == "wireguard":
            ext = ".conf"
        elif service.lower() == "shadowsocks":
            ext = ".json"
        elif service.lower() == "socks":
            ext = ""
        else:
            ext = ".txt"

        if not self.server_status.handler:
            result = "???????????????? VPN ???? ????????????????????!"
            color = 'color: rgb(255, 0, 0);'
            return result, color
        else:
            try:
                self.server.shell(cmd=f"/etc/vpn_handler/vpn_handler {service.lower()} add u{user}")
            except Exception as err:
                result = f"???????????? ?????????????????? ???????????????????????? ?????????????? ?????? {service}.\n{err}"
                color = 'color: rgb(255, 0, 0);'
                return result, color
            else:
                if service.lower() == "wireguard":
                    service = "wg"
                self.server.scp_download(file_remote_path=f"/etc/vpn_handler/configs/{service.lower()}_u{user}{ext}")
                if service.lower() == "socks":
                    self.make_socks_file(filename=f"{service.lower()}_u{user}{ext}")
                    ext = ".txt"
                elif service.lower() == "wg":
                    try:
                        self.server.shell(cmd=f"qrencode -t png -o /tmp/QR-{user}.png -r /etc/vpn_handler/configs/{service.lower()}_u{user}{ext}")
                    except Exception as err:
                        pass
                    else:
                        self.server.scp_download(file_remote_path=f"/tmp/QR-{user}.png")
                else:
                    pass

                if os.path.exists(f"{service.lower()}_u{user}{ext}"):
                    result = f"???????????????? ???????????? {service.lower()}_u{user}{ext}"
                else:
                    result = f"???????????? ???????????????? ??????????!"

        await self.get_server_status()

        color = 'color: rgb(0, 200, 0);'

        return result, color

    async def get_statistic(self) -> str:
        try:
            vpn_users = self.server.shell(cmd="ls /etc/vpn_handler/configs/ | wc -w")
            socks_users = self.server.shell(cmd="cat /etc/3proxy/.proxyauth | wc -l")
            vpn_users = int(vpn_users) - int(socks_users)
            net_stat = self.server.shell(cmd="vnstat")
            mem_stat = self.server.shell(cmd="free -h")
            disk_stat = self.server.shell(cmd="df -h /")
            server_time = self.server.shell(cmd="date")
        except Exception as err:
            return "???????????? ?????????????????????? ?? ??????????????!"

        msg = f'''
?????????????????? ??????????:  {server_time}

???????????????????? ?????????????????????????? VPN: {vpn_users}
???????????????????? ?????????????????????????? ????????????: {socks_users}

???????????????????? ??????:

{mem_stat}


???????????????????? HDD/SSD:

{disk_stat}

???????????????????? ????????:
{net_stat}
'''

        return msg
