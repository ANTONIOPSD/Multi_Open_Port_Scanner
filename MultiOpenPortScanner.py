from PyQt6.QtCore import QThread, pyqtSignal, QLocale, QRect, Qt, QMetaObject, QCoreApplication
from PyQt6.QtGui import QFont, QCursor
from PyQt6.QtWidgets import QTabWidget, QLineEdit, QWidget, QLabel, QProgressBar, QCommandLinkButton, QTextEdit, QTabWidget, QPushButton, QApplication, QDialog, QSpinBox, QMessageBox
from threading import Thread
import time
import socket
import webbrowser

class ScanThread(QThread):
    signal_percentage = pyqtSignal(int)
    signal_scanned_port = pyqtSignal(str)
    signal_open_port = pyqtSignal(str)
    signal_end_scan = pyqtSignal(int)
    
    def run(self):
        global ports_to_scan
        for port in port_list:
            if "-" in str(port):
                port = port.split("-")
                port1 = int(port[0])
                port2 = int(port[1]) + 1

                if port1 >= 65535:
                    port1 = 65535
                if port2 >= 65535:
                    port2 = 65535

                for port_r in range(port1, port2):
                    ports_to_scan.append(str(port_r))

            else:
                if int(port) >= 65535:
                    port = "65535"
                ports_to_scan.append(port)

        ports_to_scan = list(dict.fromkeys(ports_to_scan))
        ports_to_scan.sort(key=int)
        total_ports = len(ports_to_scan)
        global cancel_scan
        cancel_scan = False
        for idx, port in enumerate(ports_to_scan):
            if cancel_scan != True:
                def scan_port(host, port):
                    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    location = (host, port)
                    percentage = int(((idx+1)/total_ports)*100)
                    self.signal_percentage.emit(percentage)
                    self.signal_scanned_port.emit(port)
                    try:
                        result = socket.create_connection((location), timeout=2)
                    except:
                        if cancel_scan == True:
                            self.signal_percentage.emit(0)
                        a_socket.close()
                        return
                    if result:
                        self.signal_open_port.emit(port)
                        if cancel_scan == True:
                            self.signal_percentage.emit(0)
                        a_socket.close()
                        return
            
                Thread(target=scan_port, args=(host, port)).start()
                if scan_delay > 0:
                    time.sleep(scan_delay/1000)
            else:
                break
        end = 1
        self.signal_end_scan.emit(end)   
            
