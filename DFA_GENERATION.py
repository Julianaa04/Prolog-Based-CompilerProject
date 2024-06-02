from graphviz import Digraph

def generate_dfa_graph(dfa, filename):
    dot = Digraph()
    dot.attr('node', shape='circle')
    dot.graph_attr['rankdir'] = 'LR'

    # Add nodes
    for state in dfa['states']:
        if state in dfa['final_states']:
            dot.node(state, shape='doublecircle')  # Mark final states differently
        else:
            dot.node(state)

    # Add edges
    for state, transitions in dfa['transitions'].items():
        for symbol, next_state in transitions.items():
            if state == dfa['initial_state']:
                dot.edge(state, next_state, label=symbol, arrowhead='normal')
            else:
                dot.edge(state, next_state, label=symbol)
    # Render the Digraph
    dot.render(filename, format='png')

# Define DFAs
#dfa_Number ->integer & real
dfa_Number = {
    'states': {'start','q0', 'q1', 'q2', 'q3', 'Dead', 'q4'},
    'input_symbols': {'[0-9]', '+', '-', '.'},
    'transitions': {
        'start':{' ':'q0'},
        'q0': {'[0-9]': 'q1', '+': 'q4', '-': 'q4','.': 'Dead'},
        'q1': {'[0-9]': 'q1', '.': 'q2', '+': 'Dead', '-': 'Dead'},
        'q2': {'[0-9]': 'q3', '+': 'Dead', '-': 'Dead', '.': 'Dead'},
        'q3': {'[0-9]': 'q1','+': 'Dead', '-': 'Dead', '.': 'Dead'},
        'q4': {'[0-9]': 'q1', '+': 'Dead', '-': 'Dead', '.': 'Dead'},
        'Dead': {'[0-9]': 'Dead', '+': 'Dead', '-': 'Dead', '.': 'Dead'},
    },
    'initial_state': 'q0',
    'final_states': {'q1', 'q3'},
}
dfa_Relational_Operators = {
    'states': {'start','q0', 'q1', 'q2', 'q3','q4','q5','q6','Dead'},
    'input_symbols': {'<', '>', '=',"other"},
    'transitions': {
        'start':{' ':'q0'},
        'q0': {'<': 'q1', '=': 'q4', '>': 'q5'},
        'q1': {'=': 'q2', '>': 'q3', '<': 'Dead'},
        'q2': {'<': 'Dead', '>': 'Dead', '=': 'Dead'},
        'q3': {'<': 'Dead', '>': 'Dead', '=': 'Dead'},
        'q4': {'<': 'Dead', '>': 'Dead', '=': 'Dead'},
        'q5': {'<': 'Dead', '>': 'Dead', '=': 'q6'},
        'q6': {'<': 'Dead', '>': 'Dead', '=': 'Dead'},
        'Dead': {'<': 'Dead','>': 'Dead','=': 'Dead'},
},
    'initial_state': 'q0',
    'final_states': {'q1', 'q2', 'q3','q4','q5','q6'},
}
dfa_Arthematic_Operators = {
    'states': {'start','q0', 'q1', 'Dead'},
    'input_symbols': {'+', '-', '*','/'},
    'transitions': {
        'start':{' ':'q0'},
        'q0': {'+': 'q1', '-': 'q1','*':'q1','/':'q1'},
        'q1': {'+': 'Dead', '-': 'Dead', '*': 'Dead','/':'Dead'},
        'Dead':{'+': 'Dead', '-': 'Dead', '*': 'Dead','/':'Dead'},
},
    'initial_state': 'q0',
    'final_states': {'q1'},
}
#aoc here stands for any other character
dfaComment={
    'states':{'start','q0','q1','q3','q4','q5','dead'},
    'input_symbols':{'aoc','/','*','%'},
    'transitions':{
        'start':{' ':'q0'},
        'q0': {'aoc': 'dead', '%': 'q1', '*': 'dead','/' : 'q2'},
        'q1': {'aoc': 'q1', '%': 'q1', '*': 'q1','/' : 'q1'},
        'q2': {'aoc': 'dead', '%': 'dead', '*': 'q3','/' : 'dead'},
        'q3': {'aoc': 'q3', '%': 'q3', '*': 'q4','/' : 'q3'},
        'q4': {'aoc': 'q3', '%': 'q3', '*': 'q4','/' : 'q5'},
        'q5': {'aoc': 'dead', '%': 'dead', '*': 'dead','/':'dead'},
        'dead': {'aoc': 'dead', '%': 'dead', '*': 'dead','/':'dead'},
    },
    'initial_state': 'q0',
    'final_states': {'q1','q5'},
}

