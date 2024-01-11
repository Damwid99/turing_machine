import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PyQt5.QtGui import QFont
from GUI.Touring_Gui import Ui_TuringMachine 
from modules.turingMachine import TuringMachine
from utils.utils import render_txt
from PyQt5.QtCore import QTimer



class MyMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_TuringMachine()
        self.ui.setupUi(self)

        self.ui.pushButton_2.setEnabled(False)
        self.ui.pushButton_3.setEnabled(False)
        self.ui.Stop_button.setEnabled(False)
        fixed_font = QFont("Courier New", 10)
        self.ui.plainTextEdit_2.setFont(fixed_font)
        fixed_width = 410  
        self.ui.plainTextEdit_2.setFixedWidth(fixed_width)
        self.ui.pushButton_3.clicked.connect(self.on_button_clicked)
        self.ui.pushButton_2.clicked.connect(self.step_forward_clicked)
        self.ui.Stop_button.clicked.connect(self.stop_func)

        self.machine = None

        #file uploading
        self.file_path = ''
        self.ui.pushButton_4.clicked.connect(self.upload_file)  
        # Add the following line to initialize continuous_printing


    def upload_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Text files (*.txt)")
        file_dialog.setFileMode(QFileDialog.ExistingFile) 

        self.restart_machine()
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.file_path = selected_files[0]
                self.ui.pushButton_2.setEnabled(True)
                self.ui.pushButton_3.setEnabled(True)
                self.ui.pushButton_4.setEnabled(False)
                self.ui.Stop_button.setEnabled(True)
                self.start_machine()
            else:
                QMessageBox.warning(self, "Warning", "No file selected.")
        else:
            QMessageBox.warning(self, "Warning", "File dialog canceled.")


    def start_machine(self):
        
        initial_word, states, final_states, initial_state, relations, tape_alphabet = render_txt(self.file_path)
        self.machine = TuringMachine(relations=relations, initial_state=initial_state, final_state=final_states, states=states, initial_word=initial_word)
        
        text_to_print = self.machine.print_tape(50)
        self.ui.plainTextEdit_2.appendPlainText(text_to_print)
        
        self.continuous_printing = False
        

    
    def stop_func(self):
        self.continuous_printing = False
        self.ui.pushButton_2.setEnabled(False)
        self.ui.pushButton_3.setEnabled(False)
        self.ui.Stop_button.setEnabled(True)
        self.restart_machine()


    def restart_machine(self):
        self.ui.pushButton_2.setEnabled(False)
        self.ui.pushButton_3.setEnabled(False)
        self.ui.pushButton_4.setEnabled(True)
        self.ui.Stop_button.setEnabled(True)

        self.machine = None
        self.file_path = ''
        self.ui.plainTextEdit_2.clear()
        self.ui.lineEdit_2.clear()
        self.ui.lineEdit_3.clear()


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
            self.ui.Stop_button.setEnabled(False)
            self.ui.pushButton_2.setEnabled(False)
            self.ui.pushButton_3.setEnabled(False)
            self.ui.pushButton_4.setEnabled(True)


def main():
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())



if __name__ == "__main__":
    main()
