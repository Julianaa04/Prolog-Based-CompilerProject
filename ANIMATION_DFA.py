from graphviz import Digraph
import time

def animate_dfa(dfa, string):
    dot = Digraph()
    dot.attr('node', shape='circle')
    dot.graph_attr['rankdir'] = 'LR'

    # Add nodes
    states = dfa['states']
    for state in states:
        dot.node(state)

    # Add edges
    transitions = dfa['transitions']
    for state, symbols in transitions.items():
        for symbol, next_state in symbols.items():
            dot.edge(state, next_state, label=symbol)

    # Render the initial state of the DFA
    initial_state = dfa['initial_state']
    dot.node('current', shape='doublecircle', color='green')
    dot.edge('current', initial_state)

    # Animate the DFA transitions for the given string
    current_state = initial_state
    dot.node(current_state, color='green')
    dot.render('dfa_animation', format='png')

    for char in string:
        time.sleep(1)  # Delay between transitions
        next_state = None
        for symbol, transition_state in transitions[current_state].items():
            if symbol == char or symbol == '0|1|2|3|4|5|6|7|8|9':
                next_state = transition_state
                break

        if next_state:
            dot.node(next_state, color='green')
            dot.node(current_state, color='black')
            dot.edge(current_state, next_state, label=char, color='green')
            current_state = next_state
        else:
            break

        dot.render('dfa_animation', format='png')

    dot.node(current_state, shape='doublecircle', color='red')
    dot.render('dfa_animation', format='png')

# Number= 0 or 1 or 2 or 3 or 4 or 5 or 6 or 7 or 8 or 9

dfa_Number= {
    'states': {'q0', 'q1', 'q2', 'q3','q4','dead',},
    'input_symbols': {'0','1','2','3','4','5','6','7','8','9', '+', '-', '.'},
    'transitions': {
        'q0': { '0': 'q2',
                '1': 'q2',
                '2': 'q2',
                '3': 'q2',
                '4': 'q2',
                '5': 'q2',
                '7': 'q2',
                '8': 'q2',
                '9': 'q2',
                '+': 'q1',
                '-': 'q1',
                '.': 'dead'},
        'q1': { '0': 'q2',
                '1': 'q2',
                '2': 'q2',
                '3': 'q2',
                '4': 'q2',
                '5': 'q2',
                '7': 'q2',
                '8': 'q2',
                '9': 'q2',
                '+': 'dead',
                '-': 'dead',
                '.': 'dead'},
        'q2': { '0': 'q2',
                '1': 'q2',
                '2': 'q2',
                '3': 'q2',
                '4': 'q2',
                '5': 'q2',
                '7': 'q2',
                '8': 'q2',
                '9': 'q2',
                '+': 'dead',
                '-': 'dead',
                '.': 'q3'},
        'q3': {'0': 'q4',
                '1': 'q4',
                '2': 'q4',
                '3': 'q4',
                '4': 'q4',
                '5': 'q4',
                '7': 'q4',
                '8': 'q4',
                '9': 'q4',
                '+': 'dead',
                '-': 'dead',
                '.': 'dead'},
        'q4': {'0': 'q4',
               '1': 'q4',
               '2': 'q4',
               '3': 'q4',
               '4': 'q4',
               '5': 'q4',
               '7': 'q4',
               '8': 'q4',
               '9': 'q4',
               '+': 'dead',
               '-': 'dead',
               '.': 'dead'},
        'dead': {'0': 'dead',
               '1': 'dead',
               '2': 'dead',
               '3': 'dead',
               '4': 'dead',
               '5': 'dead',
               '7': 'dead',
               '8': 'dead',
               '9': 'dead',
               '+': 'dead',
               '-': 'dead',
               '.': 'dead'},
    },
    'initial_state': 'q0',
    'final_states': {'q4','q2'},
}

string = '-9.990'
animate_dfa(dfa_Number, string)

