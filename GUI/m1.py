from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt


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
