import sys
sys.path.append("./Preprocess/")
from nfa_preprocess import take_alphabet
from nfa_preprocess import take_nfa_final_states
from nfa_preprocess import create_nfa_transition_table

#Take input: NUMBER OF STATES 
print("""
                    \033[1m  Enter Information for NFA \033[0m
""")

while True:
    statenum = input("\nEnter number of states: ")
    if statenum.isdigit():
        statenum  = int(statenum)
        if statenum > 0:
            break
        else:
            print("Invalid input")
    else:
        print("NFA must have at least 1 state")
print("")

#Input NFA Start State
while(True):
    nfa_start_state = input("Enter Start State: ")
    if nfa_start_state.isdigit():
        if int(nfa_start_state) <= 0:
            print("Invalid State.")
        else:
            break
    else:
        print("Not a Number.")
print("")
nfa_final_states = take_nfa_final_states(statenum)
print("")

alphabets = take_alphabet()
print("")

nfa = create_nfa_transition_table(statenum, alphabets)
print("""
                    \033[1m  Nondeterministic Finite Automata \033[0m
                              5 Tuple System
    1.States  2.Alphabets  3.Start State  4.Final State  5.Transition Rules
""")
print("States: ", end=" ")
nfa_temp_states = []
for i in range(statenum):
    nfa_temp_states.append(i+1)
print(nfa_temp_states)
print("Alphabets: ", end=" ")
alphabets2 = alphabets[:]
try:
    alphabets2.remove('ε')
except ValueError:
    pass
print(alphabets2)

print("Start State: ", end=" ")
print(nfa_start_state)

print("Final States: ", end=" ")
print(nfa_final_states)

print("Transition Table: ", end=" ")
print(nfa)




#Convertion Begins
from dfa_preprocess import make_dfa_states
from dfa_preprocess import find_dfa_start_state
from dfa_preprocess import create_dfa_transition_table
from dfa_preprocess import find_dfa_final_states

dfa_states = make_dfa_states(statenum)
del dfa_states[0]
dfa_start_state = [int(nfa_start_state)]
#dfa_start_state = find_dfa_start_state(dfa_start_state, nfa, alphabets)
dfa_final_states = find_dfa_final_states(dfa_states, nfa_final_states)
dfa = create_dfa_transition_table(dfa_states, alphabets, nfa, statenum)


print("""
                    \033[1m  Deterministic Finite Automata \033[0m
                              5 Tuple System
    1.States  2.Alphabets  3.Start State  4.Final State  5.Transition Rules
""")
print("States: ", end=" ")
print(dfa_states)

print("Alphabets: ", end=" ")
print(alphabets2)

print("Start States: ", end=" ")
print(dfa_start_state)

print("Final States: ", end=" ")


print(dfa_final_states)

print("Transition Table: ", end=" ")
print(dfa)
