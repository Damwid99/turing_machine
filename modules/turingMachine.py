
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

    def update_state(self):
        for state in self.states:
            if state[0] == self.actual_state and state[1] == self.tape[self.tape_index]:
                self.actual_state = state[2]
                self.tape[self.tape_index] = state[3]
                if state[4] == 'L':
                    self.tape_index-=1
                else:
                    self.tape_index+=1
    
    def run(self):
        while self.actual_state not in self.final_state:
            self.udpate_state