from PyQt5.QtWidgets import QApplication

from gui import SimpleImageEditor

import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = SimpleImageEditor()
    MainWindow.show()
    sys.exit(app.exec_())