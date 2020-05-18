import sys
import json

from PySide2.QtCore import (
    QUrl
)
from PySide2.QtWidgets import (
    QWidget,
    QDialog,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QGroupBox,
    QLineEdit,
    QComboBox,
    QLabel,
    QPushButton
)
from PySide2.QtNetwork import (
    QNetworkAccessManager,
    QNetworkRequest,
    QNetworkReply
)

from utils.settings import Settings

DUMMY_VALUE = "****************"


class ConfigWindow(QDialog):

    def __init__(self, appctx, parent):
        super().__init__(parent)

        self.appctx = appctx

        self.gateway_grid = QGridLayout()

        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()

        # settings groups
        gateway_box = QGroupBox("Gateway")
        gateway_box.setLayout(self.gateway_grid)
        self.hbox.addWidget(gateway_box)

        # ok and cancel buttons
        btn_hbox = QHBoxLayout()
        self.ok_button = QPushButton("Save")
        self.ok_button.pressed.connect(self.ok_pressed)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.pressed.connect(self.cancel_pressed)
        self.ok_button.setDefault(True)
        btn_hbox.addStretch()
        btn_hbox.addWidget(self.cancel_button)
        btn_hbox.addWidget(self.ok_button)

        # Set layout
        self.vbox.addLayout(self.hbox)
        self.vbox.addLayout(btn_hbox)
        self.setLayout(self.vbox)

        # gateway
        row = 0
        self.gateway_grid.addWidget(QLabel("Gateway IP"), row, 0)
        self.gateway_ip = QLineEdit()
        self.gateway_grid.addWidget(self.gateway_ip, row, 1)

        row += 1
        self.gateway_grid.addWidget(QLabel("Key"), row, 0)
        self.gateway_key = QLineEdit()
        self.gateway_key.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.gateway_grid.addWidget(self.gateway_key, row, 1)

        self.setWindowTitle('TradfriGUI Config')

        self.settings = Settings()
        self.load_settings()

    def load_settings(self):
        self.gateway_ip.setText(self.settings.gateway_ip)
        if self.settings.key is not None:
            self.gateway_key.setText(DUMMY_VALUE)

    def save_settings(self):
        if self.gateway_key.text() != DUMMY_VALUE:
            self.settings.key = None
            self.settings.identity = None
            self.settings.security_key = self.gateway_key.text()
        self.settings.gateway_ip = self.gateway_ip.text()
        self.settings.save()

    def ok_pressed(self):
        self.save_settings()
        self.close()

    def cancel_pressed(self):
        self.close()
