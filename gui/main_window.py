import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextBrowser

class App(QMainWindow):

    def __init__(self):
        super().__init__()

        # Set window properties
        self.title = 'Serial Data Logger Display'
        self.left = 10
        self.top = 10
        self.width = 800
        self.height = 600

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Add a text browser to display data
        self.text_browser = QTextBrowser(self)
        self.text_browser.setGeometry(10, 10, 780, 580)

        # Show the GUI
        self.show()

    # You can use this method to update the text browser with new data
    def update_data(self, data):
        self.text_browser.append(data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
