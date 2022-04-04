import datetime
import os
import sys
from typing import Dict

from PyQt5 import QtCore, QtGui, QtWidgets
import time

import paramiko
from scp import SCPClient

bot_name = "VPNBot"


class SSH:
    def __init__(self, ip: str, port: int,
                 login: str, passwd: str,
                 label: QtWidgets.QLabel = None, msg: QtWidgets.QTextEdit = None):
        self.ssh = None
        self.established: bool = False
        self.ip = ip
        self.port = port
        self.login = login
        self.passwd = passwd
        # self.label = label
        # self.display = msg
        if label is not None:
            self.label: QtWidgets.QLabel = label
        else:
            self.label = None
        if msg is not None:
            self.display: QtWidgets.QTextEdit = msg
        else:
            self.display = None

    def label_ssh_on(self):
        if self.label is not None:
            self.label.setText("Соединен")
            self.label.setStyleSheet('color: rgb(0, 200, 0);')

    def label_ssh_off(self):
        if self.label is not None:
            self.label.setText("Не подключен")
            self.label.setStyleSheet('color: rgb(255, 0, 0);')

    def check_connect(self):
        if self.ssh is not None:
            try:
                self.established = self.ssh.get_transport().is_active()
            except Exception as err:
                self.established = False
        else:
            self.established = False

        if self.established:
            self.label_ssh_on()
        else:
            self.label_ssh_off()

        return self.established

    def connect(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            self.ssh.connect(hostname=self.ip, port=self.port, username=self.login, password=self.passwd)
        except Exception as err:
            self.label.setText("Ошибка!")
            self.label.setStyleSheet('color: rgb(255, 0, 0);')
            self.established = False
            return str(err)

        if self.check_connect():
            self.label_ssh_on()
            return f"Подключение к серверу {self.ip} установлено."

    def scp_upload(self, file_local_path: str, file_remote_path: str):
        with SCPClient(self.ssh.get_transport()) as scp:
            try:
                scp.put(files=file_local_path, remote_path=file_remote_path)
            except Exception as err:
                return str(err)

            return f"Файл {file_local_path} загружен на сервер {self.ip}."

    def scp_download(self, file_remote_path: str):
        with SCPClient(self.ssh.get_transport()) as scp:
            try:
                scp.get(remote_path=file_remote_path)
            except Exception as err:
                return str(err)

            return f"Файл {file_remote_path} загружен."

    def close(self):
        try:
            self.ssh.close()
        except Exception as err:
            return str(err)

        if not self.check_connect():
            self.label_ssh_off()
            return f"Сервер {self.ip} отключен."

    def shell(self, cmd: str):
        if not self.check_connect():
            return "Соединение с сервером не установлено!"

        try:
            (stdin, stdout, stderr) = self.ssh.exec_command(cmd)
        except Exception as err:
            return err

        time.sleep(0.5)
        answer = stdout.readlines()
        text = ""
        for line in answer:
            text += line

        return text


class Ui_MainWindow(object):
    def __init__(self):
        self.tab_main = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
### Начало первой вкладки
        self.tab_main = QtWidgets.QWidget()
        self.tab_main.setObjectName("tab_2")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab_main)
        self.verticalLayout.setObjectName("verticalLayout")


        ############# 1 строка ######################

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_2.setSpacing(20)

        # Надпись: IP
        self.label_ip = QtWidgets.QLabel(self.tab_main)
        self.label_ip.setText("IP")
        self.label_ip.setObjectName("label_ip")
        self.horizontalLayout_2.addWidget(self.label_ip)
        # Поле: IP
        self.form_ip = QtWidgets.QLineEdit(self.tab_main)
        self.form_ip.setPlaceholderText("1.1.1.1")
        self.form_ip.setObjectName("form_ip")
        self.horizontalLayout_2.addWidget(self.form_ip)

        # Надпись: Порт
        self.label_port = QtWidgets.QLabel(self.tab_main)
        self.label_port.setText("Порт")
        self.label_port.setObjectName("label_port")
        self.horizontalLayout_2.addWidget(self.label_port)
        # Поле: Порт
        self.form_port = QtWidgets.QLineEdit(self.tab_main)
        self.form_port.setPlaceholderText("22")
        self.form_port.setMaxLength(5)
        self.form_port.setValidator(QtGui.QIntValidator(1, 65656, self))
        self.form_port.setFixedWidth(50)
        self.form_port.setObjectName("form_port")
        self.horizontalLayout_2.addWidget(self.form_port)

        # Надпись: Логин
        self.label_login = QtWidgets.QLabel(self.tab_main)
        self.label_login.setText("Логин")
        self.label_login.setObjectName("label_login")
        self.horizontalLayout_2.addWidget(self.label_login)
        # Поле: Логин
        self.form_login = QtWidgets.QLineEdit(self.tab_main)
        self.form_login.setPlaceholderText("root")
        self.form_login.setObjectName("form_login")
        self.horizontalLayout_2.addWidget(self.form_login)

        # Надпись: Пароль
        self.label_passwd = QtWidgets.QLabel(self.tab_main)
        self.label_passwd.setText("Пароль")
        self.label_passwd.setObjectName("label_passwd")
        self.horizontalLayout_2.addWidget(self.label_passwd)
        # Поле: Пароль
        self.form_passwd = QtWidgets.QLineEdit(self.tab_main)
        self.form_passwd.setPlaceholderText("password")
        self.form_passwd.setObjectName("form_passwd")
        self.horizontalLayout_2.addWidget(self.form_passwd)

        # Поле: статус SSH
        self.label_ssh_status = QtWidgets.QLabel(self.tab_main)
        self.label_ssh_status.setText("Не подключен!")
        self.label_ssh_status.setObjectName("label_ssh_status")
        # self.label_ssh_status.setStyleSheet('background: rgb(255, 255, 255); color: rgb(200, 0, 0);')
        self.label_ssh_status.setStyleSheet('color: rgb(200, 0, 0);')
        self.horizontalLayout_2.addWidget(self.label_ssh_status)

        # Кнопка: Соединиться
        self.btn_ssh_connect = QtWidgets.QPushButton(self.tab_main)
        self.btn_ssh_connect.setText("Подключиться")
        self.btn_ssh_connect.setObjectName("btn_ssh_connect")
        self.horizontalLayout_2.addWidget(self.btn_ssh_connect)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        ############# 2 строка ######################

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_4.setSpacing(20)

        # Надпись: Запущен/Остановлен
        self.label_install_manager = QtWidgets.QLabel(self.tab_main)
        self.label_install_manager.setText("Не установлен")
        self.label_install_manager.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.label_install_manager.setObjectName("label_install_manager")
        self.horizontalLayout_4.addWidget(self.label_install_manager)

        # Кнопка: Запустить/Остановить бот
        self.btn_install_manager = QtWidgets.QPushButton(self.tab_main)
        self.btn_install_manager.setText("Установить менеджер на сервер")
        self.btn_install_manager.setObjectName("btn_install_manager")
        self.horizontalLayout_4.addWidget(self.btn_install_manager)

        self.verticalLayout.addLayout(self.horizontalLayout_4)

        ############# 3 строка ######################

        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(10, 10, 10, 0)
        self.horizontalLayout_5.setSpacing(20)

        # Надпись: OpenVPN
        self.label_openvpn = QtWidgets.QLabel(self.tab_main)
        self.label_openvpn.setText("OpenVPN")
        self.label_openvpn.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.label_openvpn.setObjectName("label_openvpn")
        self.horizontalLayout_5.addWidget(self.label_openvpn)

        # Кнопка: Установить OpenVPN
        self.btn_install_openvpn = QtWidgets.QPushButton(self.tab_main)
        self.btn_install_openvpn.setText("Установить OpenVPN")
        self.btn_install_openvpn.setObjectName("btn_install_openvpn")
        self.horizontalLayout_5.addWidget(self.btn_install_openvpn)

        # Надпись: WireGuard
        self.label_wireguard = QtWidgets.QLabel(self.tab_main)
        self.label_wireguard.setText("WireGuard")
        self.label_wireguard.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.label_wireguard.setObjectName("label_wireguard")
        self.horizontalLayout_5.addWidget(self.label_wireguard)

        # Кнопка: Установить WireGuard
        self.btn_install_wireguard = QtWidgets.QPushButton(self.tab_main)
        self.btn_install_wireguard.setText("Установить WireGuard")
        self.btn_install_wireguard.setObjectName("btn_install_wireguard")
        self.horizontalLayout_5.addWidget(self.btn_install_wireguard)

        # Надпись: Shadowsocks
        self.label_shadowsocks = QtWidgets.QLabel(self.tab_main)
        self.label_shadowsocks.setText("Shadowsocks")
        self.label_shadowsocks.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.label_shadowsocks.setObjectName("label_shadowsocks")
        self.horizontalLayout_5.addWidget(self.label_shadowsocks)

        # Кнопка: Установить Shadowsocks
        self.btn_install_shadowsocks = QtWidgets.QPushButton(self.tab_main)
        self.btn_install_shadowsocks.setText("Установить Shadowsocks")
        self.btn_install_shadowsocks.setObjectName("btn_install_shadowsocks")
        self.horizontalLayout_5.addWidget(self.btn_install_shadowsocks)

        # Надпись: Socks
        self.label_socks = QtWidgets.QLabel(self.tab_main)
        self.label_socks.setText("Socks")
        self.label_socks.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.label_socks.setObjectName("label_socks")
        self.horizontalLayout_5.addWidget(self.label_socks)

        # Кнопка: Установить Shadowsocks
        self.btn_install_socks = QtWidgets.QPushButton(self.tab_main)
        self.btn_install_socks.setText("Установить Socks")
        self.btn_install_socks.setObjectName("btn_install_socks")
        self.horizontalLayout_5.addWidget(self.btn_install_socks)

        self.verticalLayout.addLayout(self.horizontalLayout_5)

        ############# 4 строка ######################

        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(10, 0, 10, 10)
        self.horizontalLayout_5.setSpacing(20)

        # Кнопка: Установить OpenVPN
        self.btn_get_openvpn = QtWidgets.QPushButton(self.tab_main)
        self.btn_get_openvpn.setText("Получить конфиг OpenVPN")
        self.btn_get_openvpn.setObjectName("btn_get_openvpn")
        self.horizontalLayout_5.addWidget(self.btn_get_openvpn)

        # Кнопка: Установить WireGuard
        self.btn_get_wireguard = QtWidgets.QPushButton(self.tab_main)
        self.btn_get_wireguard.setText("Получить конфиг WireGuard")
        self.btn_get_wireguard.setObjectName("btn_get_wireguard")
        self.horizontalLayout_5.addWidget(self.btn_get_wireguard)

        # Кнопка: Установить Shadowsocks
        self.btn_get_shadowsocks = QtWidgets.QPushButton(self.tab_main)
        self.btn_get_shadowsocks.setText("Получить конфиг Shadowsocks")
        self.btn_get_shadowsocks.setObjectName("btn_get_shadowsocks")
        self.horizontalLayout_5.addWidget(self.btn_get_shadowsocks)

        # Кнопка: Установить Shadowsocks
        self.btn_get_socks = QtWidgets.QPushButton(self.tab_main)
        self.btn_get_socks.setText("Получить конфиг Socks")
        self.btn_get_socks.setObjectName("btn_get_socks")
        self.horizontalLayout_5.addWidget(self.btn_get_socks)

        self.verticalLayout.addLayout(self.horizontalLayout_5)

        ############# 5 строка ######################

        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_6.setSpacing(20)

        self.tab1_message_box = QtWidgets.QTextEdit(self.tab_main)
        self.tab1_message_box.setObjectName("textEdit")
        self.horizontalLayout_6.addWidget(self.tab1_message_box)

        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.tabWidget.addTab(self.tab_main, "")
