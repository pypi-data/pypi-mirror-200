import logging
import os
import re
from xml.dom.minidom import getDOMImplementation

from PySide6 import QtCore, QtGui, QtWidgets

import asphodel
from hyperborea.preferences import read_bool_setting
from hyperborea.preferences import read_int_setting
from hyperborea.preferences import write_bool_setting

from .ui_connectivity_dialog import Ui_ConnectivityDialog

logger = logging.getLogger(__name__)


class ConnectivityDialog(QtWidgets.QDialog, Ui_ConnectivityDialog):
    def __init__(self, serial_number, channel_infos, parent=None):
        super().__init__(parent)

        self.serial_number = serial_number
        self.channel_infos = channel_infos
        self.settings = QtCore.QSettings()
        self.settings.beginGroup(self.serial_number)

        self.setting_names = {}  # setting_name: (checkbox, spinbox)

        self.setupUi(self)

        self.add_channel_check_boxes()
        self.read_settings()

        self.accepted.connect(self.write_settings)
        self.modbusDetails.clicked.connect(self.show_modbus_details)

    def add_channel_check_boxes(self):
        pattern = re.compile("Channel([0-9]+)_([0-9]+)_Port")

        sort_keys = {}

        for channel_info in self.channel_infos:
            for i, subchannel in enumerate(channel_info.subchannel_names):
                setting_name = "Channel{}_{}_Port".format(
                    channel_info.channel_id, i)
                checkbox = QtWidgets.QCheckBox(self)
                checkbox.setText(subchannel)
                spinbox = QtWidgets.QSpinBox(self)
                self.setting_names[setting_name] = (checkbox, spinbox)
                sort_keys[setting_name] = (channel_info.channel_id, i)

        # find settings that don't have an existing channel
        for setting_name in self.settings.allKeys():
            if setting_name in self.setting_names:
                continue

            result = pattern.fullmatch(setting_name)
            if result:
                channel_id = int(result.group(1))
                subchannel_id = int(result.group(2))

                checkbox = QtWidgets.QCheckBox(self)
                checkbox.setText("Channel {} Subchannel {}".format(
                    channel_id, subchannel_id))
                spinbox = QtWidgets.QSpinBox(self)
                self.setting_names[setting_name] = (checkbox, spinbox)
                sort_keys[setting_name] = (channel_id, subchannel_id)

        for setting_name in sorted(self.setting_names.keys(),
                                   key=sort_keys.get):
            checkbox, spinbox = self.setting_names[setting_name]
            label = QtWidgets.QLabel("Port:", parent=self)
            checkbox.setChecked(True)  # so the toggled signal will fire
            checkbox.toggled.connect(spinbox.setEnabled)
            checkbox.toggled.connect(label.setEnabled)

            spinbox.setMinimum(1)
            spinbox.setMaximum(65535)

            row = self.gridLayout.rowCount()
            self.gridLayout.addWidget(checkbox, row, 1)
            self.gridLayout.addWidget(label, row, 2)
            self.gridLayout.addWidget(spinbox, row, 3)

    def done(self, r):
        chosen_ports = set()

        for _setting_name, (checkbox, spinbox) in self.setting_names.items():
            if checkbox.isChecked():
                port = spinbox.value()
                if port in chosen_ports:
                    # show a warning
                    m = self.tr('Cannot have duplicate ports!')
                    QtWidgets.QMessageBox.warning(self, self.tr("Error"), m)
                    return
                else:
                    chosen_ports.add(port)
        super().done(r)

    def read_settings(self):
        modbus_enable = read_bool_setting(
            self.settings, "ModbusEnable", False)
        self.modbusCheckBox.setChecked(modbus_enable)
        modbus_unit_id = read_int_setting(self.settings, "ModbusUnitID", 1)
        self.unitId.setValue(modbus_unit_id)

        for setting_name, (checkbox, spinbox) in self.setting_names.items():
            port = read_int_setting(self.settings, setting_name, None)
            if not port:
                checkbox.setChecked(False)
                spinbox.setValue(12345)
            else:
                checkbox.setChecked(True)
                spinbox.setValue(port)

    def write_settings(self):
        modbus_enable = self.modbusCheckBox.isChecked()
        write_bool_setting(self.settings, "ModbusEnable", modbus_enable)
        modbus_unit_id = self.unitId.value()
        self.settings.setValue("ModbusUnitID", modbus_unit_id)

        for setting_name, (checkbox, spinbox) in self.setting_names.items():
            if checkbox.isChecked():
                port = spinbox.value()
                self.settings.setValue(setting_name, port)
            else:
                self.settings.remove(setting_name)

    def show_modbus_details(self):
        impl = getDOMImplementation()
        dt = impl.createDocumentType(
            "html",
            "-//W3C//DTD XHTML 1.0 Strict//EN",
            "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd",
        )
        dom = impl.createDocument("http://www.w3.org/1999/xhtml", "html", dt)
        html = dom.documentElement
        head = dom.createElement("head")
        html.appendChild(head)
        title = dom.createElement("title")
        title_string = f"{self.serial_number} Modbus Details"
        title.appendChild(dom.createTextNode(title_string))
        head.appendChild(title)
        body = dom.createElement("body")
        html.appendChild(body)
        h1 = dom.createElement("h1")
        h1.appendChild(dom.createTextNode(title_string))
        body.appendChild(h1)

        # create the table
        table = dom.createElement("table")
        table.setAttribute("border", "1")
        table.setAttribute("cellspacing", "0")
        table.setAttribute("cellpadding", "2")
        body.appendChild(table)

        # create the table header
        top_header_row = dom.createElement("tr")
        table.appendChild(top_header_row)
        bottom_header_row = dom.createElement("tr")
        table.appendChild(bottom_header_row)
        blank_th = dom.createElement("th")
        blank_th.setAttribute("rowspan", "2")
        top_header_row.appendChild(blank_th)

        # populate the table header
        for type_name in ["Mean (1s)", "Std Dev (1s)", "Instant"]:
            top_th = dom.createElement("th")
            top_th.appendChild(dom.createTextNode(type_name))
            top_th.setAttribute("colspan", "2")
            top_header_row.appendChild(top_th)
            float_th = dom.createElement("th")
            float_th.appendChild(dom.createTextNode("Float Registers"))
            bottom_header_row.appendChild(float_th)
            sixteen_bit_th = dom.createElement("th")
            sixteen_bit_th.appendChild(dom.createTextNode("16-Bit Register"))
            bottom_header_row.appendChild(sixteen_bit_th)

        float_unit_th = dom.createElement("th")
        float_unit_th.appendChild(dom.createTextNode("Float Units"))
        float_unit_th.setAttribute("rowspan", "2")
        top_header_row.appendChild(float_unit_th)

        sixteen_bit_range_th = dom.createElement("th")
        sixteen_bit_range_th.appendChild(dom.createTextNode("16-bit Range"))
        sixteen_bit_range_th.setAttribute("colspan", "2")
        top_header_row.appendChild(sixteen_bit_range_th)
        mean_and_instant_th = dom.createElement("th")
        mean_and_instant_th.appendChild(dom.createTextNode("Mean & Instant"))
        bottom_header_row.appendChild(mean_and_instant_th)
        std_dev_th = dom.createElement("th")
        std_dev_th.appendChild(dom.createTextNode("Std Dev"))
        bottom_header_row.appendChild(std_dev_th)

        # generate the device rows
        index = 1
        for channel_info in self.channel_infos:
            unit = channel_info.channel.unit_type
            res = channel_info.channel.resolution
            uf_base = asphodel.nativelib.create_unit_formatter(
                unit, 1.0, 1.0, 1.0)

            min_mean = "0x0000: {}".format(asphodel.format_value_utf8(
                unit, res, channel_info.channel.minimum))
            max_mean = "0xFFFF: {}".format(asphodel.format_value_utf8(
                unit, res, channel_info.channel.maximum))
            min_std = "0x0000: {}".format(asphodel.format_value_utf8(
                unit, 1.0, 0.0))
            std_range = (channel_info.channel.maximum -
                         channel_info.channel.minimum) / 2.0
            max_std = "0xFFFF: {}".format(asphodel.format_value_utf8(
                unit, res, std_range))

            for subchannel_name in channel_info.subchannel_names:
                tr = dom.createElement("tr")
                table.appendChild(tr)
                th = dom.createElement("th")
                th.appendChild(dom.createTextNode(subchannel_name))
                tr.appendChild(th)

                for i in range(3):
                    float_index = 30000 + (i * 2000) + index
                    sixteen_bit_index = 31000 + (i * 2000) + index

                    float_td = dom.createElement("td")
                    float_td.appendChild(dom.createTextNode(
                        "{}-{}".format(float_index, float_index + 1)))
                    tr.appendChild(float_td)
                    sixteen_bit_td = dom.createElement("td")
                    sixteen_bit_td.appendChild(dom.createTextNode(
                        f"{sixteen_bit_index}"))
                    tr.appendChild(sixteen_bit_td)

                float_unit_td = dom.createElement("td")
                float_unit_td.appendChild(dom.createTextNode(
                    uf_base.unit_utf8))
                tr.appendChild(float_unit_td)

                mean_range_td = dom.createElement("td")
                mean_range_td.appendChild(dom.createTextNode(min_mean))
                mean_range_td.appendChild(dom.createElement("br"))
                mean_range_td.appendChild(dom.createTextNode(max_mean))
                tr.appendChild(mean_range_td)

                std_range_td = dom.createElement("td")
                std_range_td.appendChild(dom.createTextNode(min_std))
                std_range_td.appendChild(dom.createElement("br"))
                std_range_td.appendChild(dom.createTextNode(max_std))
                tr.appendChild(std_range_td)

                index += 2

        outdir = QtCore.QStandardPaths.writableLocation(
            QtCore.QStandardPaths.AppLocalDataLocation)
        outfile = os.path.join(outdir, f"{self.serial_number}_Modbus.html")

        try:
            with open(outfile, "wb") as f:
                f.write(dom.toxml(encoding="UTF-8"))
        except Exception:
            m = self.tr('Error creating file!')
            QtWidgets.QMessageBox.critical(self, self.tr("Error"), m)
            logger.exception(m)
            return

        url = QtCore.QUrl.fromLocalFile(outfile)
        QtGui.QDesktopServices.openUrl(url)