dfa_Predicates={
    'states': {'start','q0', 'q1', 'q2', 'q3','q4','q5','q6','q7','q8','q9','q10','Dead'},
    'input_symbols': {'A-Z','a-z','P','r','e','d','i','c','a','t','e','s'},
    'transitions': {
        'start':{' ':'q0'},
        'q0': {'P': 'q1', '[^P]': 'Dead'},
        'q1': {'r': 'q2', '[^r]': 'Dead'},
        'q2': {'e': 'q3', '[^e]': 'Dead'},
        'q3': {'d': 'q4', '[^d]': 'Dead'},
        'q4': {'i': 'q5', '[^i]': 'Dead'},
        'q5': {'c': 'q6', '[^c]': 'Dead'},
        'q6': {'a': 'q7', '[^a]': 'Dead'},
        'q7': {'t': 'q8', '[^t]': 'Dead'},
        'q8': {'e': 'q9', '[^e]': 'Dead'},
        'q9': {'s': 'q10', '[^s]': 'Dead'},
        'q10': {'[a-zA-Z0-9+\\-*/<=>]': 'Dead'},
        'Dead': {'[a-zA-Z0-9+\\-*/<=>]': 'Dead'},
    },
    'initial_state': 'q0',
    'final_states': {'q10'},
}
dfa_goal={
    'states': {'start','q0', 'q1', 'q2', 'q3','q4', 'Dead'},
    'input_symbols': {'+', '-', '*','/','A-Z','a-z'},
    'transitions': {
        'start':{' ':'q0'},
        'q0': {'g': 'q1', '[^g]': 'Dead'},
        'q1': {'o': 'q2', '[^o]': 'Dead'},
        'q2': {'a': 'q3', '[^a]': 'Dead'},
        'q3': {'l': 'q4', '[^l]': 'Dead'},
        'Dead': {'[a-zA-Z0-9+\\-*/<=>]': 'Dead'},
    },
    'initial_state': 'q0',
    'final_states': {'q4'},
}
dfa_clauses={
    'states': {'start','q0', 'q1', 'q2', 'q3','q4','q5','q6','q7', 'Dead'},
    'input_symbols': {'A-Z','a-z','c','l','a','u','s','e'},
    'transitions': {
        'start':{' ':'q0'},
        'q0': {'c': 'q1', '[^c]': 'Dead'},
        'q1': {'l': 'q2', '[^l]': 'Dead'},
        'q2': {'a': 'q3', '[^a]': 'Dead'},
        'q3': {'u': 'q4', '[^u]': 'Dead'},
        'q4': {'s': 'q5', '[^s]': 'Dead'},
        'q5': {'e': 'q6', '[^e]': 'Dead'},
        'q6': {'s': 'q7', '[^s]': 'Dead'},
        'q7': {'[a-zA-Z0-9+\\-*/<=>]': 'Dead'},
        'Dead': {'[a-zA-Z0-9+\\-*/<=>]': 'Dead'},
    },
    'initial_state': 'q0',
    'final_states': {'q7'},
}
dfa_SpecialChar={
'states': {'start','q0', 'q1', 'q2','dead'},
    'input_symbols': {'.' ':' ';' ',' '(' ')' '-' '[ / < > = +  * A-Z a-z 0-9]'},
    'transitions': {
        'start':{' ':'q0'},
        'q0':{'.':'q1', ':':'q2', ';':'q1', ',':'q1', '(':'q1', ')':'q1','-':'dead', '[ / < > = +  * A-Z a-z 0-9]':'dead'},
        'q1':{'.':'dead', ':':'dead', ';':'dead', ',':'dead', '(':'dead', ')':'dead','-':'dead', '[ / < > = +  * A-Z a-z 0-9]':'dead'},
        'q2':{'.':'dead', ':':'dead', ';':'dead', ',':'dead', '(':'dead', ')':'dead','-':'q2', '[ / < > = + * A-Z a-z 0-9]':'dead'},
        'dead':{'.':'dead', ':':'dead', ';':'dead', ',':'dead', '(':'dead', ')':'dead','-':'dead', '[ / < > = +  * A-Z a-z 0-9]':'dead'},

},
'initial_state': 'q0',
   'final_states': {'q1','q2'},

}
dfa_Char={
    'states':{'start','q0','q1','q2', 'dead'},
    'input_symbols':{'\'','[A-Z a-z 0-9 . ,  ; : _ % ( ) < > = :- \" \\ / + - * ]','[A-Z 0-9 . , ; : _ % ( ) < > = :- \" \\ / + - *   ]'},
    'transitions':{
        'start':{' ':'q0'},
        'q0':{'\'':'q1','^[A-Z a-z 0-9 . ,  ; : _ % ( ) < > = :- \" \\ / + - *   ]':'dead'},
        'q1':{'\'':'q2','[A-Z a-z 0-9 . , ; : _ % ( ) < > = :- \" \\ / + - *   ]':'q2'},
        'q2':{'\'':'q1','[A-Z a-z 0-9 . ,  ; : _ % ( ) < > = :- \" \\ / + - *   ]':'dead'},
        'dead':{'\'':'dead','[A-Z a-z 0-9 . ,  ; : _ % ( ) < > = :- \" \\ / + - *   ]':'dead'},

    },
'initial_state': 'q0',
   'final_states': {'q2'},

}
dfa_String={
    'states': {'start','q0', 'q1', 'q2', 'q3', 'dead'},
    'input_symbols': {'\"', '[A-Z a-z 0-9 . ,  ; : _ % ( ) < > = :- \' \\ / + - * ]'},
    'transitions': {
        'start':{' ':'q0'},
        'q0': {'\"': 'q1', '^[A-Z a-z 0-9 . ,  ; : _ % ( ) < > = :- \' \\ / + - *   ]': 'dead'},
        'q1': {'\"': 'q3', '[A-Z 0-9 . , ; : _ % ( ) < > = :- \' \\ / + - *   ]': 'q2'},
        'q2': {'\"': 'q3', '[A-Z a-z 0-9 . ,  ; : _ % ( ) < > = :- \' \\ / + - *   ]': 'q2'} ,
        'q3': {'\"': 'q3', '[A-Z a-z 0-9 . ,  ; : _ % ( ) < > = :- \' \\ / + - *   ]': 'q2'},
        'dead': {'\"': 'dead', '[A-Z a-z 0-9 . ,  ; : _ % ( ) < > = :- \' \\ / + - *   ]': 'dead'},

    },
    'initial_state': 'q0',
    'final_states': {'q3'},
}