dfa_Relational_Operators = {
    'states': {'q0', 'q1', 'q2', 'q3','q4','q6','Dead'},
    'input_symbols': {'<', '>', '='},
    'transitions': {
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
# string = '>='
# animate_dfa(dfa_Relational_Operators, string)

dfaSpecialVariable={

    'states': {'q0','q1','dead'},
    'input_symbols':{'_'},
    'transitions':{
        'q0':{'_':'q1', 'other':'dead'},
        'q1':{'_':'dead', 'other':'dead'},
        'dead':{'_':'dead', 'other':'dead'},
    },
    'initial_state': 'q0',
    'final_states': {'q1'},
}
# string = '_'
# animate_dfa(dfaSpecialVariable, string)

dfa_Arthematic_Operators ={
    'states': {'q0', 'q1', 'Dead'},
    'input_symbols': {'+', '-', '*','/'},
    'transitions': {
        'q0': {'+': 'q1', '-': 'q1','*':'q1','/':'q1'},
        'q1': {'+': 'Dead', '-': 'Dead', '*': 'Dead','/':'Dead'},
        'Dead':{'+': 'Dead', '-': 'Dead', '*': 'Dead','/':'Dead'},
},
    'initial_state': 'q0',
    'final_states': {'q1'},
}
# string = '+-'
# animate_dfa(dfa_Arthematic_Operators, string)
dfa_Predicates={
    'states': {'q0', 'q1', 'q2', 'q3','q4','q5','q6','q7','q8','q9','q10','Dead'},
    'input_symbols': {'A-Z','a-z','P','r','e','d','i','c','a','t','e','s'},
    'transitions': {
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
# string = 'Predicates'
# animate_dfa(dfa_Predicates, string)

dfa_goal={
    'states': {'q0', 'q1', 'q2', 'q3','q4', 'Dead'},
    'input_symbols': {'+', '-', '*','/','A-Z','a-z'},
    'transitions': {
        'q0': {'g': 'q1', '[^g]': 'Dead'},
        'q1': {'o': 'q2', '[^o]': 'Dead'},
        'q2': {'a': 'q3', '[^a]': 'Dead'},
        'q3': {'l': 'q4', '[^l]': 'Dead'},
        'Dead': {'[a-zA-Z0-9+\\-*/<=>]': 'Dead'},
    },
    'initial_state': 'q0',
    'final_states': {'q4'},
}
# string = 'goal'
# animate_dfa(dfa_goal, string)
dfa_clauses={
    'states': {'q0', 'q1', 'q2', 'q3','q4','q5','q6','q7', 'Dead'},
    'input_symbols': {'A-Z','a-z','c','l','a','u','s','e'},
    'transitions': {
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
# string = 'clauses'
# animate_dfa(dfa_clauses, string)

dfaPredicate={
    'states':{'q0','q1','q2','dead'},
    'input_symbols':{ 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9','_','" "','-'},
    'transitions':{
        'q0':{'a':'q1',
              'b':'q1',
              'c':'q1',
              'd':'q1',
              'e':'q1',
              'f':'q1',
              'g':'q1',
              'h':'q1',
              'i':'q1',
              'j':'q1',
              'k':'q1',
              'l':'q1',
              'm':'q1',
              'n':'q1',
              'o':'q1',
              'p':'q1',
              'q':'q1',
              'r':'q1',
              's':'q1',
              't':'q1',
              'u':'q1',
              'v':'q1',
              'w':'q1',
              'x':'q1',
              'y':'q1',
              'z':'q1',
              'A':'dead',
              'B':'dead',
              'C':'dead',
              'D':'dead',
              'E':'dead',
              'F':'dead',
              'G':'dead',
              'H':'dead',
              'I':'dead',
              'J':'dead',
              'K':'dead',
              'L':'dead',
              'M':'dead',
              'N':'dead',
              'O':'dead',
              'P':'dead',
              'Q':'dead',
              'R':'dead',
              'S':'dead',
              'T':'dead',
              'U':'dead',
              'V':'dead',
              'W':'dead',
              'X':'dead',
              'Y':'dead',
              'Z':'dead',
              '0': 'q2',
              '1': 'q2',
              '2': 'q2',
              '3': 'q2',
              '4': 'q2',
              '5': 'q2',
              '7': 'q2',
              '8': 'q2',
              '9': 'q2','_':'dead','" "':'dead','-':'dead'},
        'q1':{'a':'q2',
              'b':'q2',
              'c':'q2',
              'd':'q2',
              'e':'q2',
              'f':'q2',
              'g':'q2',
              'h':'q2',
              'i':'q2',
              'j':'q2',
              'k':'q2',
              'l':'q2',
              'm':'q2',
              'n':'q2',
              'o':'q2',
              'p':'q2',
              'q':'q2',
              'r':'q2',
              's':'q2',
              't':'q2',
              'u':'q2',
              'v':'q2',
              'w':'q2',
              'x':'q2',
              'y':'q2',
              'z':'q2',
              'A':'q2',
              'B':'q2',
              'C':'q2',
              'D':'q2',
              'E':'q2',
              'F':'q2',
              'G':'q2',
              'H':'q2',
              'I':'q2',
              'J':'q2',
              'K':'q2',
              'L':'q2',
              'M':'q2',
              'N':'q2',
              'O':'q2',
              'P':'q2',
              'Q':'q2',
              'R':'q2',
              'S':'q2',
              'T':'q2',
              'U':'q2',
              'V':'q2',
              'W':'q2',
              'X':'q2',
              'Y':'q2',
              'Z':'q2',
              '0': 'q2',
              '1': 'q2',
              '2': 'q2',
              '3': 'q2',
              '4': 'q2',
              '5': 'q2',
              '7': 'q2',
              '8': 'q2',
              '9': 'q2','_':'q2','" "':'dead','-':'dead'},
        'q2':{'a':'q2',
              'b':'q2',
              'c':'q2',
              'd':'q2',
              'e':'q2',
              'f':'q2',
              'g':'q2',
              'h':'q2',
              'i':'q2',
              'j':'q2',
              'k':'q2',
              'l':'q2',
              'm':'q2',
              'n':'q2',
              'o':'q2',
              'p':'q2',
              'q':'q2',
              'r':'q2',
              's':'q2',
              't':'q2',
              'u':'q2',
              'v':'q2',
              'w':'q2',
              'x':'q2',
              'y':'q2',
              'z':'q2',
              'A':'q2',
              'B':'q2',
              'C':'q2',
              'D':'q2',
              'E':'q2',
              'F':'q2',
              'G':'q2',
              'H':'q2',
              'I':'q2',
              'J':'q2',
              'K':'q2',
              'L':'q2',
              'M':'q2',
              'N':'q2',
              'O':'q2',
              'P':'q2',
              'Q':'q2',
              'R':'q2',
              'S':'q2',
              'T':'q2',
              'U':'q2',
              'V':'q2',
              'W':'q2',
              'X':'q2',
              'Y':'q2',
              'Z':'q2',
              '0': 'q2',
              '1': 'q2',
              '2': 'q2',
              '3': 'q2',
              '4': 'q2',
              '5': 'q2',
              '7': 'q2',
              '8': 'q2',
              '9': 'q2','_':'q2','" "':'dead','-':'dead'},
        'dead':{'a':'dead',
                'b':'dead',
                'c':'dead',
                'd':'dead',
                'e':'dead',
                'f':'dead',
                'g':'dead',
                'h':'dead',
                'i':'dead',
                'j':'dead',
                'k':'dead',
                'l':'dead',
                'm':'dead',
                'n':'dead',
                'o':'dead',
                'p':'dead',
                'q':'dead',
                'r':'dead',
                's':'dead',
                't':'dead',
                'u':'dead',
                'v':'dead',
                'w':'dead',
                'x':'dead',
                'y':'dead',
                'z':'dead',
                'A':'q2',
                'B':'q2',
                'C':'q2',
                'D':'q2',
                'E':'q2',
                'F':'q2',
                'G':'q2',
                'H':'q2',
                'I':'q2',
                'J':'q2',
                'K':'q2',
                'L':'q2',
                'M':'q2',
                'N':'q2',
                'O':'q2',
                'P':'q2',
                'Q':'q2',
                'R':'q2',
                'S':'q2',
                'T':'q2',
                'U':'q2',
                'V':'q2',
                'W':'q2',
                'X':'q2',
                'Y':'q2',
                'Z':'q2',
                '0': 'dead',
                '1': 'dead',
                '2': 'dead',
                '3': 'dead',
                '4': 'dead',
                '5': 'dead',
                '7': 'dead',
                '8': 'dead',
                '9': 'dead','_':'dead','" "':'dead','-':'dead'},
    },
   'initial_state': 'q0',
   'final_states': {'q1','q2'},
}

# string = 'predicate'
# animate_dfa(dfaPredicate, string)
