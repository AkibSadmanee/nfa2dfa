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
    Enter 'none' if there is no transition from a state, we will denote that with a 'ϕ'
    Enter 'done' for finishing taking input for a particular state and alphabet 
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