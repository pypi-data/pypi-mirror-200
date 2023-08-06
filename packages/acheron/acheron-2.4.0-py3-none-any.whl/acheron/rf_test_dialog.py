import logging

from PySide6 import QtWidgets

from .ui_rf_test_dialog import Ui_RFTestDialog

logger = logging.getLogger(__name__)


class RFTestDialog(QtWidgets.QDialog, Ui_RFTestDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)
        self.extra_ui_setup()

    def extra_ui_setup(self):
        self.test_type_group = QtWidgets.QButtonGroup()
        self.test_type_group.addButton(self.fixedRadioButton)
        self.test_type_group.addButton(self.sweepRadioButton)

        self.test_mode_group = QtWidgets.QButtonGroup()
        self.test_mode_group.addButton(self.txCarrierRadioButton)
        self.test_mode_group.addButton(self.rxCarrierRadioButton)
        self.test_mode_group.addButton(self.txModulatedRadioButton)

        self.fixedChannel.editingFinished.connect(self.check_channels)
        self.startChannel.editingFinished.connect(self.check_channels)
        self.stopChannel.editingFinished.connect(self.check_channels)
        self.fixedChannel.valueChanged.connect(self.update_frequencies)
        self.startChannel.valueChanged.connect(self.update_frequencies)
        self.stopChannel.valueChanged.connect(self.update_frequencies)

        self.fixedRadioButton.setChecked(True)
        self.txCarrierRadioButton.setChecked(True)

    def check_channels(self, junk=None):
        fixed_channel = self.fixedChannel.value()
        if fixed_channel % 2 != 0:
            fixed_channel -= 1
            self.fixedChannel.setValue(fixed_channel)
        start_channel = self.startChannel.value()
        if start_channel % 2 != 0:
            start_channel -= 1
            self.startChannel.setValue(start_channel)
        stop_channel = self.stopChannel.value()
        if stop_channel % 2 != 0:
            stop_channel -= 1
            self.stopChannel.setValue(stop_channel)

    def update_frequencies(self):
        fixed_channel = self.fixedChannel.value()
        self.centerFreq.setText("{} MHz".format(fixed_channel + 2400))
        start_channel = self.startChannel.value()
        self.startFreq.setText("{} MHz".format(start_channel + 2400))
        stop_channel = self.stopChannel.value()
        self.stopFreq.setText("{} MHz".format(stop_channel + 2400))

    def get_results(self):
        params = {}
        if self.fixedRadioButton.isChecked():
            test_type = "fixed"
            params['channel'] = self.fixedChannel.value()
            params['duration'] = self.fixedDuration.value()
        else:  # self.sweepRadioButton.isChecked()
            test_type = "sweep"
            params['start'] = self.startChannel.value()
            params['stop'] = self.stopChannel.value()
            params['hop_interval'] = self.hopInterval.value()
            params['hop_count'] = self.hopCount.value()

        if self.txCarrierRadioButton.isChecked():
            params['mode'] = 0
        elif self.rxCarrierRadioButton.isChecked():
            params['mode'] = 1
        else:  # self.txModulatedRadioButton.isChecked()
            params['mode'] = 2

        return (test_type, params)
