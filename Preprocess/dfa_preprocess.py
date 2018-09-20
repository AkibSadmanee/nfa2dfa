
def powerset(iterable):
    """
    chain.from_iterable(['ABC', 'DEF']) --> A B C D E F
    combinations('ABCD', 1) --> A B C D
    combinations('ABCD', 2) --> AB AC AD BC BD CD
    combinations('ABCD', 3) --> ABC ABD ACD BCD 
    here r goes from 0 to number of states and returns a tuple with the combination
    of all the elements of the given list
    """
    from itertools import chain, combinations
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
            if 'ϕ' not in nfa[i][eps_ind]:
                eps_list = eps_list + nfa[i][eps_ind]
                flag = False
            
            #check if both of the above conditions are true
            if flag:
                dfa[i][j] = []
            
            for k in eps_list:
                eps_list = list(set(eps_list))
                if 'ϕ' not in nfa[k-1][nfa_col]:
                    dfa[i][j]= dfa[i][j] + (nfa[k-1][nfa_col])
                
                if 'ϕ' not in nfa[k-1][eps_ind]:
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
    
