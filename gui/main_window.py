from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QLabel, QMenuBar, QMenu, QVBoxLayout, QWidget
from PyQt5.QtGui import QColor
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Window title and size
        self.setWindowTitle('Solar Data Logger')
        self.setGeometry(100, 100, 600, 400)
        
        # Background color
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(40, 40, 60))  # Dark blue-ish color
        self.setPalette(p)

        # Main Layout
        layout = QVBoxLayout()

        # 1. Start and Stop Buttons
        self.startButton = QPushButton('Start')
        self.stopButton = QPushButton('Stop')
        layout.addWidget(self.startButton)
        layout.addWidget(self.stopButton)

        # 2. Text Area for last value read
        self.lastValueTextEdit = QTextEdit(self)
        self.lastValueTextEdit.setPlaceholderText('Last Value from Serial Port...')
        layout.addWidget(self.lastValueTextEdit)

        # 3. Text Area for port number
        self.portTextEdit = QTextEdit(self)
        self.portTextEdit.setPlaceholderText('Port Number...')
        layout.addWidget(self.portTextEdit)

        # 4. Status indicators
        self.statusLabel = QLabel("Status: Not Logging")
        layout.addWidget(self.statusLabel)

        # Date and Time Indicators
        self.utcLabel = QLabel("UTC Time: ")
        self.localTimeLabel = QLabel("Local Time: ")
        layout.addWidget(self.utcLabel)
        layout.addWidget(self.localTimeLabel)

        # 5. Text area for print messages
        self.logTextEdit = QTextEdit(self)
        layout.addWidget(self.logTextEdit)

        # Setting the central widget
        centralWidget = QWidget(self)
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        # 6. Menu bar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        settingsMenu = menubar.addMenu('Settings')

        # Sample menu items for file and settings
        openAction = fileMenu.addAction('Open')
        exitAction = fileMenu.addAction('Exit')
        portAction = settingsMenu.addAction('Set Port')
        directoryAction = settingsMenu.addAction('Set Directory')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
