from utils.utils import render_txt
from modules.turingMachine import TuringMachine


initial_word, states, final_states, initial_state, relations, tape_alphabet = render_txt('./in.txt')
machine = TuringMachine(relations=relations, initial_state=initial_state, final_state=final_states, states=states,
                        initial_word=initial_word)

print(tape_alphabet )


print("-----------------------------------")
# machine.run()    