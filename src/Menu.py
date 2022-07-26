import keyboard
import os

class Menu:
  """
  Uma classe usada para instanciar menus

  Attributes
  ----------
  options: list
    lista com os itens do menu
  selected: int
    índice do item atual selecionado
  title: str
    título do menu
  """

  def __init__(self, options, title='', submenu=False):
    """
    Parameters
    ----------
    options: list
      lista com os itens do menu
    selected: int
      índice do item atual selecionado
    title: str
      título do menu
    """

    self.options = options + (['Sair'] if not submenu else ['Voltar'])
    self.selected = 1
    self.title = title

  def refreshTitle(self, title=''):
    """
    Atualiza o título do menu

    Parameters
    ----------
    title [default='']: str
      novo título do menu
    """

    self.title = title

  def append(self, item):
    """
    Adiciona um novo item ao menu

    Parameters
    ----------
    item: str
      novo item do menu
    """

    self.options.remove('Sair' | 'Voltar')
    if isinstance(item, list):
      [self.options.append(x) for x in item]
    else:
      self.options.append(item)
    self.options.append('Sair' | 'Voltar')

  def remove(self, item):
    """
    Remove um item do menu

    Parameters
    ----------
    item: str
      novo item do menu
    """

    if isinstance(item, list):
      [self.options.remove(x) for x in item if x in self.options and x != 'Sair' and x != 'Voltar']
    elif item in self.options and item != 'Sair' and item != 'Voltar':
      self.options.remove(item)

  def up(self):
    """Move o cursor do menu para cima"""

    if self.selected == 1:
      self.selected = len(self.options) + 1
    self.selected -= 1
    self.show_menu()

  def down(self):
    """Move o cursor do menu para baixo"""

    if self.selected == len(self.options):
      self.selected = 0
    self.selected += 1
    self.show_menu()

  def show_menu(self):
    """Imprime, na tela, o menu"""

    os.system('cls||clear')
    print(self.title + '\n\n' if self.title else '', end='')
    print("Escolha uma opção:")
    for i in range(1, len(self.options) + 1):
      print("{1} {0}. {3} {2}".format(i, '\033[95m>' if self.selected == i else ' ', '<\033[0m' if self.selected == i else ' ', self.options[i - 1]))

  def select(self):
    """Imprime o menu e aguarda até um item ser escolhido"""

    up = keyboard.add_hotkey('up', self.up, suppress=True)
    down = keyboard.add_hotkey('down', self.down, suppress=True)

    self.show_menu()
    
    keyboard.wait('enter', suppress=True)
    keyboard.remove_hotkey(up)
    keyboard.remove_hotkey(down)
    
    return (self.selected, self.options[self.selected - 1])