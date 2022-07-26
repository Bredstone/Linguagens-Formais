from AF import AF
from Tree import Tree

class ER:
  """
  Uma classe usada para representar expressões regulares

  Attributes
  ----------
  expression: str
    expressão regular
  tree: Tree object
    árvore de derivação
  """

  def __init__(self, expression):
    """
    Parameters
    ----------
    expression: str
      expressão regular
    tree: Tree object
      árvore de derivação
    """

    expression = expression.replace(' ', '').replace('|', '+') + '#'

    self.expression = ''
    for c in range(len(expression) - 1):
      self.expression += expression[c]

      if (expression[c] in ['+', '.'] and expression[c + 1] in ['+', '.', '*'] or 
          expression[c] == '*' and expression[c + 1] == '*' or 
          expression[c] == '(' and expression[c + 1] == ')'):
        raise Exception('Expressão inválida!')

      if expression[c] not in ['+', '.', '('] and expression[c + 1] not in ['*', '.', '+', ')']:
        self.expression += '.'
    self.expression += '#'

    self.tree = self.generateERTree()

  def generateERTree(self):
    """Gera e retorna a árvore de derivação da expressão regular"""
    
    def private(start, end):
      """
      Insere, na árvore de derivação, um trecho da expressão regular, caractere por caractere
      
      Parameters
      ----------
      start: int
        índice inicial da subexpressão
      end: int
        índice final da subexpressão
      """

      tree = Tree()
      index = end
      while index >= start:
        if any(index == x for _, x in indexes if x != end):
          [(x, y)] = [(start, end) for start, end in indexes if end == index]
          tree.insert(private(x, y))
          index = x
          pass
        elif self.expression[index] not in ['(', ')']:
          tree.insert(self.expression[index])
        index -= 1

      return tree

    aux = []
    indexes = []
    try:
      for index in range(len(self.expression)):
        if self.expression[index] == '(':
          aux.append(index)
        if self.expression[index] == ')':
          indexes.append((aux.pop(), index + 1 if self.expression[index + 1] == '*' else index))
        if self.expression[index] == '*' and self.expression[index - 1] != ')':
          indexes.append((index - 1, index))

      if len(aux) > 0:
        raise Exception()
    except:
      raise Exception('Expressão inválida!')

    return private(0, len(self.expression) - 1)

  def toAF(self):
    """Converte a expressão regular para um autômato finito"""

    follow_pos = self.tree.followPos()
    
    dstates = [sorted([x.index for x in self.tree.root.firstPos()])]
    visited = []
    dtran = dict()
    while dstates:
      visited.append(dstates.pop())
      for terminal in set([self.tree.dict[x] for x in visited[-1] if self.tree.dict[x] != '#']):
        union = []
        union += [y for x in visited[-1] for y in follow_pos[x] if self.tree.dict[x] == terminal]
        union = sorted(list(set(union)))

        if union not in visited and union not in dstates:
          dstates.append(union)

        dtran[str(visited[-1]), str(union)] = dtran.get((str(visited[-1]), str(union)), []) + [terminal]

    new_states = dict()
    for i in range(1, len(visited) + 1):
      new_states[str(visited[i - 1])] = i
    
    new_transitions = dict()
    for ((fonte, destino), terminal) in dtran.items():
      new_transitions[(new_states[str(fonte)], new_states[str(destino)])] = terminal
    
    return AF(list(new_states.values()), new_transitions, 1, [new_states[str(x)] for x in visited if any(self.tree.dict[y] == '#' for y in x)])