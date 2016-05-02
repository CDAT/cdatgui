from PySide import QtCore, QtGui


class BaseSaveWindowWidget(QtGui.QWidget):
    savePressed = QtCore.Signal(str)

    def __init__(self):
        super(BaseSaveWindowWidget, self).__init__()

        self.object = None
        self.preview = None
        self.dialog = QtGui.QInputDialog()
        self.dialog.setModal(QtCore.Qt.ApplicationModal)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        shortcut = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self)
        shortcut.activated.connect(self.close)

        # Layout to add new elements
        self.vertical_layout = QtGui.QVBoxLayout()

        # Save and Cancel Buttons
        cancel_button = QtGui.QPushButton()
        cancel_button.setText("Cancel")
        cancel_button.clicked.connect(self.close)

        saveas_button = QtGui.QPushButton()
        saveas_button.setText("Save As")
        saveas_button.clicked.connect(self.saveAs)

        self.save_button = QtGui.QPushButton()
        self.save_button.setText("Save")
        self.save_button.clicked.connect(self.save)

        save_cancel_row = QtGui.QHBoxLayout()
        save_cancel_row.addWidget(cancel_button)
        save_cancel_row.addWidget(saveas_button)
        save_cancel_row.addWidget(self.save_button)
        save_cancel_row.insertStretch(1, 1)

        # Set up vertical_layout
        self.vertical_layout.addLayout(save_cancel_row)
        self.setLayout(self.vertical_layout)

    def setPreview(self, preview):
        if self.preview:
            self.vertical_layout.removeWidget(self.preview)
            self.preview.deleteLater()

        self.preview = preview
        self.vertical_layout.insertWidget(0, self.preview)

    def saveAs(self):

        self.win = self.dialog

        self.win.setLabelText("Enter New Name:")
        self.win.accepted.connect(self.save)

        self.win.show()
        self.win.raise_()

    def save(self):

        try:
            name = self.win.textValue()
            self.win.close()
            self.win.deleteLater()
        except:
            name = self.object.name

        self.savePressed.emit(name)
        self.close()

    def setSaveDialog(self, dialog):
        self.dialog = dialog


class BaseOkWindowWidget(QtGui.QWidget):
    okPressed = QtCore.Signal()

    def __init__(self):
        super(BaseOkWindowWidget, self).__init__()

        self.object = None
        self.preview = None
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        shortcut = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self)
        shortcut.activated.connect(self.close)

        # Layout to add new elements
        self.vertical_layout = QtGui.QVBoxLayout()

        # Save and Cancel Buttons
        cancel_button = QtGui.QPushButton()
        cancel_button.setText("Cancel")
        cancel_button.clicked.connect(lambda: self.close())

        ok_button = QtGui.QPushButton()
        ok_button.setText("OK")
        ok_button.clicked.connect(self.okClicked)

        ok_cancel_row = QtGui.QHBoxLayout()
        ok_cancel_row.addWidget(cancel_button)
        ok_cancel_row.addWidget(ok_button)
        ok_cancel_row.insertStretch(1, 1)

        # Set up vertical_layout
        self.vertical_layout.addLayout(ok_cancel_row)
        self.setLayout(self.vertical_layout)

    def setPreview(self, preview):
        if self.preview:
            self.vertical_layout.removeWidget(self.preview)
            self.preview.deleteLater()

        self.preview = preview
        self.vertical_layout.insertWidget(0, self.preview)

    def okClicked(self):
        self.okPressed.emit()
        self.close()
