from itertools import chain, combinations

def take_alphabet():
    """
    Takes input of alphabet(s) of a language and returns a list of alphabets
    """
    alphabets = set()       #Empty container for Symbols (Data-structure: DISJOINT-SET)
    key = ""
    alphabets.add('ε')
    counter = 1
    
    print("ENTER ALPHABET")
    print("""     Enter 'done' to finish input.""")
    
    while(key != "done"):
        temp = input("Enter Symbol " + str(counter)+": ")
        key = temp.lower()
        if(key != "done"):      #if user enters anything except 'done' -> add to set
            alphabets.add(key)
    alphabets = list(alphabets)     #Convert the set into list for indexed access
    return alphabets

def take_nfa_final_states(statenum):
    """
    Takes input of final states
    Takes in Number of states as parameter and Returns a List of final states
    """
    final_states = set()        #Empty Set to contain final states (Data-structure: DISJOINT-SET)
    counter = 1                 #Final state counter
    key = ""
    print("ENTER FINAL STATES")
    print("""     Enter 'done' to finish input.""")
    while(key != "done"):       #keep taking input until user enters "done"
        temp = input("Enter Final state " + str(counter)+": ")
        key = temp.lower()
        
        if key == "done":
            if len(final_states) == 0:  #if user enters no final state
                print("\nPlease Enter at least 1 final state.")
                key=""
            else:
                final_states = list(final_states)   #Convert the set into list for indexed access
                return final_states
        elif not(key.isdigit()):    #If the entered final state is not a digit
            print("Invalid input")
        else:       #If the inpput is a number
            if int(key) > statenum:     #Check if the final state number exceeds the number of states
                print("Invalid input")  #if final satte number exceeds the number of states give warning
            else:                       #If all is well. add it to the set    
                final_states.add(int(key))
                counter+=1

def create_nfa_transition_table(statenum, alphabets):
    """
    Creates the NFA transition table with user input.
    takes in 2 parameters: number of states, list of alphabets 
    returns the populated 2D list which is the transition table of the NFA
    
    e.g.:
          a       b        ε
    q1   0,1      ϕ        ϕ
    q2    ϕ      2,0       ϕ
    q3    2       ϕ        1
    """
    
    #instructions
    print("\nGETTING TRANSITION TABLE READY")
    print(
    """
    Enter 'none' if there is no transition from a state, we will denote that wih a 'ϕ'
    Enter 'done' for finishing taking input for a perticular state and alphabet 
    """)

    #empty 2D list for NFA
    nfa = [[[] for x in range(len(alphabets))] for y in range(statenum)]
   
   #Populate
    for i in range(statenum):
        for j in range(len(alphabets)):
            while(True):
                temp = input("From state q" + str(i+1) + " Getting \'" + str(alphabets[j]) + "\' Go to state: ")
                if temp.lower() == "done":
                    
                    if(len(nfa[i][j]) == 0):    #If there is no transition, add "ϕ" to nfa[i][j]
                        nfa[i][j].append("ϕ")
                        break
                    else:
                        break   #if user enters "done" after adding some transitions, simply abbort            
                
                elif temp.lower() == "none":
                    if(len(nfa[i][j]) == 0):
                        nfa[i][j].append("ϕ")   #If there is no transition, add "ϕ" to nfa[i][j]
                        break
                    else:
                        break       #if user enters "none" after adding some transitions, simply abbort 
                else:
                    if temp.isnumeric() == True and int(temp) <= statenum and int(temp) > 0 and temp not in nfa[i][j]:
                        #THREE conditions are placed.
                        #1. Input is a number
                        #2. Input is valid(Does not exceed number of sates and greater than 0)
                        #3. Same transition rule hasn't been already given
                        #If all of them hold, add the transition rule
                        nfa[i][j].append(int(temp))
                    elif not(temp.isnumeric()):     #CHECK1->FALSE: Input is not a number
                        print("Not a valid state number. Add Numbers Starting from 1 & Dont exceed the number of states.")
                    elif temp in nfa[i][j]:         #CHECK3->FALSE: Input already exists
                        print("State number already exists.")
                    else:           ##CHECK2->FALSE: Input exceeds number of states or is less than 0
                        print("Invalid state number.")
                    nfa[i][j] = list(set(nfa[i][j]))
            
    return nfa
    
def powerset(iterable):
    """
    chain.from_iterable(['ABC', 'DEF']) --> A B C D E F
    combinations('ABCD', 1) --> A B C D
    combinations('ABCD', 2) --> AB AC AD BC BD CD
    combinations('ABCD', 3) --> ABC ABD ACD BCD 
    here r goes from 0 to number of states and returns a tuple with the combination
    of all the elements of the given list
    """
    
    return chain.from_iterable(combinations(iterable, r) for r in range(len(iterable)+1))

def make_dfa_states(statenum):
    """
    Creates and returns a list of all the DFA states
    which is the powerset of the NFA states
    """
    temp_list = range(1,statenum+1)
    #powerset returns a tuple, convert it to list for indexed access
    dfa_states = [list(result) for result in powerset(temp_list)]
    return dfa_states

