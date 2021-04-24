# coding: iso-8859-1 -*-

import sys
from design import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from functions import ChromeDriver
from time import sleep
import requests


class LichessExcel(QMainWindow, Ui_MainWindow, ChromeDriver):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.setFixedSize(519, 163)
        self.list = self.type = []
        self.linkline.setText('')
        self.archiveline.setText('')
        self.pathline.setText('')
        self.pathbutton.clicked.connect(self.save)
        self.sendbutton.clicked.connect(self.make_excel)

    def save(self):
        path = QFileDialog.getExistingDirectory()
        self.pathline.setText(path)

    def clear_spaces(self):
        self.linkline.setText('')
        self.archiveline.setText('')

    def validate(self):
        url = self.linkline.text()
        file = self.archiveline.text()
        path = self.pathline.text()

        if not 'https://lichess.org/' in url:
            self.resultline.setText('LINK INVALIDO')
            self.clear_spaces()
            return False

        elif url == '' or path == '' or file == '':
            self.resultline.setText('CAMPOS INVALIDO')
            self.clear_spaces()
            return False

        if not requests.get(url).status_code == 200:
            self.resultline.setText('SITE NÃO ENCONTRADO')
            self.clear_spaces()
            return False

        return True

    def make_excel(self):
        url = self.linkline.text()
        file_name = self.archiveline.text()
        path = self.pathline.text()

        ok = self.validate()

        if not ok:
            return

        chrome = ChromeDriver()

        chrome.get(url)
        num_next = chrome.num_players()

        for i in range(num_next):
            self.list, self.type = chrome.get_datas()
            chrome.next_page()
            sleep(2)

        chrome.do_excel(self.list, self.type, file_name, path)
        chrome.quit()
        self.resultline.setText('ARQUIVO SALVO')
        self.clear_spaces()


if __name__ == '__main__':
    qt = QApplication(sys.argv)
    webscrap = LichessExcel()
    webscrap.show()
    qt.exec_()
