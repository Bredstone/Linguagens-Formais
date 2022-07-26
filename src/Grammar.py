import sys
from itertools import chain, groupby, product
from operator import itemgetter
from copy import deepcopy

class Grammar:
  """
  Uma classe usada para representar gramáticas

  Attributes
  ----------
  productions: dict
    dicionário com as produções geradas por cada não-terminal da gramática
  nterminals: list
    lista de itens não-terminais da gramática
  terminals: list
    lista de itens terminais da gramática
  firsts: dict
    dicionário com o conjunto 'First' de cada item não-terminal
  follows: dict
    dicionário com o conjunto 'Follow' de cada item não-terminal
  llTable: dict
    dicionário contendo a tabela de análise preditivo LL(1)
  lrSet: list
    conjunto de itens LR(0)
  slrTableAction: dict
    dicionário contendo a tabela de análise 'Action' SLR(1)
  slrTableGoTo: dict
    dicionário contendo a tabela de análise 'Go To' SLR(1)
  """

  def __init__(self, productions):
    """
    Parameters
    ----------
    productions: dict
      dicionário com as produções geradas por cada não-terminal da gramática
    """

    self.productions = productions
    self.nterminals = [y for x in productions.keys() for y in x if y[0].isupper()]
    self.terminals = [y for x in chain.from_iterable(productions.values()) for y in x if not y[0].isupper()]
    self.terminals = sorted(set(self.terminals))
    self.firsts = dict()
    self.follows = dict()
    self.llTable = dict()
    self.lrSet = []
    self.slrTableAction = dict()
    self.slrTableGoTo = dict()
    
    if len(list(productions.keys())[0]) != 1:
      raise Exception('Gramática inválida!')

  def isGLC(self):
    """Verifica se a gramática é livre de contexto"""

    return all([y[0].isupper() and len(x) == 1 for x in self.productions.keys() for y in x])

  def toStr(self):
    """Transforma a gramática em string, para impressão"""

    out = []
    for (nt, t) in self.productions.items():
      out += [f'{" ".join(nt)} -> {" | ".join(" ".join(x) for x in t)}']
    
    return '\n'.join(out)

  def printGrammar(self):
    """Imprime a gramática em formato padrão"""

    for (nt, t) in self.productions.items():
      print(f'{" ".join(nt)} -> {" | ".join(" ".join(x) for x in t)}')

  def generateFirstSet(self):
    """Gera o conjunto de 'First' para cada não-terminal da gramática"""

    def generateFirst(value):
      """
      Gera o conjunto de 'First' para um não-terminal específico da gramática
      
      Parameters
      ----------
      value: str
        não-terminal
      """
      if value in self.terminals:
        return [value]

      first = []
      for prod in self.productions[(value, )]:
        if all('&' in generateFirst(p) for p in prod if p != value) or prod == ['&']:
          first += ['&']

        for p in prod:
          if p == value: break
          first += [x for x in generateFirst(p) if x != '&']
          if '&' not in generateFirst(p): break

      return sorted(set(first))

    if Grammar.eliminateLeftRecursion(self).productions.keys() != self.productions.keys():
      raise Exception('A gramática não pode ser recursiva à esquerda!')

    self.firsts = dict()
    for nterminal in self.nterminals:
      self.firsts[nterminal] = generateFirst(nterminal)

  def generateFollowSet(self):
    """Gera o conjunto de 'Follow' para cada não-terminal da gramática"""

    def insert(nterminal, index):
      """
      Faz a análise de determinada produção e atualiza o conjunto 'Follows' com o resultado
      
      Parameters
      ----------
      nterminal: str
        não-terminal
      index: int
        índice do não terminal na produção
      """

      if index == len(production) - 1:
        follow[nterminal] = follow.get(nterminal, []) + follow[nt]
      elif production[index + 1] in self.terminals:
        follow[nterminal] = follow.get(nterminal, []) + [production[index + 1]]
      else:
        follow[nterminal] = follow.get(nterminal, []) + [x for x in self.firsts[production[index + 1]] if x != '&']

        if '&' in self.firsts[production[index + 1]]:
          insert(nterminal, index + 1)

    self.generateFirstSet()

    follow = dict.fromkeys(self.nterminals, [])
    follow[self.nterminals[0]] = ['$']
    while True:
      size = len([y for x in follow.values() for y in x])

      for ((nt,), productions) in self.productions.items():
        for production in productions:
          for index in range(len(production)):
            if production[index] in self.nterminals:
              insert(production[index], index)

      for key in follow.keys():
        follow[key] = sorted(set(follow[key]))

      if len([y for x in follow.values() for y in x]) == size:
        break

    self.follows = follow

  def buildLLTable(self):
    """Gera a tabela de análise preditivo LL(1)"""

    grammar = Grammar.eliminateLeftRecursion(Grammar.factorate(self))
    grammar.generateFollowSet()

    for nterminal in grammar.nterminals:
      if any(production == ['&'] for production in grammar.productions[(nterminal, )]):
        if set(grammar.firsts[nterminal]) & set(grammar.follows[nterminal]):
          raise Exception('Interseção entre First e Follow não é vazia!')

    table = dict.fromkeys(product(grammar.nterminals, [x for x in grammar.terminals if x != '&'] + ['$']), '')
    for ((nt,), productions) in grammar.productions.items():
      for production in productions:
        firsts = grammar.firsts.get(production[0], [production[0]])

        if '&' in firsts:
          firsts.remove('&')
          for follow in grammar.follows[nt]:
            table[(nt, follow)] = production

        for first in firsts:
          table[(nt, first)] = production

    grammar.llTable = table
    return grammar

  def readInputLL(self, input):
    """
    Lê uma entrada, utilizando a tabela de análise preditivo LL(1)
    
    Parameters
    ----------
    input: str
      valor da entrada
    """

    input = input.split()
    input += ['$']

    grammar = self
    if not self.llTable:
      grammar = self.buildLLTable()

    stack = ['$', grammar.nterminals[0]]
    read = input.pop(0)

    while True:
      if read == stack[-1] and read == '$':
        return True
      elif read == stack[-1] and read != '$':
        stack.pop()
        read = input.pop(0)
      elif stack[-1] in grammar.nterminals and grammar.llTable.get((stack[-1], read), ''):
        aux = grammar.llTable[(stack.pop(), read)][::-1]
        if aux != ['&']:
          stack += aux
      else:
        return False

  def goto(self, closure_set, value):
    """
    Computa a função 'Go To' para determinado conjunto de itens LR(0) através de um terminal ou não-terminal
    
    Parameters
    ----------
    closure_set: list
      conjunto de itens LR(0)
    value: str
      terminal ou não-terminal para computar
    """

    items = dict()
    for (nt, production) in [(nt, production) for (nt, productions) in closure_set for production in productions]:
      index = production.index('.')

      if index != len(production) - 1 and production[index + 1] == value:
        production[index], production[index + 1] = production[index + 1], production[index]
        items[nt] = items.get(nt, []) + [production]
      
    return list(items.items())

  def closure(self, items):
    """
    Computa a função 'Closure' para determinado conjunto de itens LR(0)
    
    Parameters
    ----------
    items: list
      Lista de itens LR(0)
    """

    closure_set = items
    while True:
      size = len(closure_set)

      for production in [production for (_, productions) in closure_set for production in productions]:
        index = production.index('.')

        if index != len(production) - 1 and production[index + 1] in self.nterminals:
          for x in [(production[index + 1], [['.'] + (x if x != ['&'] else []) for x in self.productions[(production[index + 1], )]])]:
            if x not in closure_set: closure_set.append(x)
      
      if len(closure_set) == size:
        break

    return closure_set

  def generateLRSet(self):
    """Gera a Coleção LR(0) Canônica de determinada gramática"""

    new_productions = {(self.nterminals[0] + '*', ): [[self.nterminals[0]]]}
    new_productions.update(self.productions)

    grammar = Grammar(new_productions)
    grammar = Grammar.eliminateLeftRecursion(Grammar(new_productions))
    grammar.generateFollowSet()

    lrSet = [grammar.closure([(grammar.nterminals[0], [['.'] + x for x in grammar.productions[(grammar.nterminals[0], )]])])]

    while True:
      size = len(lrSet)

      for item in deepcopy(lrSet):
        for value in grammar.nterminals + grammar.terminals:
          new_closure = grammar.goto(deepcopy(item), value)
          if new_closure: 
            new_closure = sorted(grammar.closure(deepcopy(new_closure)))
            if new_closure not in lrSet: 
              lrSet += [new_closure]

      if size == len(lrSet):
        break
    
    grammar.lrSet = lrSet
    return grammar

  def buildSLRTable(self):
    """Constrói a tabela de análise SLR"""

    grammar = self.generateLRSet()
    action = dict.fromkeys(product(range(len(grammar.lrSet)), [x for x in grammar.terminals if x != '&'] + ['$']), '')
    goto = dict.fromkeys(product(range(len(grammar.lrSet)), grammar.nterminals), '')
    for items in grammar.lrSet:
      for (nt, production) in [(nt, production) for (nt, productions) in items for production in productions]:
        index = production.index('.')

        if index != len(production) - 1 and production[index + 1] in grammar.terminals:
          indexTarget = grammar.lrSet.index(sorted(grammar.closure(grammar.goto(deepcopy(items), production[index + 1]))))
          action[(grammar.lrSet.index(items), production[index + 1])] = ('S', indexTarget)
        elif index == len(production) - 1 and nt != grammar.nterminals[0]:
          for follow in grammar.follows[nt]:
            action[(grammar.lrSet.index(items), follow)] = ('R', (nt, production[0:-1]))
        elif index == len(production) - 1 and nt == grammar.nterminals[0]:
          action[(grammar.lrSet.index(items), '$')] = ('acc', )

        if index != len(production) - 1 and production[index + 1] in grammar.nterminals:
          indexTarget = grammar.lrSet.index(sorted(grammar.closure(grammar.goto(deepcopy(items), production[index + 1]))))
          goto[(grammar.lrSet.index(items), production[index + 1])] = indexTarget

    grammar.slrTableAction = action
    grammar.slrTableGoTo = goto

    return grammar

  def readInputSLR(self, input):
    """
    Lê uma entrada, utilizando a tabela de análise SLR(1)
    
    Parameters
    ----------
    input: str
      valor da entrada
    """

    input = input.split()
    input += ['$']

    grammar = self
    if not self.slrTableAction or not self.slrTableGoTo:
      grammar = self.buildSLRTable()

    stack = [0]
    read = input.pop(0)
    while True:
      result = grammar.slrTableAction.get((stack[-1], read), '')
      
      if not result:
        return False
      elif result[0] == 'S':
        stack.append(result[1])
        read = input.pop(0)
      elif result[0] == 'R':
        [stack.pop() for _ in range(len(result[1][1]))]
        stack.append(grammar.slrTableGoTo[(stack[-1], result[1][0])])
      elif result[0] == 'acc':
        return True
      else:
        return False

  def saveToFile(self, arquivo):
    """
    Salva a gramática em um arquivo especificado
    
    Parameters
    ----------
    arquivo: str
      caminho do arquivo
    """

    original_stdout = sys.stdout 
    with open(arquivo, 'w') as f:
      sys.stdout = f
      self.printGrammar()
      sys.stdout = original_stdout

  @staticmethod
  def factorate(grammar):
    """
    Remove a ambiguidade em produções da gramática
    
    Parameters
    ----------
    grammar: Grammar object
      instância de uma gramática
    """

    def eliminateDirect(productions):
      """
      Remove a ambiguidade direta, em produções
      
      Parameters
      ----------
      productions: list
        lista de produções de um não terminal
      """

      count = 1
      new_productions = dict()
      for elt, items in groupby(sorted(productions), itemgetter(0)):
        items = list(items)
        if len(items) > 1:
          new_productions[(nt, )] = new_productions.get((nt, ), []) + [[elt, f'{nt}{count}']]
          new_productions[(f'{nt}{count}', )] = new_productions.get((f'{nt}{count}', ), []) + [x[1:] or ['&'] for x in items]
          count += 1
        else:
          new_productions[(nt, )] = new_productions.get((nt, ), []) + items
      return new_productions

    def eliminateIndirect(productions, visited):
      """
      Deriva produções indiretas em produções diretas
      
      Parameters
      ----------
      productions: list
        lista de produções de um não terminal
      visited: list
        lista de não terminais já visitados
      """

      while True:
        lr = [prod for prod in productions if prod[0] in grammar.nterminals and prod[0] not in visited] # Produções com ambiguidade indireta
        nr = [prod for prod in productions if prod[0] not in grammar.nterminals or prod[0] in visited]  # Produções sem ambiguidade indireta
        visited += [prod[0] for prod in lr]

        if lr:
          lr = [([] if y == ['&'] and x[1:] else y) + x[1:] for x in lr for y in old_productions[(x[0],)]]
          return eliminateIndirect(lr + nr, visited)
        else:
          break
      return nr

    if not grammar.isGLC():
      raise Exception('A gramática deve ser livre de contexto!')

    old_productions = grammar.productions
    counter = 0
    limit = 100
    while True:
      new_productions = dict()
      for ((nt,), productions) in old_productions.items():
        new_productions.update(eliminateDirect(productions))

      counter += 1
      if counter >= limit:
        raise Exception('Limite de execuções atingido! Talvez a gramática seja inerentemente ambígua...')

      if new_productions == old_productions:
        break
      else:
        old_productions = new_productions

    while True:
      new_productions = dict()
      for ((nt,), productions) in old_productions.items():
        indirect = eliminateDirect(eliminateIndirect(productions, [nt]))
        if len(indirect.keys()) > 1:
          new_productions.update(indirect)
        else:
          new_productions.update({(nt, ): old_productions[(nt, )]})

      counter += 1
      if counter >= limit:
        raise Exception('Limite de execuções atingido! Talvez a gramática seja inerentemente ambígua...')

      if new_productions == old_productions:
        break
      else:
        old_productions = new_productions

    return Grammar(new_productions)

  @staticmethod
  def eliminateLeftRecursion(grammar):
    """
    Remove a recursão à esquerda em produções da gramática
    
    Parameters
    ----------
    grammar: Grammar object
      instância de uma gramática
    """

    def eliminateDirectLeftRecursion(productions):
      """
      Remove a recursão direta, em produções
      
      Parameters
      ----------
      productions: list
        lista de produções de um não terminal
      """

      new_productions = dict()
      lr = [prod for prod in productions if nt == prod[0]]  # Produções com recursão direta à esquerda
      nr = [prod for prod in productions if nt != prod[0]]  # Produções sem recursão

      if lr:
        lr = [prod[1:] + [f'{nt}\''] for prod in lr] + [['&']]
        nr = [prod + [f'{nt}\''] for prod in nr] or [f'{nt}\'']

      new_productions[(nt, )] = nr
      if lr: new_productions[(f'{nt}\'', )] = lr

      return new_productions

    def eliminateRecursion(productions, limit=100, counter=0):
      """
      Deriva recursões indiretas em recursões diretas
      
      Parameters
      ----------
      productions: list
        lista de produções de um não terminal
      limit [default=100]: int
        limite de execuções
      counter [default=0]: int
        contador de execuções
      """

      while True:
        lr = [prod for prod in productions if prod[0] in visited]     # Produções com recursão indireta
        nr = [prod for prod in productions if prod[0] not in visited] # Produções sem recursão indireta

        if counter >= limit:
          raise Exception('Limite de execuções atingido! Talvez a gramática seja inerentemente recursiva...')

        if lr:
          lr = [(y if y != ['&'] else []) + x[1:] for x in lr for y in new_productions[(x[0],)]]
          return eliminateRecursion(lr + nr, limit, counter + 1)
        else:
          break

      return nr

    if not grammar.isGLC():
      raise Exception('A gramática deve ser livre de contexto!')

    visited = []
    new_productions = dict()
    for ((nt,), productions) in grammar.productions.items():
      new_productions.update(eliminateDirectLeftRecursion(eliminateRecursion(productions)))
      visited.append(nt)

    return Grammar(new_productions)

  @staticmethod
  def fromFile(arquivo):
    """
    Lê um arquivo e retorna uma gramática
    
    Parameters
    ----------
    arquivo: str
      caminho do arquivo
    """

    try:
      file = open(arquivo).readlines()
      file = [row.strip().split('->') for row in file if row[0:2] != '--']

      productions = dict()
      for row in file:
        if row[0] and row[1:][0] and row[0][0:2] != '--':
          nterminal = row[0].split()
          terminals = row[1].split('|')
          productions[tuple(nterminal)] = productions.get(tuple(nterminal), []) + [x.split() for x in terminals]
    except:
      raise Exception('Arquivo inválido!')
    
    return Grammar(productions)