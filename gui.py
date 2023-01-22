from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import pyttsx3
import app


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.title = "SIS - Sign Interpretation Software"
        self.setWindowTitle(self.title)
        self.icon = QIcon('SIS-1.png')
        self.setWindowIcon(self.icon)
        self.setGeometry(0, 0, 1200, 900)
        self.move(420, 0)
        self.setStyleSheet("QMainWindow"
                           "{"
                           "background-color: rgb(48,51,51);"
                           "}"
                           )

        self.layout = QVBoxLayout(self)

        self.font = QFont()
        self.font.setFamily("Segoe UI Bold")
        self.font.setPointSize(12)

        self.font2 = QFont()
        self.font2.setFamily("Segoe UI SemiBold")
        self.font2.setPointSize(16)

        self.textarea = QTextEdit(self)

        self.textarea.setReadOnly(False) #make readonly
        self.textarea.setGeometry(120, 30, 961, 641)
        self.textarea.setFont(self.font2)

        self.textarea.setStyleSheet("QTextEdit"
                                    "{"
                                    "background-color: rgb(245,245,245); "
                                    "color: black"
                                    "}")
        with open('./gen/file.txt', 'r') as f:
            text = f.readline()
        self.textarea.setText(text)

        # self.generate = QPushButton("Generate", self)
        # self.generate.setGeometry(20, 800, 180, 65)
        # self.generate.clicked.connect(self.textset)
        # self.generate.setFont(self.font)

        # self.generate.setStyleSheet("QPushButton"
        #                             "{"
        #                             "border-color : rgb(255, 255, 255);"
        #                             "border-width : 5px;"
        #                             "color: white;"
        #                             "background-color : orange;"
        #                             "border-radius : 12px"
        #                             "}"
        #                             "QPushButton::pressed"
        #                             "{"
        #                             "background-color : rgb(4, 136, 166);"

        #                             "}")

        self.t2s = QPushButton("Dictate", self)
        self.t2s.setGeometry(1000, 800, 180, 65)
        self.font = QFont()
        self.font.setFamily("Segoe UI Semilight")
        self.font.setPointSize(12)
        self.t2s.setFont(self.font)
        self.t2s.clicked.connect(self.text2speech)
        self.t2s.setStyleSheet("QPushButton"
                               "{"
                               "border-color : rgb(255, 255, 255);"
                               "border-width : 5px;"
                               "color: white;"
                               "background-color : orange;"
                               "border-radius : 12px"
                               "}"
                               "QPushButton::pressed"
                               "{"
                               "background-color : rgb(4, 136, 166);"

                               "}")

    def text2speech(self):
        try:
            engine = pyttsx3.init()
            text2s = self.textarea.toPlainText()

            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[1].id)
            engine.setProperty('rate', 120)
            engine.say(text2s)

            engine.runAndWait()
        except Exception as s:
            self.critical_dialog(s)

    def critical_dialog(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()


if __name__ == "__main__":
    with open('./gen/file.txt','w') as f:
        f.write('')
    # proc = subprocess.Popen(['D:\Code\SDK\Python\Python310\python.exe', 'app.py'], stdout=subprocess.PIPE)
    app.main()
    appi = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    appi.setStyle('Fusion')

    sys.exit(appi.exec_())
