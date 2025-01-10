##__init__(self,alphabet,states,start,final,transitions):
import re
from functools import reduce


class Fsm:

  def __init__(self, alphabet, states, start, final, transitions):
    self.sigma = alphabet
    self.states = states
    self.start = start
    self.final = final
    self.transitions = transitions

  def __str__(self):
    sigma = "Alphabet: " + str(self.sigma) + "\n"
    states = "States: " + str(self.states) + "\n"
    start = "Start: " + str(self.start) + "\n"
    final = "Final: " + str(self.final) + "\n"
    trans_header = "Transitions: [\n"
    thlen = len(trans_header)
    translist = ""
    for t in self.transitions:
      translist += " " * thlen + str(t) + "\n"
    translist += " " * thlen + "]"
    transitions = trans_header + translist
    ret = sigma + states + start + final + transitions
    return ret


count = 0


def fresh():
  global count
  count += 1
  return count


def char(string):
  #raise Exception("Not Implemented")
  nfa = Fsm([], [0], 0, [], [])
  if string == "":
    nfa.final.append(1)
    nfa.transitions.append((0, 'epsilon', 1))
    nfa.states.append(1)

  else:
    x = 0
    for c in string:
      nfa.sigma.append(c)
      nfa.transitions.append((x, c, x + 1))
      x += 1
      nfa.states.append(x)
    nfa.final.append(x)
  return nfa


def concat(r1, r2):
  a = r1.sigma
  for b in r2.sigma:
    if b not in a:
      a.extend(b)
  s = r1.start
  nfa = Fsm(a, r1.states, r1.start, [],r1.transitions)

  x = r1.final[0]
  f = r2.final[0] + x
  nfa.final = [f]
  for t in r2.transitions:
    if t[0] + x not in nfa.states:
      nfa.states.append(t[0] + x)
    if t[2] + x not in nfa.states:
      nfa.states.append(t[2] + x)
    myT = [t[0] + x, t[1], t[2] + x]
    nfa.transitions.extend([tuple(myT)])

  return nfa


def union(r1, r2):
  myLen = len(r1.states) + len(r1.states)
  x = 0
  a = r1.sigma
  for b in r2.sigma:
    if b not in a:
      a.extend(b)
  f = list(i + 1 for i in r1.final)
  nfa = Fsm(a, [x], x, f, [])

  x = 1
  myT = [0, "epsilon", r1.start + x]
  nfa.transitions.extend([tuple(myT)])
  for t in r1.transitions:
    myLen -= 1
    if t[0] + x not in nfa.states:
      nfa.states.append(t[0] + x)
    if t[2] + x not in nfa.states:
      nfa.states.append(t[2] + x)
    myT = [t[0] + x, t[1], t[2] + x]
    nfa.transitions.extend([tuple(myT)])

  x = myLen
  myT = [0, "epsilon", r2.start + x]
  nfa.transitions.extend([tuple(myT)])
  l = list(i for i in r2.final)
  f.extend(i + x for i in l)
  for t in r2.transitions:
    if t[0] + x not in nfa.states:
      nfa.states.append(t[0] + x)
    if t[2] + x not in nfa.states:
      nfa.states.append(t[2] + x)
    myT = [t[0] + x, t[1], t[2] + x]
    nfa.transitions.extend([tuple(myT)])

  return nfa


def star(r1):
  raise Exception("Not Implemented")


def e_closure(s, nfa):
  #raise Exception("Not Implemented")
  ret = []
  if isinstance(s, int):
    ret = [s]
  else:
    ret.extend(s)
  ret.extend(move('epsilon', s, nfa))

  for x in range(1, len(ret)):
    s2 = ret[x]
    ret.extend(move('epsilon', s2, nfa))

  ret2 = []
  for sublist in ret:
    if sublist not in ret2:
      ret2.append(sublist)

  ret2.sort()
  return ret2


def move(c, s, nfa):
  #raise Exception("Not Implemented")
  ret = []
  if isinstance(s, int):
    s = [s]
  for transition in nfa.transitions:
    for i in s:
      if transition[0] == i and transition[1] == c:
        ret.append(transition[2])

  ret2 = []
  for sublist in ret:
    if sublist not in ret2:
      ret2.append(sublist)
  ret2.sort()
  return ret2


def nfa_to_dfa(nfa):
  #raise Exception("Not Implemented")
  # DFA = ( a , states , start, finals, transitions)
  dfa = Fsm(nfa.sigma, [], [], [], [])
  # visited = [ ]
  visited = []
  # let DFA.start = e−closure (start) , add to DFA . states
  dfa.start = [e_closure(nfa.start, nfa)]
  dfa.states.extend(dfa.start)
  # while visited! = DFA.states
  while visited != dfa.states:
    #for s in dfa.states:
    # add an unvisited state , s , to visited
    myState = [state for state in dfa.states if state not in visited][0]
    visited.append(myState)
    for s in myState:
      # for each char in a
      for c in dfa.sigma:
        # E = move(s)
        E = move(c, [s], nfa)
        # e = e−closure (E)
        if E != []:
          e = e_closure(E, nfa)
          # if e not in DFA.states
          if e not in dfa.states:
            # add e to DFA.states
            dfa.states.append(e)
          # add(s, char, e) to DFA.transitions
          t = tuple([myState, c, e])
          dfa.transitions.append(t)

    # DFA.final= { r|r\ in DFA . s tates
    #and \existss\ in r and s \ in NFA.final}
    #final
      for final_state in nfa.final:
        for t in dfa.transitions:
          if final_state in t[2] and t[2] not in dfa.final:
            dfa.final.append(t[2])
  return dfa


def accept(nfa, string):
  #raise Exception("Not Implemented")
  nfa = nfa_to_dfa(nfa)
  allCS = []
  currentS = nfa.start
  for i in string:
    allCS = move(i, currentS, nfa)
    currentS = allCS

  for s in currentS:
    if s in nfa.final:
      return True
  return currentS in nfa.final