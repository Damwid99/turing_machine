import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PyQt5.QtGui import QFont, QFontMetrics
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
        self.font_metrics= QFontMetrics(fixed_font)

        self.machine = None
        self.is_final_state = False
        self.is_ended =False

        self.actual_config = None
        self.config_text_to_save = ''
        #file uploading
        self.file_path = ''
        self.ui.pushButton_4.clicked.connect(self.upload_file)  
        # Add the following line to initialize continuous_printing

        self.approx_columns = int(fixed_width/self.font_metrics.width('#'))-5

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
        
        text_to_print = self.machine.print_tape(self.approx_columns)
        self.ui.plainTextEdit_2.appendPlainText(text_to_print)
        
        self.continuous_printing = False
        

    
    def stop_func(self):
        self.continuous_printing = False
        self.ui.pushButton_2.setEnabled(False)
        self.ui.pushButton_3.setEnabled(False)
        self.ui.Stop_button.setEnabled(True)
        self.config_text_to_save += 'Machine has been stopped'
        self.save_output()
        self.restart_machine()


    def restart_machine(self):
        self.ui.pushButton_2.setEnabled(False)
        self.ui.pushButton_3.setEnabled(False)
        self.ui.pushButton_4.setEnabled(True)
        self.ui.Stop_button.setEnabled(True)

        self.machine = None
        self.file_path = ''
        self.actual_config = ''
        self.config_text_to_save = ''
        self.ui.plainTextEdit_2.clear()
        self.ui.plainTextEdit_5.clear()
        self.ui.lineEdit_3.clear()
        self.is_ended = False
        self.is_final_state =False


    def on_button_clicked(self):
        if not self.continuous_printing:
            self.continuous_printing = True
            self.update_text_continuously()
            self.ui.pushButton_2.setEnabled(False)
        else:
            self.continuous_printing = False
            self.ui.pushButton_2.setEnabled(True)


    def step_forward_clicked(self):
        tape_text = self.machine.print_tape(self.approx_columns)
        self.check_if_in_final_state(tape_text)
        self.update_actual_config()
        relation_to_show = self.machine.update_state()
        if (self.machine.actual_state in self.machine.final_state):
                self.is_final_state=True
        if not self.is_ended:
            self.ui.plainTextEdit_2.clear()
            self.ui.plainTextEdit_2.appendPlainText(tape_text)
            self.ui.plainTextEdit_5.clear()
            self.ui.plainTextEdit_5.appendPlainText(self.actual_config)
            if self.machine.message:
                self.ui.lineEdit_3.setText(self.machine.message)
                QTimer.singleShot(1700, self.clear_message_box)
        else:
            self.is_ended = False

    def update_actual_config(self):
        if self.machine.calculating_length <5000:
            conif = "("+str(self.machine.actual_state)
            left_side = self.machine.tape[:self.machine.tape_index]
            right_side = self.machine.tape[self.machine.tape_index:]
            if all( v == '#' for v in left_side):
                left_side='#'
            else:
                left_side = ''.join(left_side).lstrip('#')
            if all( v == '#' for v in right_side):
                right_side='#'
            else:
                right_side = ''.join(right_side).rstrip('#')

            self.actual_config = "("+str(self.machine.actual_state) + ', ' + left_side + ', ' + right_side + ')' +'\n'
            self.config_text_to_save +=self.actual_config
        elif self.machine.calculating_length > 5000 and self.actual_config != 'Calculating length bigger than 5000':
            self.actual_config = 'Calculating length bigger than 5000'
            self.config_text_to_save += self.actual_config
        

    def update_text_continuously(self):
        if self.continuous_printing:
            text_to_print = self.machine.print_tape(self.approx_columns)
            self.check_if_in_final_state(text_to_print)
            self.update_actual_config()
            relation_to_show = self.machine.update_state()
            if (self.machine.actual_state in self.machine.final_state):
                self.is_final_state=True
            if not self.is_ended:
                self.ui.plainTextEdit_2.clear()
                self.ui.plainTextEdit_2.appendPlainText(text_to_print)
                self.ui.plainTextEdit_5.clear()
                self.ui.plainTextEdit_5.appendPlainText(self.actual_config)
                if self.machine.message:
                    self.ui.lineEdit_3.setText(self.machine.message)
                    QTimer.singleShot(1600, self.clear_message_box)
                
                QTimer.singleShot(1, self.update_text_continuously)
            else:
                self.is_ended = False


    def clear_message_box(self):
        self.ui.lineEdit_3.clear()


    def check_if_in_final_state(self, previous_text):
        if (self.is_final_state==True) or (self.machine.message == "No available states."):
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
            self.update_actual_config()
            self.ui.plainTextEdit_5.clear()
            self.ui.plainTextEdit_5.appendPlainText(self.actual_config)

            if self.is_final_state==True:
                self.ui.lineEdit_3.setText('Ended succesfully.')
                self.is_ended=True
                self.config_text_to_save += 'Ended succesfully'
            else:
                self.ui.lineEdit_3.setText(self.machine.message)
                self.config_text_to_save += f'{self.machine.message}'
            QTimer.singleShot(5000, self.clear_message_box)
            self.save_output()
            
            self.ui.Stop_button.setEnabled(False)
            self.ui.pushButton_2.setEnabled(False)
            self.ui.pushButton_3.setEnabled(False)
            self.ui.pushButton_4.setEnabled(True)
        

    def save_output(self):
        last_slash_index = self.file_path.rfind('/')

        if last_slash_index != -1:
            file_name = self.file_path[last_slash_index + 1:]
        else:
            file_name = self.file_path

        file_name = file_name.replace('.txt', '')


        with open(f'{file_name}_out.txt', 'w') as file:
            file.write(self.config_text_to_save)
        
    

def main():
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())



if __name__ == "__main__":
    main()