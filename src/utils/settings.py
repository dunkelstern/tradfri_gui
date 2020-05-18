from typing import Optional
import sys

from PySide2.QtCore import QSettings


class Settings:
    gateway_ip: Optional[str] = None
    security_key: Optional[str] = None
    identity: Optional[str] = None
    key: Optional[str] = None

    def __init__(self):
        company = 'dunkelstern' if sys.platform != 'darwin' else 'de.dunkelstern'
        self.settings = QSettings(company, 'TradfriGUI')
        self.load()

    def load(self):
        self.gateway_ip = self.settings.value('gateway/ip', None)
        self.identity = self.settings.value('gateway/identity', None)
        self.key = self.settings.value('gateway/key', None)

    def save(self):
        self.settings.setValue('gateway/ip', self.gateway_ip)
        self.settings.setValue('gateway/identity', self.identity)
        self.settings.setValue('gateway/key', self.key)
        self.settings.sync()
