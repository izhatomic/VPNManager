import sys
import os.path
import time
from typing import Dict

import paramiko
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtGui

from GUI.bot_install import bot_install_commands, bot_name
from GUI.ssh import SSH
from m1 import Ui_MainWindow  # Макет программы


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

        vpnbot_check = self.server.shell(cmd='if [[ -e /lib/systemd/system/vpnbot.service ]]; then echo "OK"; fi')
        if vpnbot_check.strip() == "OK":
            vpnbot_install = True
        else:
            vpnbot_install = False

        vpnbot_start_check = self.server.shell(
            cmd='sleep 5 ; if [[ ! -z $(service vpnbot status | grep -w active) ]]; then echo "OK"; fi')
        if vpnbot_start_check.strip() == "OK":
            vpnbot_start = True
        else:
            vpnbot_start = False

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
            "vpnbot": vpnbot_install,
            "bot_start": vpnbot_start,
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

        if data["handler"] and data["vpnbot"]:
            self.label_install_bot.setText("Бот установлен")
            # self.label_install_bot.setStyleSheet('background: rgb(255, 255, 255); color: rgb(0, 200, 0);')
            self.label_install_bot.setStyleSheet('color: rgb(0, 200, 0);')
        elif data["handler"] and not data["vpnbot"]:
            self.label_install_bot.setText("Бот не установлен")
            self.label_install_bot.setStyleSheet('color: rgb(255, 0, 0);')
            self.display("main", text="Бот не установлен!\n")
        elif not data["handler"] and data["vpnbot"]:
            self.label_install_bot.setText("Бот не установлен")
            self.label_install_bot.setStyleSheet('color: rgb(255, 0, 0);')
            self.display("main", text="Оркестратор VPN не установлен!\n")
        else:
            self.label_install_bot.setText("Бот не установлен")
            self.label_install_bot.setStyleSheet('color: rgb(255, 0, 0);')
            self.display("main", text="Оркестратор VPN и бот не установлен!\n")

        if data["bot_start"]:
            self.label_start_bot.setText("Запущен")
            self.label_start_bot.setStyleSheet('color: rgb(0, 200, 0);')
            self.btn_start_bot.setText("Остановить")
        else:
            self.label_start_bot.setText("Остановлен")
            self.label_start_bot.setStyleSheet('color: rgb(255, 0, 0);')
            self.btn_start_bot.setText("Запустить")

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

    def get_env_data(self):
        if self.server is None or not self.server.established:
            self.label_settings_status.setText("Соединение с сервером не установлено!")
            self.label_settings_status.setStyleSheet('color: rgb(255, 0, 0);')
            self.env_data = {}
            return self.env_data

        check = self.server.shell(cmd=f"if [[ -e /root/{bot_name}/.env ]]; then echo 'OK'; fi")
        if check.strip() != "OK":
            self.label_settings_status.setText("Бот не установлен на сервере!")
            self.label_settings_status.setStyleSheet('color: rgb(255, 0, 0);')
            self.env_data = {}
            return self.env_data

        bot_token = self.server.shell(cmd=f"cat /root/{bot_name}/.env | grep bot_token")
        if bot_token != "":
            self.env_data["bot_token"] = bot_token.split('=')[-1]

        bot_admin = self.server.shell(cmd=f"cat /root/{bot_name}/.env | grep bot_admin")
        if bot_admin != "":
            self.env_data["bot_admin"] = bot_admin.split('=')[-1]

        price_1_day = self.server.shell(cmd=f"cat /root/{bot_name}/.env | grep price_1_day")
        self.env_data["price_1_day"] = price_1_day.split('=')[-1]

        price_3_day = self.server.shell(cmd=f"cat /root/{bot_name}/.env | grep price_3_day")
        self.env_data["price_3_day"] = price_3_day.split('=')[-1]

        price_7_day = self.server.shell(cmd=f"cat /root/{bot_name}/.env | grep price_7_day")
        self.env_data["price_7_day"] = price_7_day.split('=')[-1]

        price_30_day = self.server.shell(cmd=f"cat /root/{bot_name}/.env | grep price_30_day")
        self.env_data["price_30_day"] = price_30_day.split('=')[-1]

        price_180_day = self.server.shell(cmd=f"cat /root/{bot_name}/.env | grep price_180_day")
        self.env_data["price_180_day"] = price_180_day.split('=')[-1]

        price_365_day = self.server.shell(cmd=f"cat /root/{bot_name}/.env | grep price_365_day")
        self.env_data["price_365_day"] = price_365_day.split('=')[-1]

        qiwi_number = self.server.shell(cmd=f"cat /root/{bot_name}/.env | grep qiwi_number")
        self.env_data["qiwi_number"] = qiwi_number.split('=')[-1]

        qiwi_token = self.server.shell(cmd=f"cat /root/{bot_name}/.env | grep qiwi_token")
        self.env_data["qiwi_token"] = qiwi_token.split('=')[-1]

        qiwi_pub = self.server.shell(cmd=f"cat /root/{bot_name}/.env | grep qiwi_pub")
        self.env_data["qiwi_pub"] = qiwi_pub.split('=')[-1]

        yoomoney_token = self.server.shell(cmd=f"cat /root/{bot_name}/.env | grep yoomoney_token")
        self.env_data["yoomoney_token"] = yoomoney_token.split('=')[-1]

        API_KEY = self.server.shell(cmd=f"cat /root/{bot_name}/.env | grep fk_api_key")
        self.env_data["fk_api_key"] = API_KEY.split('=')[-1]

        FK_secret = self.server.shell(cmd=f"cat /root/{bot_name}/.env | grep fk_secret")
        self.env_data["fk_secret"] = FK_secret[10:]

        SHOP_ID = self.server.shell(cmd=f"cat /root/{bot_name}/.env | grep fk_shop_id")
        self.env_data["fk_shop_id"] = SHOP_ID.split('=')[-1]

        return self.env_data

    def set_env_data(self):
        self.env_data = {}
        self.get_env_data()

        if self.env_data == {}:
            self.display("main", text="Ошибка чтения параметров бота!")
            self.label_settings_status.setStyleSheet('color: rgb(255, 0, 0);')
            return 1

        err = None
        try:
            self.form_bot_token.setText(self.env_data["bot_token"].strip())
        except Exception as er:
            self.display("main", text="Ошибка считывания bot_token")
            err = True

        try:
            self.form_bot_admin.setText(self.env_data["bot_admin"].strip())
        except Exception as er:
            self.display("main", text="Ошибка считывания bot_admin")
            err = True

        try:
            self.form_1_day_price.setText(self.env_data["price_1_day"].strip())
        except Exception as er:
            self.display("main", text="Ошибка считывания price_1_day")
            err = True

        try:
            self.form_3_day_price.setText(self.env_data["price_3_day"].strip())
        except Exception as er:
            self.display("main", text="Ошибка считывания price_3_day")
            err = True

        try:
            self.form_7_day_price.setText(self.env_data["price_7_day"].strip())
        except Exception as er:
            self.display("main", text="Ошибка считывания price_7_day")
            err = True

        try:
            self.form_30_day_price.setText(self.env_data["price_30_day"].strip())
        except Exception as er:
            self.display("main", text="Ошибка считывания price_30_day")
            err = True

        try:
            self.form_180_day_price.setText(self.env_data["price_180_day"].strip())
        except Exception as er:
            self.display("main", text="Ошибка считывания price_180_day")
            err = True

        try:
            self.form_365_day_price.setText(self.env_data["price_365_day"].strip())
        except Exception as er:
            self.display("main", text="Ошибка считывания price_365_day")
            err = True

        try:
            self.form_qiwi_number.setText(self.env_data["qiwi_number"].strip())
        except Exception as er:
            self.display("main", text="Ошибка считывания qiwi_number")
            err = True

        try:
            self.form_qiwi_token.setText(self.env_data["qiwi_token"].strip())
        except Exception as er:
            self.display("main", text="Ошибка считывания qiwi_token")
            err = True

        try:
            self.form_qiwi_pub.setText(self.env_data["qiwi_pub"].strip())
        except Exception as er:
            self.display("main", text="Ошибка считывания qiwi_pub")
            err = True

        try:
            self.form_yoomoney_token.setText(self.env_data["yoomoney_token"].strip())
        except Exception as er:
            self.display("main", text="Ошибка считывания yoomoney_token")
            err = True

        try:
            self.form_fk_api_key.setText(self.env_data["fk_api_key"].strip())
        except Exception as er:
            self.display("main", text="Ошибка считывания fk_api_key")
            err = True

        try:
            self.form_fk_secret.setText(self.env_data["fk_secret"].strip())
        except Exception as er:
            self.display("main", text="Ошибка считывания fk_secret")
            err = True

        try:
            self.form_fk_shop_id.setText(self.env_data["fk_shop_id"].strip())
        except Exception as er:
            self.display("main", text="Ошибка считывания fk_shop_id")
            err = True

        if err is not None:
            self.label_settings_status.setText("Считаны не все параметры!")
            self.label_settings_status.setStyleSheet('color: rgb(255, 0, 0);')
        else:
            self.label_settings_status.setText("Параметры считаны")
            self.label_settings_status.setStyleSheet('color: rgb(0, 200, 0);')

        return "Параметры бота считаны"

    def push_dev_data(self):
        self.label_settings_status.setText("Запись данных...")
        self.label_settings_status.setStyleSheet('color: rgb(255, 255, 255);')

        self.env_data["bot_token"] = self.form_bot_token.text().strip()

        self.env_data["bot_admin"] = self.form_bot_admin.text().strip()

        self.env_data["price_1_day"] = self.form_1_day_price.text().strip()
        self.env_data["price_3_day"] = self.form_3_day_price.text().strip()
        self.env_data["price_7_day"] = self.form_7_day_price.text().strip()
        self.env_data["price_30_day"] = self.form_30_day_price.text().strip()
        self.env_data["price_180_day"] = self.form_180_day_price.text().strip()
        self.env_data["price_365_day"] = self.form_365_day_price.text().strip()

        self.env_data["qiwi_number"] = self.form_qiwi_number.text().strip()

        self.env_data["qiwi_token"] = self.form_qiwi_token.text().strip()

        self.env_data["qiwi_pub"] = self.form_qiwi_pub.text().strip()

        self.env_data["yoomoney_token"] = self.form_yoomoney_token.text().strip()

        self.env_data["fk_api_key"] = self.form_fk_api_key.text().strip()

        self.env_data["fk_secret"] = self.form_fk_api_key.text().strip()

        self.env_data["fk_shop_id"] = self.form_fk_shop_id.text().strip()

        err = ""
        for key in self.env_data:
            err += self.server.shell(cmd=f'sed -i "/{key}/d" /root/{bot_name}/.env ; '
                                         f'echo "{key}={self.env_data[key]}" >> /root/{bot_name}/.env ;').strip()

        if err != "":
            self.label_settings_status.setText("Ошибка! Некоторые параметры могли быть не записаны")
            self.label_settings_status.setStyleSheet('color: rgb(255, 0, 0);')
        else:
            self.label_settings_status.setText("Параметры записаны")
            self.label_settings_status.setStyleSheet('color: rgb(0, 200, 0);')

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

    def btn_open_file_cliced(self):
        self.fname = QFileDialog.getOpenFileName(self, 'Open file', '')[0]
        self.form_open_file.setText(self.fname)

    def btn_start_bot_cliced(self):
        result = "Команда отправлена"
        if self.server_status["bot_start"]:
            try:
                self.server.shell(cmd="service vpnbot stop")
            except Exception as err:
                result = err
            # else:
            #     result = "Бот остановлен."
        else:
            try:
                self.server.shell(cmd="service vpnbot start")
            except Exception as err:
                result = err
            # else:
            #     result = "Бот запущен."

        self.display("main", text=result)
        self.set_status()

    def btn_install_bot_cliced(self):
        if self.server is None or not self.server.established:
            self.display("main", text="Соединение с сервером не установлено!")
            return 1

        self.fname = self.form_open_file.text()

        if len(self.fname) > 2 and os.path.exists(self.fname):
            self.display("main", text=f"Файл {self.fname} будет загружен на сервер {self.server.ip}\n")
            try:
                result = self.server.scp_upload(file_local_path=self.fname, file_remote_path="/root/")
            except Exception as err:
                result = str(err)

            self.display("main", text=result)
        else:
            self.display("main", text=f"Файл не найден!")
            return 1

        check = self.server.shell(cmd=f"if [[ -e /root/{self.fname.split('/')[-1]} ]]; then echo 'OK'; fi")
        if check.strip() != "OK":
            self.display("main", text=f"Архив с ботом ({self.fname.split('/')[-1]}) не загружен на сервер! "
                                      "Загрузите бот и повторите попытку.")
            return 1
        else:
            self.display("main", text="Началась установка бота...")
            time.sleep(5)
            self.server.shell(cmd=bot_install_commands)

        self.set_status()
        if self.server_status["handler"] and self.server_status["vpnbot"]:
            self.display("main", text="VPNBot успешно установлен.")
        else:
            self.display("main", text="Установка VPNBot завершилась с ошибкой. Бот не установлен.")

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
        pass

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
