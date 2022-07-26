from Node import Node

class Tree:
  """
  Uma classe usada para representar árvores de derivação

  Attributes
  ----------
  root: Node object
    nó raiz, da árvore
  last: Node object
    último nó adicionado
  dict: dict
    dicionário de nós folhas
  """

  def __init__(self):
    self.root = None
    self.last = None
    self.dict = dict()

  def printTree(self):
    """Imprime, na tela, toda a árvore"""

    self.root.print()

  def followPos(self):
    """Calcula a função FollowPos da árvore"""

    def iterate(node):
      """
      Retorna uma lista com os nós pertencentes à uma subárvore
      
      Parameters
      ----------
      node: Node object
        nó raiz da subárvore
      """

      aux = [node]
      if node.l_child:
        aux += iterate(node.l_child)
      if node.m_child:
        aux += iterate(node.m_child)
      if node.r_child:
        aux += iterate(node.r_child)
      return aux

    nodes = iterate(self.root)
    
    count = 1
    for node in nodes:
      if node.isLeaf():
        node.index = count
        self.dict[count] = node.data_value
        count += 1

    follow_pos = dict()
    for node in nodes:
      if node.data_value == '*':
        for lp in node.lastPos():
          follow_pos[lp.index] = follow_pos.get(lp.index, []) + [fp.index for fp in node.firstPos()]
      elif node.data_value == '.':
        for lp in node.l_child.lastPos():
          follow_pos[lp.index] = follow_pos.get(lp.index, []) + [fp.index for fp in node.r_child.firstPos()]
      elif node.isLeaf():
        follow_pos[node.index] = follow_pos.get(node.index, []) + []
    
    return follow_pos

  def insert(self, data):
    """
    Insere, na árvore, um novo nodo
    
    Parameters
    ----------
    data: str
      dado a ser inserido
    """

    # Verifica se o novo dado a ser inserido é uma subárvore
    if isinstance(data, Tree):
      new_node = data.root
    else:
      new_node = Node(data)

    # Caso a árvore esteja vazia, insere o dado na raiz
    if not self.root:
      self.root = new_node
      self.last = self.root
      return

    # Caso a raiz seja * e nenhum outro nodo tenha sido adicionado, insere o dado no filho do meio
    if self.root.data_value == '*' and self.root.isLeaf():
      new_node.parent = self.last
      self.last.m_child = new_node
      self.last = new_node
      return

    # Caso o último nodo inserido seja um operador e o novo dado a ser adicionado seja um terminal ou uma subárvore, o insere na esquerda
    if self.last.isOperator() and (not new_node.isOperator() or isinstance(data, Tree)):
      new_node.parent = self.last
      self.last.l_child = new_node
      self.last = new_node
      return
    
    # Caso o último dado inserido seja um terminal ou uma subárvore e o novo nodo seja um operador, realiza o balanceamento e insere
    if (not self.last.isOperator() or (self.last.l_child or self.last.m_child)) and new_node.isOperator():
      if self.last.parent:
        new_node.parent = self.last.parent
        if self.last.parent.l_child:
          self.last.parent.l_child = new_node
        else:
          self.last.parent.m_child = new_node
        self.last.parent = new_node
      else:
        self.root = new_node
      new_node.r_child = self.last
      self.last = new_node
      return

    raise Exception('Expressão inválida!')