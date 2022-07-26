import sys
import itertools
from tabulate import tabulate

class AF:
  """
  Uma classe usada para representar autômatos finitos

  Attributes
  ----------
  vertices: list
    lista com os estados do autômato
  transitions: dict
    dicionário de transições do autômato
  initial: int
    estado inicial
  final: list
    lista de estados de aceitação
  """

  def __init__(self, vertices, transitions, initial, final):
    """
    Parameters
    ----------
    vertices: list
      lista com os estados do autômato
    transitions: dict
      dicionário de transições do autômato
    initial: int
      estado inicial
    final: list
      lista de estados de aceitação
    """

    if not all([x in vertices for x in set(itertools.chain(*transitions))]):
      raise Exception('Transições entre estados inexistentes não são permitidas!')
    if not initial in vertices:
      raise Exception('Estado inicial não encontrado!')
    if not all(x in vertices for x in final):
      raise Exception('Estado(s) de aceitação não encontrado(s)!')

    self.vertices = vertices
    self.transitions = transitions
    self.initial = initial
    self.final = final
    self.terminals = sorted(set(itertools.chain(*transitions.values())))

  def transit(self, vertice, terminal):
    """
    Retorna os possíveis próximos estados, a partir de um terminal
    
    Parameters
    ----------
    vertice: int
      estado atual
    terminal: str
      símbolo terminal
    """

    return [ns for (cs, ns), x in self.transitions.items() if cs == vertice and terminal in x]

  def isAFND(self):
    """Verifica se o autômato é não-determinístico"""

    if '&' in self.terminals:
      return True

    for (vertice, terminal) in itertools.product(self.vertices, self.terminals):
      aux = self.transit(vertice, terminal)
      if len(aux) > 1:
        return True

    return False

  def toTable(self):
    """Retorna o autômato em formato de tabela de transições"""

    data = dict.fromkeys(self.terminals)

    if not data:
      raise Exception('Autômato vazio!')

    for terminal in self.terminals:
      data[terminal] = [', '.join(map(str, self.transit(vertice, terminal))).strip() or '-' for vertice in self.vertices]

    index = len(self.vertices)*['']
    for i in range(len(self.vertices)):
      if self.vertices[i] == self.initial:
        index[i] += '-> '
      if self.vertices[i] in self.final:
        index[i] += '* '
      index[i] += str(self.vertices[i])

    return tabulate(data, headers='keys', showindex=index, tablefmt='presto', colalign=('right',))

  def printAF(self):
    """Imprime o autômato em formato de tabela de transições"""
    
    print (self.toTable())

  def printToFile(self, arquivo):
    """
    Imprime, em um arquivo, o autômato em formato de tabela de transições
    
    Parameters
    ----------
    arquivo: str
      caminho do arquivo
    """

    original_stdout = sys.stdout 
    with open(arquivo, 'w') as f:
      sys.stdout = f
      self.printAF()
      sys.stdout = original_stdout

  def saveToFile(self, arquivo):
    """
    Salva o autômato finito em um arquivo especificado
    
    Parameters
    ----------
    arquivo: str
      caminho do arquivo
    """

    original_stdout = sys.stdout 
    with open(arquivo, 'w') as f:
      sys.stdout = f

      print ('*vertices', len(self.vertices))
      print ('*initial', self.initial)
      print ('*final', *self.final)
      print ('*transitions')
      for (fonte, destino), transition in self.transitions.items():
        print (str(fonte) + ' > ' + str(destino) + ' | ', end = '')
        print (*transition)
      
      sys.stdout = original_stdout

  @staticmethod
  def removeUnreachable(af):
    """
    Remove estados inalcançáveis de um autômato finito
    
    Parameters
    ----------
    af: AF object
      instância de um autômato finito
    """

    def private(vertice, visited):
      """
      Através de recursão, retorna os estados alcançáveis do autômato
      
      Parameters
      ----------
      vertice: int
        vértice inicial para realizar a busca
      visited: list
        lista de vértices já visitados, pelo algoritmo
      """

      visited.append(vertice)
      [private(destino, visited) for (fonte, destino) in af.transitions.keys() if fonte == vertice and destino not in visited]
      return sorted(visited)
    
    new_vertices = private(af.initial, [])
    new_transitions = dict([((fonte, destino), value) for ((fonte, destino), value) in af.transitions.items() if fonte in new_vertices and destino in new_vertices])

    return AF(new_vertices, new_transitions, af.initial, [vertice for vertice in af.final if vertice in new_vertices])

  @staticmethod
  def removeDead(af):
    """
    Remove estados mortos de um autômato finito
    
    Parameters
    ----------
    af: AF object
      instância de um autômato finito
    """

    def private(vertices, visited):
      """
      Através de recursão, retorna os estados não mortos do autômato
      
      Parameters
      ----------
      vertices: list
        lista de estados para realizar a busca
      visited: list
        lista de vértices já visitados, pelo algoritmo
      """

      if vertices:
        visited += list(set(vertices))
        private([fonte for (fonte, destino) in af.transitions.keys() if destino in vertices and fonte not in visited], visited)
      return sorted(set(visited))
    
    new_vertices = private(af.final, [])
    new_transitions = dict([((fonte, destino), value) for ((fonte, destino), value) in af.transitions.items() if fonte in new_vertices and destino in new_vertices])

    return AF(new_vertices, new_transitions, af.initial, [vertice for vertice in af.final if vertice in new_vertices])

  @staticmethod
  def equivalenceClasses(af):
    """
    Remove estados com mesma classe de equivalência de um autômato finito
    
    Parameters
    ----------
    af: AF object
      instância de um autômato finito
    """

    def getKey(vertice, classes):
      """
      Retorna a classe de determinado estado
      
      Parameters
      ----------
      vertice: int
        estado do autômato
      classes: dict
        dicionário de classes do autômato
      """

      for (key, value) in classes.items(): 
        if vertice in value: return key

    def private(classes):
      """
      Através de recursão, separa os estados do autômato em classes de equivalência
      
      Parameters
      ----------
      classes: dict
        dicionário de classes do autômato
      """

      new_classes = dict()
      new_classes_dict = dict()
      for vertice in af.vertices:
        aux = [x for terminal in af.terminals for x in sorted(af.transit(vertice, terminal)) or [0]]
        index = str([getKey(vertice, classes)] + [getKey(x, classes) or 0 for x in aux])
        new_classes_dict[index] = sorted(new_classes_dict.get(index, []) + [vertice])
      for i in range(1, len(new_classes_dict) + 1):
        new_classes[i] = new_classes_dict[list(new_classes_dict.keys())[i - 1]]
      return new_classes if len(new_classes) == len(classes) else private(new_classes)

    classes = private({1: set(af.vertices) ^ set(af.final), 2: af.final})

    new_transitions = dict()
    for ((fonte, destino), value) in af.transitions.items():
      fonte = getKey(fonte, classes)
      destino = getKey(destino, classes)
      new_transitions[(fonte, destino)] = new_transitions.get((fonte, destino), []) + value

    return AF(list(classes.keys()), new_transitions, getKey(af.initial, classes), [getKey(final, classes) for final in af.final])

  @staticmethod
  def minimize(af):
    """
    Faz a minimização de estados de um autômato finito
    
    Parameters
    ----------
    af: AF object
      instância de um autômato finito
    """

    return AF.equivalenceClasses(AF.removeDead(AF.removeUnreachable(af)))

  @staticmethod
  def union(AF1, AF2):
    """
    Faz a união de dois autômatos finitos
    
    Parameters
    ----------
    AF1: AF object
      instância de um autômato finito
    AF2: AF object
      instância de um autômato finito
    """

    total = len(AF1.vertices) + 1

    nv = [total] + [x + total for x in AF2.vertices]
    nf = [x + total for x in AF2.final]
    nt = dict(zip([(x + total, y + total) for (x, y) in AF2.transitions.keys()], AF2.transitions.values()))
    nt[(total, AF1.initial)] = ['&']
    nt[(total, AF2.initial + total)] = ['&']
    nt.update(AF1.transitions)

    return AF(AF1.vertices + nv, nt, total, AF1.final + nf)

  @staticmethod
  def intersection(AF1, AF2):
    """
    Faz a intersecção, por meio do produto cartesiano, de dois autômatos finitos
    
    Parameters
    ----------
    AF1: AF object
      instância de um autômato finito
    AF2: AF object
      instância de um autômato finito
    """

    new_vertices = list(itertools.product(AF1.vertices, AF2.vertices))
    new_vertices_dict = dict(zip(new_vertices, range(1, len(new_vertices) + 1)))
    new_initial = new_vertices_dict[(AF1.initial, AF2.initial)]
    new_final = [new_vertices_dict[(final_af1, final_af2)] for final_af1 in AF1.final for final_af2 in AF2.final]

    new_transitions = dict()
    for (vertice1, vertice2) in new_vertices:
      for terminal in set(AF1.terminals + AF2.terminals):
        af1_transition = AF1.transit(vertice1, terminal)
        af2_transition = AF2.transit(vertice2, terminal)
        fonte = new_vertices_dict[(vertice1, vertice2)]

        if terminal == '&':
          for x in af1_transition:
            destino = new_vertices_dict[(x, vertice2)]
            new_transitions[(fonte, destino)] = new_transitions.get((fonte, destino), []) + [terminal]
          for x in af2_transition:
            destino = new_vertices_dict[(vertice1, x)]
            new_transitions[(fonte, destino)] = new_transitions.get((fonte, destino), []) + [terminal]

        elif af1_transition and af2_transition:
          for x in list(itertools.product(af1_transition, af2_transition)):
            destino = new_vertices_dict[x]
            new_transitions[(fonte, destino)] = new_transitions.get((fonte, destino), []) + [terminal]

    return AF(range(1, len(new_vertices) + 1), new_transitions, new_initial, new_final)

  @staticmethod
  def fromFile(arquivo):
    """
    Lê um arquivo e retorna um autômato finito
    
    Parameters
    ----------
    arquivo: str
      caminho do arquivo
    """

    try:
      file = open(arquivo).readlines()
      file = [row.split() for row in file]

      for row in file:
        if '*vertices' in row:
          n = int(row[1])
        if '*initial' in row:
          initial = int(row[1])
        if '*final' in row:
          final = [int(f) for f in row[1:]]

      vertices = [*range(1, n + 1)]
      transitions = [x for x in file[file.index(['*transitions']) + 1:] if x]
      transitions = dict([((int(a), int(b)), x) for a, _, b, _, *x in transitions])
    except:
      raise Exception('Arquivo inválido!')
    
    return AF(vertices, transitions, initial, final)