dfa_INT={
   'states':{'start','q0','q1','q2','dead'},
    'input_symbols': {'+','-','0-9'},
    'transitions':{
        'start':{' ':'q0'},
        'q0':{'+':'q1','-':'q1','0-9':'q2'},
        'q1':{'+':'dead','-':'dead','0-9':'q2'},
        'q2':{'+':'dead','-':'dead','0-9':'q2'},
        'dead':{'+':'dead','-':'dead','0-9':'dead'},
    },
    'initial_state': 'q0',
    'final_states': {'q2'},
}
dfa_Predicate_NAME={
    'states':{'start','q0','q1','q2','dead'},
    'input_symbols':{'a-z','A-Z','0-9','_','" "','-'},
    'transitions':{
        'start':{' ':'q0'},
        'q0':{'a-z':'q1','A-Z':'dead','0-9':'dead','_':'dead','" "':'dead','-':'dead'},
        'q1':{'a-z':'q2','A-Z':'q2','0-9':'q2','_':'q2','" "':'dead','-':'dead'},
        'q2':{'a-z':'q2','A-Z':'q2','0-9':'q2','_':'q2','" "':'dead','-':'dead'},
        'dead':{'a-z':'dead','A-Z':'dead','0-9':'dead','_':'dead','" "':'dead','-':'dead'},
    },
   'initial_state': 'q0',
   'final_states': {'q1','q2'},

}
dfaIdentifierVariable={
    'states': {'start','q0', 'q1', 'q2', 'dead'},
    'input_symbols': {'A-Z', 'a-z','0-9','_','[. : ; , ( ) - \' \ < > = +  *]'},
    'transitions': {
        'start':{' ':'q0'},
        'q0': {'A-Z': 'q2','a-z': 'dead','0-9':'dead','_': 'q1','[. : ; , ( ) - \' \ < > = +  *]':'dead'},
        'q1':{'A-Z': 'q2','a-z': 'q2','0-9':'q2','_': 'q2','[. : ; , ( ) - \' \ < > = +  *]':'dead'},
        'q2': {'A-Z': 'q2','a-z': 'q2','0-9':'q2','_': 'q2','[. : ; , ( ) - \' \ < > = +  *]':'dead'},
        'dead': {'A-Z': 'dead', 'a-z': 'dead', '0-9': 'dead', '_': 'dead','[. : ; , ( ) - \' \ < > = +  *]':'dead'},
    },
    'initial_state': 'q0',
    'final_states': {'q2', 'q3'},
}
dfaSpecialVariable={

    'states': {'start','q0','q1','dead'},
    'input_symbols':{'_'},
    'transitions':{
        'start':{' ':'q0'},
        'q0':{'_':'q1', 'other':'dead'},
        'q1':{'_':'dead', 'other':'dead'},
        'dead':{'_':'dead', 'other':'dead'},
    },
    'initial_state': 'q0',
    'final_states': {'q1'},
}
dfareal={
    'states':{'start','q0','q1','q2','q3','dead'},
    'input_symbols': {'+','-','0-9','.'},
    'transitions':{
        'start':{' ':'q0'},
        'q0':{'+':'q1','-':'q1','0-9':'q2','.':'dead'},
        'q1':{'+':'dead','-':'dead','0-9':'q2','.':'dead'},
        'q2':{'+':'dead','-':'dead','0-9':'q2','.':'q3'},
        'q3':{'+':'dead','-':'dead','0-9':'q3','.':'dead'},
        'dead':{'+':'dead','-':'dead','0-9':'dead','.':'dead'},
    },
    'initial_state': 'q0',
    'final_states': {'q2','q3'},

}
dfas = [dfa_Number,dfa_Relational_Operators,dfa_Arthematic_Operators,dfaComment,dfa_Predicates,dfa_goal,dfa_clauses,dfa_Char,dfa_SpecialChar,dfa_String,dfareal,dfa_INT,dfa_Predicate_NAME,dfaSpecialVariable,dfaIdentifierVariable]
for index, dfa in enumerate(dfas):
 filename = f'dfa_graph_{index}'
 generate_dfa_graph(dfa, filename)

