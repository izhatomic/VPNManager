import time

import paramiko
from PyQt5 import QtWidgets
from scp import SCPClient
import sys


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

    def check_connect(self) -> bool:
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






