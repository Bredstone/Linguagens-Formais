class Node:
  """
  Uma classe usada para instanciar nodos de uma árvore de derivação

  Attributes
  ----------
  data_value: str
    valor do nodo
  l_child: Node object
    filho esquerdo, do nodo
  r_child: Node object
    filho direito, do nodo
  m_child: Node object
    filho do meio, do nodo
  parent: Node object
    nodo pai do nodo atual
  index: int
    índice do nodo folha
  """

  def __init__(self, data_value, l_child=None, r_child=None, m_child=None, parent=None, index=0):
    """
    Parameters
    ----------
    data_value: str
      valor do nodo
    l_child: Node object
      filho esquerdo, do nodo
    r_child: Node object
      filho direito, do nodo
    m_child: Node object
      filho do meio, do nodo
    parent: Node object
      nodo pai do nodo atual
    index: int
      índice do nodo folha
    """

    self.data_value = data_value
    self.l_child = l_child
    self.r_child = r_child
    self.m_child = m_child
    self.parent = parent
    self.index = index

  def isLeaf(self):
    """Verifica se o nodo é uma folha"""

    return not self.r_child and not self.l_child and not self.m_child

  def isOperator(self):
    """Verifica se o nodo é um operador"""

    return self.data_value in ['*', '+', '.']

  def isNullable(self):
    """Verifica se o nodo é anulável"""

    if self.data_value in ['*', '&']:
      return True
    elif self.l_child and self.r_child:
      if self.data_value == '+':
        return self.l_child.isNullable() or self.r_child.isNullable()
      elif self.data_value == '.':
        return self.l_child.isNullable() and self.r_child.isNullable()
    return False
  
  def firstPos(self):
    """Retorna o conjunto FirstPos do nodo"""

    if self.data_value == '&':
      return []
    elif self.data_value == '*':
      return self.m_child.firstPos()
    elif self.l_child and self.r_child:
      if self.data_value == '+':
        return self.l_child.firstPos() + self.r_child.firstPos()
      elif self.data_value == '.':
        return self.l_child.firstPos() + self.r_child.firstPos() if self.l_child.isNullable() else self.l_child.firstPos()
    return [self]

  def lastPos(self):
    """Retorna o conjunto LastPos do nodo"""

    if self.data_value == '&':
      return []
    elif self.data_value == '*':
      return self.m_child.lastPos()
    elif self.l_child and self.r_child:
      if self.data_value == '+':
        return self.l_child.lastPos() + self.r_child.lastPos()
      elif self.data_value == '.':
        return self.l_child.lastPos() + self.r_child.lastPos() if self.r_child.isNullable() else self.r_child.lastPos()
    return [self]

  def print(self):
    """Imprime, na tela, o nodo e seus filhos"""

    print (self.data_value)
    if self.r_child:
      print ('Right: ', end='')
      self.r_child.print()
    if self.m_child:
      print ('Middle: ', end='')
      self.m_child.print()
    if self.l_child:
      print ('Left: ', end='')
      self.l_child.print()