import itertools
from AF import AF

class AFND(AF):
  """
  Uma classe usada para representar autômatos finitos não-determinísticos

  Extends
  ----------
  classe AF

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

  def __init__(self, AF):
    """
    Parameters
    ----------
    AF: AF object
      instância de um autômato finito
    """

    super().__init__(AF.vertices, AF.transitions, AF.initial, AF.final)

    if not super().isAFND():
      raise Exception('O autômato é determinístico!')

  def calcFecho(self, vertice):
    """
    Calcula o ε-fecho de determinado estado

    Parameters
    ----------
    vertice: int
      estado
    """

    return [vertice] + list(itertools.chain(*[self.calcFecho(x) for x in self.transit(vertice, '&') if x != vertice]))

  def readInput(self, input):
    """
    Verifica se o autômato reconhece determinada cadeia de entrada

    Parameters
    ----------
    input: str
      cadeia de caracteres de entrada
    """

    fecho = dict(zip(self.vertices, [self.calcFecho(vertice) for vertice in self.vertices]))
    
    cs = fecho[self.initial]
    for t in input:
      cs = [y for vertice in cs for x in self.transit(vertice, t) for y in fecho[x]]

    return any([x in self.final for x in cs])

  def toAFD(self):
    """
    Converte o autômato finito não-determinístico para um autômato finito determinístico
    """

    from AFD import AFD

    fecho = dict(zip(self.vertices, [self.calcFecho(vertice) for vertice in self.vertices]))

    new_vertices = {str(fecho[self.initial]): 1}
    new_transitions = dict()
    new_final = []
    count = 1

    current_states = [fecho[self.initial]]
    for vertices in current_states:
      for terminal in [t for t in self.terminals if t != '&']:
        aux = sorted(set([y for vertice in vertices for x in self.transit(vertice, terminal) for y in fecho[x]]))
        if aux not in current_states:
          count += 1
          new_vertices[str(aux)] = count
          
          if any([x in self.final for x in aux]):
            new_final.append(new_vertices[str(aux)])
          
          current_states.append(aux)

        new_transitions[new_vertices[str(vertices)], new_vertices[str(aux)]] = new_transitions.get((new_vertices[str(vertices)], new_vertices[str(aux)]), []) + [terminal]

    return AFD(AF(list(new_vertices.values()), new_transitions, 1, new_final))

  @staticmethod
  def union(AF1, AF2):
    """
    Faz a união de dois autômatos finitos, em um autômato finito não-determinístico
    
    Parameters
    ----------
    AF1: AF object
      instância de um autômato finito
    AF2: AF object
      instância de um autômato finito
    """

    return AFND(AF.union(AF1, AF2))

  @staticmethod
  def intersection(AF1, AF2):
    """
    Faz a intersecção, por meio do produto cartesiano, de dois autômatos finitos, em um autômato finito não-determinístico
    
    Parameters
    ----------
    AF1: AF object
      instância de um autômato finito
    AF2: AF object
      instância de um autômato finito
    """

    return AFND(AF.intersection(AF1, AF2))

  @staticmethod
  def fromFile(arquivo):
    """
    Lê um arquivo e retorna um autômato finito não-determinístico
    
    Parameters
    ----------
    arquivo: str
      caminho do arquivo
    """

    return AFND(AF.fromFile(arquivo))