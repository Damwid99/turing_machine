import sys
import keyboard
import time
import shutil
import os


class TuringMachine:
    def __init__(self, relations, initial_word, initial_state, final_state, states:list = []):
        self.relations = relations
        self.initial_state = initial_state
        self.initial_word = initial_word
        self.final_state = final_state
        self.states = states
        self.calculating_length = 0

        self.tape = ['#' for x in range(int((32-len(initial_word))/2))]
        self.tape_index = len(self.tape)
        self.tape.extend(self.initial_word)
        for smth in range(len(self.tape), 32):
            self.tape.append('#')
        
        self.actual_state = self.initial_state
        self.message = ''

        self.paused = False

    def check_and_extend_tape(self, state):
        if self.tape_index == 0 and state == 'L':
            for x in range(16):
                self.tape.insert(0,'#')
            self.tape_index+=16
            self.message = 'Tape is being extended'
        if self.tape_index == len(self.tape)-1 and state == 'P':
            for x in range(16):
                self.tape.append('#')
            self.message = 'Tape is being extended'
        
    def update_state(self):
        self.message = ''
        realtion_accomplished = False
        relation_done = None
        for relation in self.relations:
            if relation[0] == self.actual_state and relation[1] == self.tape[self.tape_index]:
                relation_done = relation
                self.actual_state = relation[2]
                self.tape[self.tape_index] = relation[3]
                self.check_and_extend_tape(relation[4])
                if relation[4] == 'L':
                    self.tape_index -= 1
                else:
                    self.tape_index += 1
                realtion_accomplished = True
                self.calculating_length += 1
                break
        if realtion_accomplished == False:
            # sys.exit()
            self.message = "No available states."
        if relation_done:
            return ' '.join(relation_done)
        else:
            return ""

    def print_tape(self, terminal_width = shutil.get_terminal_size().columns):
        # terminal_width = shutil.get_terminal_size().columns
        all_rows = int(len(self.tape)/terminal_width)+1


        output = ""
        for row in range(all_rows):
            row_output = "" 
            for printing_index in range(terminal_width * row, min(terminal_width * (row + 1), len(self.tape))):
                if self.tape_index in range(terminal_width * row, min(terminal_width * (row + 1), len(self.tape))):
                    if printing_index == self.tape_index:
                        row_output += 'v'
                    else:
                        row_output += ' '
            row_output += '\n'  
            for printing_index in range(terminal_width * row, min(terminal_width * (row + 1), len(self.tape))):
                row_output += self.tape[printing_index]
            output += row_output + '\n'  

        os.system('cls')
        return output

    def run(self):
    
        while self.actual_state not in self.final_state:
            if not self.paused:
                print(self.print_tape())
                print()
                print(self.update_state())
                time.sleep(0.1)

            if keyboard.is_pressed(' '):
                if self.paused:
                    self.paused = False
                    print("Resuming...")
                else:
                    self.paused = True
                    print("Paused. Press space to resume or right arrow to step forward.")
                while keyboard.is_pressed(' '):
                    time.sleep(0.1) 
            elif keyboard.is_pressed('right'):
                print("Stepping forward...")
                print(self.print_tape())
                print()
                print(self.update_state())
                time.sleep(0.2)  
            elif keyboard.is_pressed('escape'):
                sys.exit()