def find_dfa_start_state(nfa_start_state, nfa, alphabets):
    """
    Takes in 2 parameters: NFA start state ,the nfa(2d list)
                           and the list of alphabets 
    returns a list of the DFA start state(s)
    """

    dfa_start_state = [nfa_start_state]
    
    #alphabets.index('ε') = the index in alphabets where 'ε' resides
    #as our sate numbers stasrt from 1 but the list starts from 0, 
    #to access the nfa row-index, we need nfa_start_state-1
    
    #temp will contain the lambda transition of the start state of the nfa
    temp = nfa[nfa_start_state-1][alphabets.index('ε')]
    try:
        temp.remove('ϕ')  # removing 'ϕ' if there is no lambda transition
    except ValueError:
        pass
    
    dfa_start_state = dfa_start_state + temp
    #look for farther lambda transitions
    #if from 1 there is lambda transition to 2, 2 is added to temp
    #now below we will check if there is more lambda transition from 2
    #if from 2 there is lambda transition to 4, add 4 to temp and traverse 
    #if from 4 there is lambda transition to 6, add 6 to temp and traverse
    #continue until temp is empty
    for i in range(len(temp)-1):
        X = nfa[int(temp[i])][alphabets.index('ε')]
        dfa_start_state = dfa_start_state + X
        temp = temp + X
        temp = list(set(temp))  #get rid of redundency which may cause cycling
    
    dfa_start_state = set(dfa_start_state)    
    return list(dfa_start_state)
    
def create_dfa_transition_table(dfa_states, alphabets, nfa, statenum):
    """
    DFA transition tables doesn't entertain lambda transition 
    its number of states is (2^number of states of NFA)
    
    This function accepts 4 parameters:
    dfa_states: as list, alphabets as list, nfa as 2D list, statenum as integer
    
    and returns a 2D list that contains the dfa transition rules
    """
    #alphabets2 = alphabets doesnt make a copy of the list, instead makes a new reference
    #so to make a copy, we need to copy the list element by element
    alphabets2 = alphabets[:]
    eps_ind = alphabets.index('ε')

    try:
        alphabets2.remove('ε')  #DFA doesn't have lambda transitions
    except ValueError:
        pass
    
    #empty 2D list for DFA --> 2^statenum number of rows and (alphabets-1) number of collumns
    dfa = [[[] for x in range(len(alphabets2))] for y in range(len(dfa_states))]
    
    #1st loop till number of states which is the size of nfa[0]
    for i in range(statenum):
        #2nd loop till size of alphabet2 which doesnt have epsilon
        for j in range(len(alphabets2)):
            
            #an empty list to hold the epsilon transitions for each symbol
            #e-closure
            eps_list = []
            
            nfa_col = alphabets.index(alphabets2[j])
            
            flag = True
            if 'ϕ' not in nfa[i][nfa_col]:
                dfa[i][j] = nfa[i][nfa_col][:]
                for m in nfa[i][nfa_col]:
                    if 'ϕ' not in nfa[m-1][eps_ind]:
                        dfa[i][j] = dfa[i][j] + nfa[m-1][eps_ind]
                dfa[i][j] = list(set(dfa[i][j]))
                flag = False
         
            #cheke if there in no lambda transition
            if 'ϕ' not in nfa[i][eps_ind][0]:
                eps_list = eps_list + nfa[i][eps_ind]
                flag = False
            
            #check if both of the above conditions are true
            if flag:
                dfa[i][j] = []
            
            for k in eps_list:
                eps_list = list(set(eps_list))
                if 'ϕ' not in nfa[k-1][nfa_col]:
                    dfa[i][j]= dfa[i][j] + (nfa[k-1][nfa_col])
                
                if 'ϕ' not in nfa[k-1][eps_ind][0]:
                    print(nfa[k-1][eps_ind])
                    eps_list = eps_list + nfa[i][eps_ind]
    for i in range(statenum):
        for j in range(len(alphabets2)):           
            try:
                dfa[i][j].remove('ϕ')
            except ValueError:
                pass
    
    #From which index in dfa_states 2 sized list starts
    #1 sized lists are covered in the 1st portion of the algorithm
    
    for k in dfa_states:
        if len(k) > 1:
            temp = dfa_states.index(k)
            break
    
    for i in range(temp, len(dfa_states)):
        for j in range(len(alphabets2)):
            temp_list = []
            for k in dfa_states[temp]:
                temp_list = temp_list +(dfa[k-1][j])
            temp_set = set()
            for k in temp_list:
                temp_set.add(k)
            dfa[temp][j] = list(temp_set)[:]
        temp = temp + 1
    
    return dfa

def find_dfa_final_states(dfa_states, nfa_final_states):
    final_states = []
    for i in nfa_final_states:
        for j in dfa_states:
            if i in j:
                final_states.append(j)
    return final_states
    

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
