import asyncio
import sys
import os.path
import time
from typing import Dict

import datetime

import paramiko
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtGui

from GUI.VPN_Manager import VPNManager
from GUI.ssh import SSH
from m1 import Ui_MainWindow  # Макет программы

bot_name = "VPNBot"


# Создаем класс и наследуем его от макета программы
class GuiForVPNBot(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent=parent)
        self.vpnmanager = VPNManager()
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

    def set_status(self, data: None):
        if data is None:
            data = self.vpnmanager.server_status

        if data.connected:
            self.label_ssh_status.setText("Подключен")
            self.label_ssh_status.setStyleSheet('color: rgb(0, 200, 0);')
            self.btn_ssh_connect.setText("Отключиться")
        else:
            self.label_ssh_status.setText("Не подключен")
            self.label_ssh_status.setStyleSheet('color: rgb(255, 0, 0);')
            self.btn_ssh_connect.setText("Подключиться")

        if data.handler:
            self.label_install_manager.setText("Менеджер VPN установлен")
            # self.label_install_manager.setStyleSheet('background: rgb(255, 255, 255); color: rgb(0, 200, 0);')
            self.label_install_manager.setStyleSheet('color: rgb(0, 200, 0);')
        else:
            self.label_install_manager.setText("Менеджер VPN не установлен")
            self.label_install_manager.setStyleSheet('color: rgb(255, 0, 0);')

        if data.openvpn:
            self.label_openvpn.setText("Установлен")
            self.label_openvpn.setStyleSheet('color: rgb(0, 200, 0);')
        else:
            self.label_openvpn.setText("Не установлен")
            self.label_openvpn.setStyleSheet('color: rgb(255, 0, 0);')

        if data.wireguard:
            self.label_wireguard.setText("Установлен")
            self.label_wireguard.setStyleSheet('color: rgb(0, 200, 0);')
        else:
            self.label_wireguard.setText("Не установлен")
            self.label_wireguard.setStyleSheet('color: rgb(255, 0, 0);')

        if data.shadowsocks:
            self.label_shadowsocks.setText("Установлен")
            self.label_shadowsocks.setStyleSheet('color: rgb(0, 200, 0);')
        else:
            self.label_shadowsocks.setText("Не установлен")
            self.label_shadowsocks.setStyleSheet('color: rgb(255, 0, 0);')

        if data.socks:
            self.label_socks.setText("Установлен")
            self.label_socks.setStyleSheet('color: rgb(0, 200, 0);')
        else:
            self.label_socks.setText("Не установлен")
            self.label_socks.setStyleSheet('color: rgb(255, 0, 0);')

    def btn_ssh_connect_cliced(self):
        result = ""
        if self.vpnmanager.server is not None and self.vpnmanager.server.established:
            result = asyncio.run(self.vpnmanager.disconnect())
            self.display("main", text=result)
        else:
            result = asyncio.run(self.vpnmanager.connect(ip=self.form_ip.text(), port=self.form_port.text(),
                                                         login=self.form_login.text(), passwd=self.form_passwd.text()))
            self.display("main", text=result, clear=True)

        self.set_status(data=self.vpnmanager.server_status)
        # self.display("main", text=result)

    def btn_install_openvpn_cliced(self):
        result, color = asyncio.run(self.vpnmanager.install_service("OpenVPN"))
        self.set_status(data=self.vpnmanager.server_status)
        self.display("main", text=result)

    def btn_install_wireguard_cliced(self):
        result, color = asyncio.run(self.vpnmanager.install_service("Wireguard"))
        self.set_status(data=self.vpnmanager.server_status)
        self.display("main", text=result)

    def btn_install_shadowsocks_cliced(self):
        result, color = asyncio.run(self.vpnmanager.install_service("Shadowsocks"))
        self.set_status(data=self.vpnmanager.server_status)
        self.display("main", text=result)

    def btn_install_socks_cliced(self):
        result, color = asyncio.run(self.vpnmanager.install_service("Socks"))
        self.set_status(data=self.vpnmanager.server_status)
        self.display("main", text=result)

    def btn_install_manager_cliced(self):
        result = asyncio.run(self.vpnmanager.install_manager())
        self.set_status(data=self.vpnmanager.server_status)
        self.display("main", text=result)

    def btn_get_openvpn_cliced(self):
        result, color = asyncio.run(self.vpnmanager.get_config("OpenVPN"))
        self.set_status(data=self.vpnmanager.server_status)
        self.display("main", text=result)

    def btn_get_wireguard_cliced(self):
        result, color = asyncio.run(self.vpnmanager.get_config("Wireguard"))
        self.set_status(data=self.vpnmanager.server_status)
        self.display("main", text=result)

    def btn_get_shadowsocks_cliced(self):
        result, color = asyncio.run(self.vpnmanager.get_config("Shadowsocks"))
        self.set_status(data=self.vpnmanager.server_status)
        self.display("main", text=result)

    def btn_get_socks_cliced(self):
        result, color = asyncio.run(self.vpnmanager.get_config("Socks"))
        self.set_status(data=self.vpnmanager.server_status)
        self.display("main", text=result)

    def btn_get_statistic_cliced(self):
        stat = asyncio.run(self.vpnmanager.get_statistic())
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
