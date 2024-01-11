# from utils.utils import render_txt
# from modules.turingMachine import TuringMachine


# initial_word, states, final_states, initial_state, relations, tape_alphabet = render_txt('./in.txt')
# machine = TuringMachine(relations=relations, initial_state=initial_state, final_state=final_states, states=states,
#                         initial_word=initial_word)

# machine.run()    

import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QFont
from Touring_Gui import Ui_MainWindow 
from modules.turingMachine import TuringMachine
from utils.utils import render_txt
from PyQt5.QtCore import QTimer



class MyMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton_2.setEnabled(False)
        self.ui.pushButton_3.setEnabled(False)
        fixed_font = QFont("Courier New", 10)
        self.ui.plainTextEdit_2.setFont(fixed_font)
        fixed_width = 410  
        self.ui.plainTextEdit_2.setFixedWidth(fixed_width)

        self.machine = None

        #file uploading
        self.file_path = ''
        self.ui.pushButton_4.clicked.connect(self.upload_file)


    def upload_file(self):
        self.file_path = self.ui.lineEdit.text()
        if not os.path.exists(self.file_path):
            QMessageBox.warning(self, "File Not Found", f"The file '{self.file_path}' does not exist.")
            self.file_path = ''
        else:
            self.ui.pushButton_2.setEnabled(True)
            self.ui.pushButton_3.setEnabled(True)
            QMessageBox.information(self, "File uploaded", f"The file '{self.file_path}' was uploaded succesfully.\nPress play or step forward button to start.")
            self.start_machine()


    def start_machine(self):
        
        initial_word, states, final_states, initial_state, relations, tape_alphabet = render_txt(self.file_path)
        self.machine = TuringMachine(relations=relations, initial_state=initial_state, final_state=final_states, states=states, initial_word=initial_word)
        
        text_to_print = self.machine.print_tape(50)
        self.ui.plainTextEdit_2.appendPlainText(text_to_print)
        self.ui.pushButton_3.clicked.connect(self.on_button_clicked)
        self.ui.pushButton_2.clicked.connect(self.step_forward_clicked)
        self.continuous_printing = False


    def on_button_clicked(self):
        if not self.continuous_printing:
            self.continuous_printing = True
            self.update_text_continuously()
            self.ui.pushButton_2.setEnabled(False)
        else:
            self.continuous_printing = False
            self.ui.pushButton_2.setEnabled(True)


    def step_forward_clicked(self):
        tape_text = self.machine.print_tape(50)
        relation_to_show = self.machine.update_state()

        self.ui.plainTextEdit_2.clear()
        self.ui.plainTextEdit_2.appendPlainText(tape_text)
        self.ui.lineEdit_2.clear()
        self.ui.lineEdit_2.setText(str(relation_to_show))
        if self.machine.message:
            self.ui.lineEdit_3.setText(self.machine.message)
            QTimer.singleShot(1700, self.clear_message_box)
        self.check_if_in_final_state(tape_text)



    def update_text_continuously(self):
        if self.continuous_printing:
            text_to_print = self.machine.print_tape(50)
            relation_to_show = self.machine.update_state()
            self.ui.plainTextEdit_2.clear()
            self.ui.plainTextEdit_2.appendPlainText(text_to_print)
            self.ui.lineEdit_2.clear()
            self.ui.lineEdit_2.setText(str(relation_to_show))
            if self.machine.message:
                self.ui.lineEdit_3.setText(self.machine.message)
                QTimer.singleShot(1700, self.clear_message_box)
            # You can adjust the time.sleep value to control the delay between updates.
            # Here, we're using a short delay of 100 milliseconds.
            self.check_if_in_final_state(text_to_print)
            QTimer.singleShot(100, self.update_text_continuously)


    def clear_message_box(self):
        self.ui.lineEdit_3.clear()


    def check_if_in_final_state(self, previous_text):
        if (self.machine.actual_state in self.machine.final_state) or (self.machine.message == "No available states."):
            self.continuous_printing =False
            self.ui.pushButton_2.setEnabled(False)
            self.ui.pushButton_3.setEnabled(False)
            final_text = '\nInitial word:\n'
            final_text += ''.join(self.machine.initial_word) + '\n'
            final_text += 'Final word:\n'
            final_text += ''.join(self.machine.tape).strip('#') + '\n'
            final_text += 'Calculating length:\n'
            final_text += str(self.machine.calculating_length)
            previous_text += final_text
            self.ui.plainTextEdit_2.clear()
            self.ui.plainTextEdit_2.appendPlainText(previous_text)
            if self.machine.message:
                self.ui.lineEdit_3.setText(self.machine.message)
            else:
                self.ui.lineEdit_3.setText('Ended succesfully.')
            QTimer.singleShot(5000, self.clear_message_box)



def main():
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())



if __name__ == "__main__":
    main()
