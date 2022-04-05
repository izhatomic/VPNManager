import sys
import os.path
import time
from typing import Dict

import datetime

import paramiko
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtGui

from GUI.ssh import SSH
from m1 import Ui_MainWindow  # Макет программы

bot_name = "VPNBot"

# Создаем класс и наследуем его от макета программы
class GuiForVPNBot(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent=parent)
        self.server = None
        self.server_status: Dict = {}
        self.env_data: Dict = {}
        self.fname = None
        self.setupUi(self)
        self.btn_cliced()
        self.tab = {
            "main": self.tab1_message_box,
            "stat": self.tab_statistic_box,
        }

    def display(self, tab: str, text: str, clear: bool = False):
        box = self.tab[tab]

        if clear is False:
            msg = self.tab1_message_box.toPlainText() + '\n'
        else:
            msg: str = "\n"

        try:
            iterator = iter(text)
        except TypeError:
            msg = f"{msg}\n{text}\n"
            box.setText(msg)
        else:
            for line in text:
                msg += line
                box.setText(msg)

    def get_server_status(self):
        if self.server is None or not self.server.established:
            return {}

        handler_check = self.server.shell(cmd='if [[ -e /etc/vpn_handler/vpn_handler ]]; then echo "OK"; fi')
        if handler_check.strip() == "OK":
            handler_install = True
        else:
            handler_install = False

        openvpn_check = self.server.shell(cmd='if [[ ! -z $(which openvpn) ]]; then echo "OK"; fi')
        if openvpn_check.strip() == "OK":
            openvpn_install = True
        else:
            openvpn_install = False

        wireguard_check = self.server.shell(cmd='if [[ ! -z $(which wg-quick) ]]; then echo "OK"; fi')
        if wireguard_check.strip() == "OK":
            wireguard_install = True
        else:
            wireguard_install = False

        shadowsocks_check = self.server.shell(cmd='if [[ ! -z $(which ss-server) ]]; then echo "OK"; fi')
        if shadowsocks_check.strip() == "OK":
            shadowsocks_install = True
        else:
            shadowsocks_install = False

        socks_check = self.server.shell(cmd='if [[ ! -z $(which 3proxy) ]]; then echo "OK"; fi')
        if socks_check.strip() == "OK":
            socks_install = True
        else:
            socks_install = False

        self.server_status = {
            "handler": handler_install,
            "openvpn": openvpn_install,
            "wireguard": wireguard_install,
            "shadowsocks": shadowsocks_install,
            "socks": socks_install,
        }

        return self.server_status

    def set_status(self, data: Dict = None):

        self.get_server_status()
        if data is None:
            data = self.server_status

        if data["handler"]:
            self.label_install_manager.setText("Установлен")
            self.label_install_manager.setStyleSheet('color: rgb(0, 200, 0);')
        else:
            self.label_install_manager.setText("Не установлен")
            self.label_install_manager.setStyleSheet('color: rgb(255, 0, 0);')

        if data["openvpn"]:
            self.label_openvpn.setText("Установлен")
            self.label_openvpn.setStyleSheet('color: rgb(0, 200, 0);')
        else:
            self.label_openvpn.setText("Не установлен")
            self.label_openvpn.setStyleSheet('color: rgb(255, 0, 0);')

        if data["wireguard"]:
            self.label_wireguard.setText("Установлен")
            self.label_wireguard.setStyleSheet('color: rgb(0, 200, 0);')
        else:
            self.label_wireguard.setText("Не установлен")
            self.label_wireguard.setStyleSheet('color: rgb(255, 0, 0);')

        if data["shadowsocks"]:
            self.label_shadowsocks.setText("Установлен")
            self.label_shadowsocks.setStyleSheet('color: rgb(0, 200, 0);')
        else:
            self.label_shadowsocks.setText("Не установлен")
            self.label_shadowsocks.setStyleSheet('color: rgb(255, 0, 0);')

        if data["socks"]:
            self.label_socks.setText("Установлен")
            self.label_socks.setStyleSheet('color: rgb(0, 200, 0);')
        else:
            self.label_socks.setText("Не установлен")
            self.label_socks.setStyleSheet('color: rgb(255, 0, 0);')

    def get_user(self):
        now = datetime.datetime.now()
        delta = (now - datetime.datetime(1970, 1, 1))
        return delta.total_seconds()

    def btn_ssh_connect_cliced(self):
        result = ""
        if self.server is not None and self.server.established:
            try:
                result = self.server.close()
            except Exception as err:
                self.display("main", text=str(err))
            self.btn_ssh_connect.setText("Подключиться")
            self.display("main", text=result)
        else:
            self.server = SSH(ip=self.form_ip.text(), port=self.form_port.text(),
                              login=self.form_login.text(), passwd=self.form_passwd.text(),
                              label=self.label_ssh_status, msg=self.tab["main"])
            try:
                result = self.server.connect()
            except Exception as err:
                result = err
                self.server.established = False

            self.display("main", text=result, clear=True)

            if self.server is not None and self.server.established:
                self.btn_ssh_connect.setText("Отключиться")
                self.set_status()
                # self.set_env_data()

    def btn_install_openvpn_cliced(self):
        if self.server is None or not self.server.established:
            self.display("main", text="Соединение с сервером не установлено!")
            return 1

        check = self.server.shell(cmd="if [[ -e /etc/vpn_handler/vpn_handler ]]; then echo 'OK'; fi")
        if check.strip() != "OK":
            self.display("main", text="Оркестратор VPN не установлен!")
            return 1
        else:
            self.display("main", text="Началась установка OpenVPN...")
            time.sleep(5)
            try:
                self.server.shell(cmd="/etc/vpn_handler/vpn_handler openvpn install")
            except Exception as err:
                self.display("main", text=f"Ошибка установки OpenVPN.\n{err}")

        self.set_status()
        if self.server_status["openvpn"]:
            self.display("main", text="OpenVPN установлен.")
        else:
            self.display("main", text="OpenVPN не установлен.")

    def btn_install_wireguard_cliced(self):
        if self.server is None or not self.server.established:
            self.display("main", text="Соединение с сервером не установлено!")
            return 1

        check = self.server.shell(cmd="if [[ -e /etc/vpn_handler/vpn_handler ]]; then echo 'OK'; fi")
        if check.strip() != "OK":
            self.display("main", text="Оркестратор VPN не установлен!")
            return 1
        else:
            self.display("main", text="Началась установка WireGuard...")
            time.sleep(5)
            try:
                self.server.shell(cmd="/etc/vpn_handler/vpn_handler wireguard install")
            except Exception as err:
                self.display("main", text=f"Ошибка установки WireGuard.\n{err}")

        self.set_status()
        if self.server_status["wireguard"]:
            self.display("main", text="WireGuard установлен.")
        else:
            self.display("main", text="WireGuard не установлен.")

    def btn_install_shadowsocks_cliced(self):
        if self.server is None or not self.server.established:
            self.display("main", text="Соединение с сервером не установлено!")
            return 1

        check = self.server.shell(cmd="if [[ -e /etc/vpn_handler/vpn_handler ]]; then echo 'OK'; fi")
        if check.strip() != "OK":
            self.display("main", text="Оркестратор VPN не установлен!")
            return 1
        else:
            self.display("main", text="Началась установка Shadowsocks...")
            time.sleep(5)
            try:
                self.server.shell(cmd="/etc/vpn_handler/vpn_handler shadowsocks install")
            except Exception as err:
                self.display("main", text=f"Ошибка установки Shadowsocks.\n{err}")

        self.set_status()
        if self.server_status["shadowsocks"]:
            self.display("main", text="Shadowsocks установлен.")
        else:
            self.display("main", text="Shadowsocks не установлен.")

    def btn_install_socks_cliced(self):
        if self.server is None or not self.server.established:
            self.display("main", text="Соединение с сервером не установлено!")
            return 1

        check = self.server.shell(cmd="if [[ -e /etc/vpn_handler/vpn_handler ]]; then echo 'OK'; fi")
        if check.strip() != "OK":
            self.display("main", text="VPNManager не установлен!")
            return 1
        else:
            self.display("main", text="Началась установка Socks-proxy...")
            time.sleep(5)
            try:
                self.server.shell(cmd="/etc/vpn_handler/vpn_handler socks install")
            except Exception as err:
                self.display("main", text=f"Ошибка установки Socks-proxy.\n{err}")

        self.set_status()
        if self.server_status["socks"]:
            self.display("main", text="Socks-proxy установлен.")
        else:
            self.display("main", text="Socks-proxy не установлен.")

    def btn_install_manager_cliced(self):
        install_cmd = """
        wget https://github.com/izhatomic/VPNManager/releases/download/v1.0/vpn_handler
        chmod +x vpn_handler
        mkdir -p /etc/vpn_handler
        mv vpn_handler /etc/vpn_handler/
        /etc/vpn_handler/vpn_handler scheduler install
        apt-get update
        apt-get install vnstat -y
        """

        try:
            self.server.shell(cmd=install_cmd)
        except Exception as err:
            self.display("main", text="Сбой подключения к серверу!")
        else:
            try:
                check = self.server.shell(cmd="if [[ -e /etc/vpn_handler/vpn_handler ]]; then echo 'OK'; fi")
            except Exception as err:
                self.display("main", text="Сбой подключения к серверу!")
                return 1
            else:
                if check.strip() == "OK":
                    self.display("main", text="VPNManager установлен")
                else:
                    self.display("main", text="Ошибка установки VPNManager")

        self.set_status()

    def btn_get_openvpn_cliced(self):
        try:
            check = self.server.established
        except Exception as err:
            self.display("main", text="Соединение с сервером не установлено!")
            return 1
        else:
            if not check:
                self.display("main", text="Соединение с сервером не установлено!")
                return 1

        user = self.get_user()

        try:
            install = self.server_status["openvpn"]
        except Exception as err:
            install = False

        if install:
            try:
                self.server.shell(cmd=f"/etc/vpn_handler/vpn_handler openvpn add u{user}")
            except Exception as err:
                self.display("main", text="Ошибка подключения к серверу!")
            else:
                self.server.scp_download(file_remote_path=f"/etc/vpn_handler/configs/openvpn_u{user}.ovpn")
                if os.path.exists(f"openvpn_u{user}.ovpn"):
                    self.display("main", text=f"Загружен конфиг openvpn_u{user}.ovpn")
                else:
                    self.display("main", text=f"Ошибка загрузки файла!")
        else:
            self.display("main", text=f"OpenVPN не установлен на сервере!")

    def btn_get_wireguard_cliced(self):
        try:
            check = self.server.established
        except Exception as err:
            self.display("main", text="Соединение с сервером не установлено!")
            return 1
        else:
            if not check:
                self.display("main", text="Соединение с сервером не установлено!")
                return 1

        user = self.get_user()

        try:
            install = self.server_status["wireguard"]
        except Exception as err:
            install = False

        if install:
            try:
                self.server.shell(cmd=f"/etc/vpn_handler/vpn_handler wireguard add u{user}")
            except Exception as err:
                self.display("main", text="Ошибка подключения к серверу!")
            else:
                self.server.scp_download(file_remote_path=f"/etc/vpn_handler/configs/wireguard_u{user}.conf")
                if os.path.exists(f"wireguard_u{user}.conf"):
                    self.display("main", text=f"Загружен конфиг wireguard_u{user}.conf")
                else:
                    self.display("main", text=f"Ошибка загрузки файла!")
        else:
            self.display("main", text=f"WireGuard не установлен на сервере!")

    def btn_get_shadowsocks_cliced(self):
        try:
            check = self.server.established
        except Exception as err:
            self.display("main", text="Соединение с сервером не установлено!")
            return 1
        else:
            if not check:
                self.display("main", text="Соединение с сервером не установлено!")
                return 1

        user = self.get_user()

        try:
            install = self.server_status["shadowsocks"]
        except Exception as err:
            install = False

        if install:
            try:
                self.server.shell(cmd=f"/etc/vpn_handler/vpn_handler shadowsocks add u{user}")
            except Exception as err:
                self.display("main", text="Ошибка подключения к серверу!")
            else:
                self.server.scp_download(file_remote_path=f"/etc/vpn_handler/configs/shadowsocks_u{user}.json")
                if os.path.exists(f"shadowsocks_u{user}.json"):
                    self.display("main", text=f"Загружен конфиг shadowsocks_u{user}.json")
                else:
                    self.display("main", text=f"Ошибка загрузки файла!")
        else:
            self.display("main", text=f"Shadowsocks не установлен на сервере!")

    def make_socks_file(self, filename: str):
        with open(filename, 'rt') as file:
            line = file.read().strip()
            user = line.split(":")[0]
            passwd = line.split(":")[-1]

        data = f"Proxy IP: {self.form_ip.text()}\n" \
               f"Type: SOCKS5" \
               f"Port SOCKS5: 9999\n" \
               f"Port HTTPS: 9100\n" \
               f"Login: {user}\n" \
               f"Password: {passwd}"

        with open(f"{filename}.txt", 'wt') as file:
            file.write(data)

        os.remove(filename)

    def btn_get_socks_cliced(self):
        try:
            check = self.server.established
        except Exception as err:
            self.display("main", text="Соединение с сервером не установлено!")
            return 1
        else:
            if not check:
                self.display("main", text="Соединение с сервером не установлено!")
                return 1

        user = self.get_user()

        try:
            install = self.server_status["socks"]
        except Exception as err:
            install = False

        if install:
            try:
                self.server.shell(cmd=f"/etc/vpn_handler/vpn_handler socks add u{user}")
            except Exception as err:
                self.display("main", text="Ошибка подключения к серверу!")
            else:
                self.server.scp_download(file_remote_path=f"/etc/vpn_handler/configs/socks_u{user}")
                if os.path.exists(f"socks_u{user}"):
                    self.make_socks_file(f"socks_u{user}")
                    self.display("main", text=f"Загружен конфиг socks_u{user}")
                else:
                    self.display("main", text=f"Ошибка загрузки файла!")
        else:
            self.display("main", text=f"Socks-прокси не установлен на сервере!")

    def btn_get_statistic_cliced(self):
        try:
            stat = self.server.shell(cmd="vnstat")
        except Exception as err:
            stat = "Ошибка подключения к серверу!"
        self.display("stat", text=stat, clear=True)

    def btn_cliced(self):
        self.btn_ssh_connect.clicked.connect(lambda: self.btn_ssh_connect_cliced())
        self.btn_install_manager.clicked.connect(lambda: self.btn_install_manager_cliced())
        self.btn_install_openvpn.clicked.connect(lambda: self.btn_install_openvpn_cliced())
        self.btn_install_wireguard.clicked.connect(lambda: self.btn_install_wireguard_cliced())
        self.btn_install_shadowsocks.clicked.connect(lambda: self.btn_install_shadowsocks_cliced())
        self.btn_install_socks.clicked.connect(lambda: self.btn_install_socks_cliced())
        self.btn_get_openvpn.clicked.connect(lambda: self.btn_get_openvpn_cliced())
        self.btn_get_wireguard.clicked.connect(lambda: self.btn_get_wireguard_cliced())
        self.btn_get_shadowsocks.clicked.connect(lambda: self.btn_get_shadowsocks_cliced())
        self.btn_get_socks.clicked.connect(lambda: self.btn_get_socks_cliced())
        self.btn_get_statistic.clicked.connect(lambda: self.btn_get_statistic_cliced())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    try:
        from PyQt5.QtWinExtras import QtWin

        myappid = 'izhsaa.vpnbot.gui.1_0'
        QtWin.setCurrentProcessExplicitAppUserModelID(myappid)
    except ImportError:
        pass

    app.setWindowIcon(QtGui.QIcon('vpnmanager.png'))

    app.setStyle("Fusion")
    MainWindow = GuiForVPNBot()
    MainWindow.show()
    sys.exit(app.exec_())