class Ui_dialog(object):
    def setupUi(self, dialog):
        dialog.setObjectName("dialog")
        dialog.setFixedSize(600,540)
        font = QFont()
        font.setPointSize(14)
        dialog.setFont(font)
        dialog.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        dialog.setWhatsThis("")
        dialog.setAccessibleName("")
        dialog.setAutoFillBackground(False)
        dialog.setLocale(QLocale(QLocale.Language.English, QLocale.Country.UnitedStates))
        dialog.setSizeGripEnabled(False)
        dialog.setModal(False)
        self.tabWidget = QTabWidget(dialog)
        self.tabWidget.setGeometry(QRect(-1, 0, 601, 536))
        self.tabWidget.setFont(font)
        self.tabWidget.setTabShape(QTabWidget.TabShape.Rounded)
        self.tabWidget.setUsesScrollButtons(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.ScannerTab = QWidget()
        self.ScannerTab.setObjectName("ScannerTab")
        self.PortsInput = QLineEdit(self.ScannerTab)
        self.PortsInput.setGeometry(QRect(5, 75, 586, 30))
        self.PortsInput.setFont(font)
        self.PortsInput.setText("")
        self.PortsInput.setEchoMode(QLineEdit.EchoMode.Normal)
        self.PortsInput.setClearButtonEnabled(True)
        self.PortsInput.setObjectName("PortsInput")
        self.HostLabel = QLabel(self.ScannerTab)
        self.HostLabel.setGeometry(QRect(5, 0, 586, 21))
        self.HostLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.HostLabel.setObjectName("HostLabel")
        self.ScanButton = QPushButton(self.ScannerTab)
        self.ScanButton.setGeometry(QRect(240, 425, 100, 30))
        self.ScanButton.setCheckable(False)
        self.ScanButton.setAutoDefault(True)
        self.ScanButton.setDefault(False)
        self.ScanButton.setFlat(False)
        self.ScanButton.setObjectName("ScanButton")
        self.CancelButton = QPushButton(self.ScannerTab)
        self.CancelButton.setGeometry(QRect(240, 425, 100, 30))
        self.CancelButton.setCheckable(False)
        self.CancelButton.setAutoDefault(True)
        self.CancelButton.setDefault(False)
        self.CancelButton.setFlat(False)
        self.CancelButton.setObjectName("CancelButton")
        self.CancelButton.setVisible(False)
        self.ScannedLabel = QLabel(self.ScannerTab)
        self.ScannedLabel.setGeometry(QRect(5, 100, 281, 30))
        self.ScannedLabel.setTextFormat(Qt.TextFormat.PlainText)
        self.ScannedLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ScannedLabel.setObjectName("ScannedLabel")
        self.ScannedList = QTextEdit(self.ScannerTab)
        self.ScannedList.setEnabled(True)
        self.ScannedList.setGeometry(QRect(5, 130, 281, 291))
        self.ScannedList.setFont(font)
        self.ScannedList.setInputMethodHints(Qt.InputMethodHint.ImhNone)
        self.ScannedList.setReadOnly(True)
        self.ScannedList.setOverwriteMode(False)
        self.ScannedList.setAcceptRichText(False)
        self.ScannedList.setObjectName("ScannedList")
        self.OpenList = QTextEdit(self.ScannerTab)
        self.OpenList.setEnabled(True)
        self.OpenList.setGeometry(QRect(295, 130, 296, 291))
        self.OpenList.setFont(font)
        self.OpenList.setInputMethodHints(Qt.InputMethodHint.ImhNone)
        self.OpenList.setReadOnly(True)
        self.OpenList.setOverwriteMode(False)
        self.OpenList.setAcceptRichText(False)
        self.OpenList.setObjectName("OpenList")
        self.IpInput = QLineEdit(self.ScannerTab)
        self.IpInput.setGeometry(QRect(5, 20, 586, 30))
        self.DelayBox = QSpinBox(self.ScannerTab)
        self.DelayBox.setGeometry(QRect(6, 430, 66, 22))
        self.DelayBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.DelayBox.setMaximum(9999)
        self.DelayBox.setProperty("value", 1)
        self.DelayBox.setObjectName("DelayBox")
        self.DelayLabel = QLabel(self.ScannerTab)
        self.DelayLabel.setGeometry(QRect(75, 430, 146, 21))
        self.DelayLabel.setFont(font)
        self.DelayLabel.setTextFormat(Qt.TextFormat.PlainText)
        self.DelayLabel.setWordWrap(True)
        self.DelayLabel.setOpenExternalLinks(False)
        self.DelayLabel.setObjectName("DelayLabel")
        self.IpInput.setFont(font)
        self.IpInput.setInputMethodHints(Qt.InputMethodHint.ImhNone)
        self.IpInput.setText("")
        self.IpInput.setEchoMode(QLineEdit.EchoMode.Normal)
        self.IpInput.setDragEnabled(False)
        self.IpInput.setClearButtonEnabled(True)
        self.IpInput.setObjectName("IpInput")
        self.PortsToScanLabel = QLabel(self.ScannerTab)
        self.PortsToScanLabel.setGeometry(QRect(5, 55, 586, 21))
        self.PortsToScanLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.PortsToScanLabel.setObjectName("PortsToScanLabel")
        self.ProgressBar = QProgressBar(self.ScannerTab)
        self.ProgressBar.setEnabled(False)
        self.ProgressBar.setGeometry(QRect(5, 459, 586, 36))
        self.ProgressBar.setFont(font)
        self.ProgressBar.setDisabled(True)
        self.ProgressBar.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.ProgressBar.setAccessibleName("")
        self.ProgressBar.setAutoFillBackground(False)
        self.ProgressBar.setMaximum(100)
        self.ProgressBar.setProperty("value", 0)
        self.ProgressBar.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.ProgressBar.setTextVisible(False)
        self.ProgressBar.setOrientation(Qt.Orientation.Horizontal)
        self.ProgressBar.setInvertedAppearance(False)
        self.ProgressBar.setTextDirection(QProgressBar.Direction.TopToBottom)
        self.ProgressBar.setObjectName("ProgressBar")
        self.OpenLabel = QLabel(self.ScannerTab)
        self.OpenLabel.setGeometry(QRect(295, 100, 296, 30))
        self.OpenLabel.setTextFormat(Qt.TextFormat.PlainText)
        self.OpenLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.OpenLabel.setObjectName("OpenLabel")
        self.tabWidget.addTab(self.ScannerTab, "")
        self.AboutTab = QWidget()
        self.AboutTab.setObjectName("AboutTab")
        self.AuthorLabel = QLabel(self.AboutTab)
        self.AuthorLabel.setGeometry(QRect(210, 185, 146, 66))
        self.AuthorLabel.setObjectName("AuthorLabel")
        self.ProjectLinkButton = QCommandLinkButton(self.AboutTab)
        self.ProjectLinkButton.setGeometry(QRect(100, 245, 350, 40))
        self.ProjectLinkButton.setObjectName("ProjectLinkButton")
        self.tabWidget.addTab(self.AboutTab, "")
        self.retranslateUi(dialog)
        self.tabWidget.setCurrentIndex(0)
        QMetaObject.connectSlotsByName(dialog)
        self.ScanButton.clicked.connect(self.start_scan)
        self.CancelButton.clicked.connect(self.cancel_scan)
        self.ProjectLinkButton.clicked.connect(self.open_url)
        self.PortsInput.textChanged.connect(self.check_input_ports)
        self.DelayBox.valueChanged.connect(self.check_delay_value)

    global allowed_port_characters
    global not_allowed_port_characters
    
    allowed_port_characters = ["0","1","2","3","4","5","6","7","8","9","-"," "]
    not_allowed_port_characters = ["--", "---", "- ", " - "]

    def check_delay_value(self):
        if self.DelayBox.value() == 0:
            warning_font = QFont()
            warning_font.setPointSize(12)
            delay_warning = QMessageBox()
            delay_warning.setIcon(QMessageBox.Icon.Warning)
            delay_warning.setFont(warning_font)
            delay_warning.setText('Delay between each port scan too low !!!')
            delay_warning.setInformativeText("Some servers will drop some of the scans and some open ports won't be detected.")
            delay_warning.setWindowTitle("Warning")
            delay_warning.setStandardButtons(QMessageBox.StandardButton.Ok)
            delay_warning.exec()

    def check_input_ports(self):
        ports = self.PortsInput.text()
        splitted_ports = ports.split()

        if ports.startswith("-") or ports.startswith(" "):
            ports = ports[:-1]
            ports = ""
            self.PortsInput.setText(ports)
            
        for splitted in splitted_ports:
            dash_count = splitted.lower().count('-')
            if splitted.startswith("-"):
                ports = ports[:-1]
                self.PortsInput.setText(ports)

            if dash_count >= 2:
                ports = ports[:-1]
                ports = ' '.join(ports.split())
                self.PortsInput.setText(ports)

        for x in ports:
            for not_allowed in not_allowed_port_characters:
                if not_allowed in ports:
                    ports = ports.replace(not_allowed, "-")
                    ports = ' '.join(ports.split())
                    self.PortsInput.setText(ports)

            if x not in allowed_port_characters:
                ports = ports.replace(x, "")
                ports = ' '.join(ports.split())
                self.PortsInput.setText(ports)

    def open_url(self):
        browser = webbrowser.get()
        browser.open_new(self.ProjectLinkButton.text())
    
    def start_scan(self):
        global port_list
        global ports_to_scan
        global host
        global scan_delay
        scan_delay = self.DelayBox.value()
        if self.IpInput.text() != "":
            if self.PortsInput.text() == "":
                self.PortsInput.setText("1-65535")
            self.ScanButton.setDisabled(True)
            self.ScanButton.setVisible(False)
            self.CancelButton.setDisabled(False)
            self.CancelButton.setVisible(True)
            self.IpInput.setDisabled(True)
            self.PortsInput.setDisabled(True)
            self.ProgressBar.setDisabled(False)
            self.ProgressBar.setCursor(QCursor(Qt.CursorShape.WaitCursor))
            self.ProgressBar.setTextVisible(True)
            self.ProgressBar.setValue(0)
            self.DelayBox.setDisabled(True)
            self.ScannedList.clear()
            self.OpenList.clear()
            ports_to_scan = []
            host = self.IpInput.text()
            host = ''.join(host.split())
            ports = self.PortsInput.text()
            ports = ' '.join(ports.split())
            port_list = ports.split()
            self.IpInput.setText(host)
            self.PortsInput.setText(ports)
            self.scan = ScanThread()
            self.scan.signal_percentage.connect(self.update_progressbar)
            self.scan.signal_scanned_port.connect(self.update_scanned_ports)
            self.scan.signal_open_port.connect(self.update_open_ports)
            self.scan.signal_end_scan.connect(self.end_scan)
            self.scan.start()
    
    def cancel_scan(self):
        global cancel_scan
        cancel_scan = True

    def update_progressbar(self, percentage):
        self.ProgressBar.setValue(percentage)
    
    def update_scanned_ports(self, port):
        self.ScannedList.append(port)
    
    def update_open_ports(self, port):
        self.OpenList.append(port)
        open_port_list = self.OpenList.toPlainText()
        open_port_list = open_port_list.split()
        open_port_list.sort(key=int)
        self.OpenList.setPlainText("\n". join(open_port_list))

    def end_scan(self):
        self.ScanButton.setVisible(True)
        self.ScanButton.setDisabled(False)
        self.IpInput.setDisabled(False)
        self.PortsInput.setDisabled(False)
        self.CancelButton.setVisible(False)
        self.CancelButton.setDisabled(True)
        self.DelayBox.setDisabled(False)
        self.ProgressBar.setDisabled(True)
        self.ProgressBar.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

    def retranslateUi(self, dialog):
        _translate = QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "Multi Open Port Scanner By ANTONIOPS"))
        self.PortsInput.setPlaceholderText(_translate("dialog", "20-25 80 443 100-200 | Empty = Scan all ports"))
        self.HostLabel.setText(_translate("dialog", "Host"))
        self.ScanButton.setText(_translate("dialog", "Scan"))
        self.CancelButton.setText(_translate("dialog", "Cancel"))
        self.ScannedLabel.setText(_translate("dialog", "Scanned Ports"))
        self.ScannedList.setPlaceholderText(_translate("dialog", "Scanned ports will appear here."))
        self.OpenList.setPlaceholderText(_translate("dialog", "Open ports will appear here."))
        self.IpInput.setPlaceholderText(_translate("dialog", "Domain or IP"))
        self.PortsToScanLabel.setText(_translate("dialog", "Ports to scan"))
        self.ProgressBar.setFormat(_translate("dialog", "%p%"))
        self.OpenLabel.setText(_translate("dialog", "Open ports"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ScannerTab), _translate("dialog", "Scanner"))
        self.DelayLabel.setText(_translate("dialog", "Scan delay (ms)"))
        self.AuthorLabel.setText(_translate("dialog", "By ANTONIOPSD"))
        self.ProjectLinkButton.setText(_translate("dialog", "https://github.com/ANTONIOPSD"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.AboutTab), _translate("dialog", "About"))

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    dialog = QDialog()
    ui = Ui_dialog()
    ui.setupUi(dialog)
    dialog.show()
    sys.exit(app.exec())
