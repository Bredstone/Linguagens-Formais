from AF import AF

class AFD(AF):
  """
  Uma classe usada para representar autômatos finitos determinísticos

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

    if super().isAFND():
      raise Exception('O autômato é não-determinístico!')

  def readInput(self, input):
    """
    Verifica se o autômato reconhece determinada cadeia de entrada

    Parameters
    ----------
    input: str
      cadeia de caracteres de entrada
    """
    
    cs = [self.initial]
    for t in input:
      cs = [x for vertice in cs for x in self.transit(vertice, t)]

    return any([x in self.final for x in cs])

  @staticmethod
  def union(AF1, AF2):
    """
    Faz a união de dois autômatos finitos, em um autômato finito determinístico
    
    Parameters
    ----------
    AF1: AF object
      instância de um autômato finito
    AF2: AF object
      instância de um autômato finito
    """

    from AFND import AFND

    return AFND.union(AF1, AF2).toAFD()

  @staticmethod
  def intersection(AF1, AF2):
    """
    Faz a intersecção, por meio do produto cartesiano, de dois autômatos finitos, em um autômato finito determinístico
    
    Parameters
    ----------
    AF1: AF object
      instância de um autômato finito
    AF2: AF object
      instância de um autômato finito
    """

    from AFND import AFND

    return AFND.intersection(AF1, AF2).toAFD()

  @staticmethod
  def fromFile(arquivo):
    """
    Lê um arquivo e retorna um autômato finito determinístico
    
    Parameters
    ----------
    arquivo: str
      caminho do arquivo
    """

    return AFD(AF.fromFile(arquivo))