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

        self.tape = ['#' for x in range(int((32-len(initial_word))/2))]
        self.tape_index = len(self.tape)
        self.tape.extend(self.initial_word)
        for smth in range(len(self.tape), 32):
            self.tape.append('#')
        
        self.actual_state = self.initial_state

        self.paused = False

    def check_and_extend_tape(self, state):
        print(f'index: {self.tape_index}    dlugosc: {len(self.tape)}')
        if self.tape_index == 0 and state == 'L':
            for x in range(16):
                self.tape.insert(0,'#')
            self.tape_index+=16
        if self.tape_index == len(self.tape)-1 and state == 'P':
            for x in range(16):
                self.tape.append('#')

    def update_state(self):
        realtion_accomplished = False
        for relation in self.relations:
            if relation[0] == self.actual_state and relation[1] == self.tape[self.tape_index]:
                print(relation)
                self.actual_state = relation[2]
                self.tape[self.tape_index] = relation[3]
                self.check_and_extend_tape(relation[4])
                if relation[4] == 'L':
                    self.tape_index-=1
                else:
                    self.tape_index+=1
                realtion_accomplished =True
                break
        if realtion_accomplished == False:
            sys.exit()

    def print_tape(self):
        terminal_width = shutil.get_terminal_size().columns
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
        print(output)

    def run(self):
    
        while self.actual_state not in self.final_state:


            if not self.paused:
                self.print_tape()
                print()
                self.update_state()
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
                self.print_tape()
                print()
                self.update_state()
                time.sleep(0.2)  
            elif keyboard.is_pressed('escape'):
                sys.exit()
