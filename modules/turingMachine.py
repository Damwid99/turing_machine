import sys
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

    def check_and_extend_tape(self, state):
        if self.tape_index == 0 and state[4] == 'L':
            for x in range(16):
                self.tape.insert(0,'#')
            self.tape_index+=16
        if self.tape_index == len(self.tape) and state == 'P':
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
    
    def run(self):
        while self.actual_state not in self.final_state:
            print(self.tape)
            print("")
            self.update_state()

