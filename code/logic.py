# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 18:34:02 2024

@author: Davide
"""

import random

    
    
def initialize_truth_dict(P, Q):
    '''Initializes a truth dictionary with basic truth values for P, Q, and their negations.'''
    return {
        'P': P,
        '(NOT P)': not P,
        'Q': Q,
        '(NOT Q)': not Q
    }

def create_text(first_state, second_state, connective):
    '''Generates a string representation of a statement involving two states and a connective.'''
    
    if connective == 'THEN':
        return '(IF ' + first_state + ' ' + connective + ' ' + second_state + ')'
    return '(' + first_state + ' ' + connective + ' ' + second_state + ')'
    


def find_truth(first_truth_state, second_truth_state, connective):
    ''''Evaluates the truth value of a statement based on the truth values of two states and the specified connective.'''
    
    if connective == 'AND':
        return first_truth_state and second_truth_state
    elif connective == 'OR':
        return first_truth_state or second_truth_state
    elif connective == 'THEN':
        return not first_truth_state or second_truth_state
    elif connective == 'EQUIVALENT':
        return first_truth_state == second_truth_state
    else:
        raise ValueError(f"Unsupported connective: {connective}")
    


def create_statements_2(truth_dict,connectives):
    '''Generates a statement using two random states from "truth_dict" and a random connective from "connectives",
    and returns the statement (with P and Q), its truth value, and a textual representation of the truth calculation.'''
    
    first_state, second_state = random.choices(list(truth_dict), k=2)
    connective = random.choice(connectives)
    statement = create_text(first_state, second_state, connective)
    first_truth_state = truth_dict[first_state]
    second_truth_state = truth_dict[second_state]
    truth = find_truth(first_truth_state, second_truth_state, connective)
    text = create_text(str(first_truth_state), str(second_truth_state), connective)
    return statement, truth, text

def attach_statements(first_statement, second_statement, connectives, first_truth_statement, second_truth_statement, text1, text2):
    '''Combines two statements with a connective, and returns the new statement, its truth value, 
    and a step-by-step solution for evaluating the truth value.'''

    connective = random.choice(connectives)
    statement = create_text(first_statement, second_statement, connective)
    truth = find_truth(first_truth_statement, second_truth_statement, connective)
    if len(text1) < len(text2):
        text1 += [text1[-1]] * (len(text2) - len(text1))
    elif len(text2) < len(text1):
        text2 += [text2[-1]] * (len(text1) - len(text2))
    combined_text = [create_text(text1[i], text2[i], connective) for i in range(len(text1))]
    combined_text.append(str(truth))
    return statement, truth, combined_text

def create_final_statement(length,truth_dict,connectives):
    '''Recursively generates a statement with a specified length "l" by combining smaller statements,
    and returns the final statement, its truth value, and a list of steps for calculating the truth.'''
    
    if length==1:
        state = random.choice(list(truth_dict))
        return state, truth_dict[state], [str(truth_dict[state])]*2
    elif length==2:
        statement, truth, text = create_statements_2(truth_dict,connectives)
        return statement, truth, [text, str(truth)]
    elif length>2:
        mid = length // 2
        statement_left, truth_left, steps_left = create_final_statement(mid + length%2, truth_dict, connectives)
        statement_right, truth_right, steps_right = create_final_statement(mid,truth_dict,connectives)
        return attach_statements(statement_left, statement_right, connectives,\
                                 truth_left, truth_right, steps_left, steps_right)
    else:
        raise ValueError(f"Unsupported lenght value: {length}")



def create_data(connectives, Q, P, length):
    '''Generates a complex logical statement of specified length and evaluates it.
    Returns the statement, a request prompt, answer explanation, and the truth value.'''
    truth_dict = initialize_truth_dict(P, Q)
    final_statement, truth, steps = create_final_statement(length, truth_dict, connectives)
    
    # Building the answer explanation in steps
    answer = (
        f"Let's evaluate the given statement with the provided truth values for P and Q:\n"
        f"P is {truth_dict['P']}\nQ is {truth_dict['Q']}\nNow substitute these values into the statement:\n"
        f"{final_statement}\nSubstitute truth values:\n{steps.pop(0)}"\
        f"\nStarting from the innermost parenthesis, we solve the statement:\n{steps.pop(0)}"
        )
        
    for step in steps:
        answer += f"\nProceeding:\n{step}"
    
    # Create a prompt for evaluation
    request = f"Evaluate the following statement knowing that P is {truth_dict['P']} and Q is {truth_dict['Q']}:\n{final_statement}"
    
    return final_statement, request, answer, truth




connectives = ['AND', 'OR', 'EQUIVALENT', 'THEN']
len_data=10
statement_list, answer_list, request_list, truth_list = [], [], [], []


while len(request_list)<len_data:
    P = random.choice([True, False])
    Q = random.choice([True, False])
    statement, request, answer, truth = create_data(connectives, Q, P, 8)
    if request not in request_list:
        statement_list.append(statement)
        request_list.append(request)
        answer_list.append(answer)
        truth_list.append(truth)
#print(statement, request, answer, truth)

