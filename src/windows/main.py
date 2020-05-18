import sys
import json

from PySide2.QtCore import (
    QUrl,
    QByteArray,
    QSize,
    Qt,
    QTimer
)
from PySide2.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QGroupBox,
    QCheckBox,
    QListWidget,
    QListWidgetItem,
    QComboBox,
    QSlider
)
from PySide2.QtGui import (
    QIcon
)

from pytradfri import Gateway


from utils.settings import Settings
from utils.resource_path import resource_path
from utils.auth import get_api
from windows.config import ConfigWindow


class MainWindow(QWidget):

    def __init__(self, appctx):
        super().__init__()

        self.appctx = appctx
        self.api = None
        self.settings = Settings()
        self.gateway = Gateway()
        self.timers:Dict[str, QTimer] = {}

        self.init_ui()

    def init_ui(self):
        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()

        # Set layout
        self.setLayout(self.vbox)

        # Group list
        vbox3 = QVBoxLayout()
        group_frame = QGroupBox("Device Groups")
        group_frame.setLayout(QVBoxLayout())
        self.group_list = QListWidget()
        self.group_list.itemActivated.connect(self.group_selected)
        vbox3.addWidget(self.group_list)

        # Sliders
        self.group_toggle = QCheckBox("Power")
        self.group_toggle.setEnabled(False)
        self.group_toggle.stateChanged.connect(self.group_toggled)
        vbox3.addWidget(self.group_toggle)
        vbox3.addWidget(QLabel("Brightness"))
        self.group_brightness_slider = QSlider(Qt.Orientation.Horizontal)
        self.group_brightness_slider.setEnabled(False)
        self.group_brightness_slider.sliderMoved.connect(self.group_brightness_changed)
        vbox3.addWidget(self.group_brightness_slider)
        vbox3.addWidget(QLabel("Color Temperature"))
        self.group_color_slider = QSlider(Qt.Orientation.Horizontal)
        self.group_color_slider.setEnabled(False)
        self.group_color_slider.sliderMoved.connect(self.group_color_changed)
        vbox3.addWidget(self.group_color_slider)

        self.hbox.addLayout(vbox3)

        # Devices in group
        vbox2 = QVBoxLayout()

        device_frame = QGroupBox("Devices in Group")
        device_frame.setLayout(QVBoxLayout())
        self.device_list = QListWidget()
        self.device_list.setEnabled(False)
        self.device_list.itemActivated.connect(self.device_selected)
        device_frame.layout().addWidget(self.device_list)
        vbox2.addWidget(device_frame)

        # Sliders
        self.device_toggle = QCheckBox("Power")
        self.device_toggle.setEnabled(False)
        self.device_toggle.stateChanged.connect(self.device_toggled)
        vbox2.addWidget(self.device_toggle)
        vbox2.addWidget(QLabel("Brightness"))
        self.brightness_slider = QSlider(Qt.Orientation.Horizontal)
        self.brightness_slider.setEnabled(False)
        self.brightness_slider.sliderMoved.connect(self.brightness_changed)
        vbox2.addWidget(self.brightness_slider)
        vbox2.addWidget(QLabel("Color Temperature"))
        self.color_slider = QSlider(Qt.Orientation.Horizontal)
        self.color_slider.setEnabled(False)
        self.color_slider.sliderMoved.connect(self.color_changed)
        vbox2.addWidget(self.color_slider)

        self.hbox.addLayout(vbox2)
        self.vbox.addLayout(self.hbox)

        # Settings button
        icon = QIcon(resource_path('icons/settings.png'))
        self.settings_button = QPushButton(icon, "Settings")
        self.settings_button.pressed.connect(self.settings_pressed)
        self.vbox.addWidget(self.settings_button)

        self.setWindowTitle('TradfriGUI')
        self.re_init()

    def re_init(self):
        if self.settings.gateway_ip is None or self.settings.gateway_ip == '':
            self.settings_pressed()
        self.api = get_api(self.settings)

        self.device_list.clear()
        self.group_list.clear()

        groups = self.api(self.gateway.get_groups())
        if len(groups) == 0:
            self.group_list.setEnabled(False)
            # TODO: load devices directly

        for group in groups:
            item = self.api(group)
            list_item = QListWidgetItem(item.name, self.group_list)
            setattr(list_item, 'api_item', item)

    def group_selected(self):
        current_item = self.group_list.currentItem()
        item = getattr(current_item, 'api_item', None)
        if item is None:
            return
        devices = item.members()
        self.device_list.clear()

        state = False
        brightness = []
        for d in devices:
            device = self.api(d)
            if device.has_light_control:
                if device.light_control.lights[0].state:
                    state = True
                if device.light_control.can_set_dimmer:
                    if device.light_control.lights[0].state:
                        brightness.append(device.light_control.lights[0].dimmer)
                    else:
                        brightness.append(0)
            list_item = QListWidgetItem(device.name, self.device_list)
            setattr(list_item, 'api_item', device)

        if len(brightness) > 0:
            brightness = int(sum(brightness) / len(brightness))
        else:
            brightness = 0

        self.device_list.setEnabled(True)

        self.group_brightness_slider.setEnabled(True)
        self.group_brightness_slider.setMinimum(0)
        self.group_brightness_slider.setMaximum(254)
        self.group_brightness_slider.setSingleStep(16)
        self.group_brightness_slider.setValue(brightness)

        self.group_toggle.setEnabled(True)
        self.group_toggle.setCheckState(Qt.CheckState.Checked if state else Qt.CheckState.Unchecked)

        self.brightness_slider.setEnabled(False)
        self.color_slider.setEnabled(False)
        self.device_toggle.setEnabled(False)


    def device_selected(self):
        current_item = self.device_list.currentItem()
        item = getattr(current_item, 'api_item', None)
        if item is None:
            return

        if item.has_light_control:
            ctrl = item.light_control
            if ctrl.can_set_dimmer:
                self.brightness_slider.setEnabled(True)
                self.brightness_slider.setMinimum(0)
                self.brightness_slider.setMaximum(254)
                self.brightness_slider.setSingleStep(16)
                self.brightness_slider.setValue(ctrl.lights[0].dimmer)
            else:
                self.brightness_slider.setEnabled(False)
            if ctrl.can_set_temp:
                self.color_slider.setEnabled(True)
                self.color_slider.setMinimum(ctrl.min_mireds)
                self.color_slider.setMaximum(ctrl.max_mireds)
                self.color_slider.setSingleStep(int((ctrl.max_mireds - ctrl.min_mireds) / 10))
                self.color_slider.setValue(ctrl.lights[0].color_temp)
            else:
                self.color_slider.setEnabled(False)
            self.device_toggle.setEnabled(True)
            self.device_toggle.setCheckState(Qt.CheckState.Checked if ctrl.lights[0].state else Qt.CheckState.Unchecked)
        else:
            self.brightness_slider.setEnabled(False)
            self.color_slider.setEnabled(False)
            self.device_toggle.setEnabled(False)

    def group_brightness_changed(self):
        current_item = self.group_list.currentItem()
        if current_item is None:
            return
        item = getattr(current_item, 'api_item', None)
        command = item.set_dimmer(self.group_brightness_slider.value(), transition_time=2)

        self.queue_command('group_brightness', command)

    def group_color_changed(self):
        current_item = self.group_list.currentItem()
        if current_item is None:
            return
        item = getattr(current_item, 'api_item', None)

    def brightness_changed(self):
        current_item = self.device_list.currentItem()
        if current_item is None:
            return
        item = getattr(current_item, 'api_item', None)
        command = item.light_control.set_dimmer(self.brightness_slider.value(), transition_time=2)

        self.queue_command('device_brightness_{}'.format(item.id), command)

    def color_changed(self):
        current_item = self.device_list.currentItem()
        if current_item is None:
            return
        item = getattr(current_item, 'api_item', None)
        command = item.light_control.set_color_temp(self.color_slider.value(), transition_time=2)

        self.queue_command('device_color_{}'.format(item.id), command)

    def device_toggled(self):
        current_item = self.device_list.currentItem()
        if current_item is None:
            return
        item = getattr(current_item, 'api_item', None)
        command = item.light_control.set_state(self.device_toggle.checkState() == Qt.CheckState.Checked)
        self.api(command)

    def group_toggled(self):
        current_item = self.group_list.currentItem()
        if current_item is None:
            return
        item = getattr(current_item, 'api_item', None)
        command = item.set_state(self.group_toggle.checkState() == Qt.CheckState.Checked)
        self.api(command)

    def settings_pressed(self):
        config = ConfigWindow(self.appctx, self)
        config.setWindowModality(Qt.ApplicationModal)
        config.exec_()

        # reload settings
        self.settings = config.settings

        # re-initialize window
        self.re_init()

    def queue_command(self, name, command):
        timer = self.timers.get(name, None)
        if timer is None:
            timer = QTimer()
            timer.setInterval(200)
            timer.setSingleShot(True)
            timer.timeout.connect(self.timeout)
            timer.start()

        setattr(timer, 'command', command)
        self.timers[name] = timer

    def timeout(self):
        remove = []
        for key, item in self.timers.items():
            if item.isActive() == False:
                cmd = getattr(item, 'command')
                self.api(cmd)
                remove.append(key)
        for key in remove:
            del self.timers[key]