# Конец первой вкладки

        self.tab_statistic = QtWidgets.QWidget()
        self.tab_statistic.setObjectName("tab_statistic")

        self.verticalLayout_statistic = QtWidgets.QVBoxLayout(self.tab_statistic)
        self.verticalLayout_statistic.setObjectName("verticalLayout_statistic")
        #
        # ############# 1 строка ######################
        #
        self.horizontalLayout_statistic_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_statistic_2.setObjectName("horizontalLayout_statistic_2")
        self.horizontalLayout_statistic_2.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_statistic_2.setSpacing(20)

        # Кнопка: Применить
        self.btn_get_statistic = QtWidgets.QPushButton(self.tab_statistic)
        self.btn_get_statistic.setText("Получить статистику")
        self.btn_get_statistic.setFixedWidth(200)
        self.btn_get_statistic.setObjectName("btn_get_statistic")
        self.horizontalLayout_statistic_2.addWidget(self.btn_get_statistic)

        self.verticalLayout_statistic.addLayout(self.horizontalLayout_statistic_2)

        #
        # ############# 2 строка ######################
        #
        self.horizontalLayout_statistic_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_statistic_3.setObjectName("horizontalLayout_statistic_3")
        self.horizontalLayout_statistic_3.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_statistic_3.setSpacing(20)

        self.tab_statistic_box = QtWidgets.QTextEdit(self.tab_statistic)
        self.tab_statistic_box.setObjectName("tab_statistic_box")
        self.horizontalLayout_statistic_3.addWidget(self.tab_statistic_box)

        self.verticalLayout_statistic.addLayout(self.horizontalLayout_statistic_3)

        self.tabWidget.addTab(self.tab_statistic, "")  # В конце вкладки
# Конец вкладки "Статистика"

# Конец
        self.horizontalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "VPNManager - консоль управления"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_main), _translate("MainWindow", "Главная"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_statistic), _translate("MainWindow", "Статистика"))


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
               f"Port: 9999\n" \
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





