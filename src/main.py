import time
import os

from AF import AF
from AFND import AFND
from AFD import AFD
from ER import ER
from Grammar import Grammar
from Menu import Menu

afs = dict()
grammars = dict()
arquivos = {'AFDS': [], 'AFNDS': [], 'Gramáticas': []}
select_menu = Menu(
  ['Carregar autômato', 
   'Ler entrada', 
   'Converter AFND > AFD', 
   'Minimizar AF', 
   'União de AFs', 
   'Interseção de AFs', 
   'Converter ER > AFD',
   'Carregar gramática',
   'Eliminar recursão à esquerda',
   'Fatorar gramática',
   'Ler entrada [preditivo LL(1)]',
   'Ler entrada [SLR(1)]'])

def afsMenu(title='Selecione um autômato:'):
  if not arquivos['AFDS'] and not arquivos['AFNDS']:
    raise Exception('Nenhum autômato encontrado!')

  select_afs = Menu([y for x in arquivos.values() for y in x], title=title, submenu=True)
  (_, selected) = select_afs.select()

  return (False, False) if selected == 'Voltar' else (AFND(afs[selected]) if afs[selected].isAFND() else AFD(afs[selected]), selected)

def grammarsMenu(title='Selecione uma gramática:'):
  if not arquivos['Gramáticas']:
    raise Exception('Nenhuma gramática encontrado!')

  select_grammars = Menu(arquivos['Gramáticas'], title=title, submenu=True)
  (_, selected) = select_grammars.select()

  return (False, False) if selected == 'Voltar' else (grammars[selected], selected)

def optionsMenu(af, title=''):
  options_menu = Menu(['Salvar como arquivo', 'Salvar como tabela de transições', 'Carregar'], title=title + ':\n\n' + af.toTable(), submenu=True)
  (n, selected) = options_menu.select()

  if selected == 'Voltar':
    return
  elif n == 3:
    arquivo = input(f'Nome do autômato [default={title}]: ') or title
    updateArquivos(af, arquivo)
    return
  elif n == 1:
    af.saveToFile(input('\nNome do arquivo: '))
    print ('\n\033[92mArquivo salvo com sucesso!\033[0m')
  elif n == 2:
    af.printToFile(input('\nNome do arquivo: '))
    print ('\n\033[92mArquivo salvo com sucesso!\033[0m')
  time.sleep(1)

def grammarOptionsMenu(grammar, title=''):
  options_menu = Menu(['Salvar como arquivo', 'Carregar'], title=title + ':\n\n' + grammar.toStr(), submenu=True)
  (n, selected) = options_menu.select()

  if selected == 'Voltar':
    return
  elif n == 2:
    arquivo = input(f'Nome do autômato [default={title}]: ') or title
    updateArquivos(grammar, arquivo)
    return
  elif n == 1:
    grammar.saveToFile(input('\nNome do arquivo: '))
    print ('\n\033[92mArquivo salvo com sucesso!\033[0m')
  time.sleep(1)

def updateArquivos(object, object_name):
  if isinstance(object, AF):
    if object_name not in afs:
      arquivos['AFNDS'].append(object_name) if object.isAFND() else arquivos['AFDS'].append(object_name)
    afs[object_name] = object
  elif isinstance(object, Grammar):
    if object_name not in arquivos:
      arquivos['Gramáticas'].append(object_name)
    grammars[object_name] = object

  out = ''
  if arquivos['AFDS']:
    out += 'AFDS:\n'
    out += '\n'.join(arquivos['AFDS'])
  if arquivos['AFNDS']:
    out += '\n\n' if arquivos['AFDS'] else ''
    out += 'AFNDS:\n'
    out += '\n'.join(arquivos['AFNDS'])
  if arquivos['Gramáticas']:
    out += '\n\n' if arquivos['AFDS'] or arquivos['AFDS'] else ''
    out += 'Gramáticas:\n'
    out += '\n'.join(arquivos['Gramáticas'])
  select_menu.refreshTitle(out)

def op1():
  arquivo = input('\nCaminho do arquivo: ')
  af = AF.fromFile(arquivo)

  updateArquivos(af, arquivo)

def op2():
  (af, _) = afsMenu()

  if af:
    read = input('\nEntrada: ')

    print ('\n\033[92mEntrada válida!\033[0m' if af.readInput(read) else '\n\033[91mEntrada inválida!\033[0m')
    time.sleep(1)

def op3():
  if not arquivos['AFNDS']:
    raise Exception('Nenhum autômato finito não-determinístico encontrado!')

  select_afs = Menu(arquivos['AFNDS'], submenu=True)
  (_, selected) = select_afs.select()

  if selected != 'Voltar':
    af = AFND(afs[selected]).toAFD()
    optionsMenu(af=af, title=f'AFNDtoAFD({selected})')

def op4():
  (af, selected) = afsMenu()

  if af:
    af = AF.minimize(af)

    optionsMenu(af=af, title=f'AF Mínimo({selected})')

def op5():
  (af1, selected1) = afsMenu()

  if af1:
    (af2, selected2) = afsMenu(title='\033[94mAF selecionado: ' + selected1 + '\033[0m')

    if af2:
      af = AF.union(af1, af2)
      optionsMenu(af=af, title=f'União({selected1}, {selected2})')

def op6():
  (af1, selected1) = afsMenu()

  if af1:
    (af2, selected2) = afsMenu(title='\033[94mAF selecionado: ' + selected1 + '\033[0m')

    if af2:
      af = AF.intersection(af1, af2)
      optionsMenu(af=af, title=f'Interseção({selected1}, {selected2})')

def op7():
  os.system('cls||clear')
  read = input('Expressão regular: ')

  af = ER(read).toAF()
  optionsMenu(af=af, title=f'ERtoAF({read})')

def op8():
  arquivo = input('\nCaminho do arquivo: ')
  grammar = Grammar.fromFile(arquivo)

  updateArquivos(grammar, arquivo)

def op9():
  (grammar, selected) = grammarsMenu()

  if grammar:
    grammar = Grammar.eliminateLeftRecursion(grammar)
    grammarOptionsMenu(grammar=grammar, title=f'NonRecursive({selected})')

def op10():
  (grammar, selected) = grammarsMenu()

  if grammar:
    grammar = Grammar.factorate(grammar)
    grammarOptionsMenu(grammar=grammar, title=f'Factorate({selected})')

def op11():
  (grammar, _) = grammarsMenu()

  if grammar:
    read = input('\nEntrada: ')

    print ('\n\033[92mEntrada válida!\033[0m' if grammar.readInputLL(read) else '\n\033[91mEntrada inválida!\033[0m')
    time.sleep(1)

def op12():
  (grammar, _) = grammarsMenu()

  if grammar:
    read = input('\nEntrada: ')

    print ('\n\033[92mEntrada válida!\033[0m' if grammar.readInputSLR(read) else '\n\033[91mEntrada inválida!\033[0m')
    time.sleep(1)

while True:
  (op, _) = select_menu.select()

  try:
    if op == 1:
      op1()
    elif op == 2:
      op2()
    elif op == 3:
      op3()
    elif op == 4:
      op4()
    elif op == 5:
      op5()
    elif op == 6:
      op6()
    elif op == 7:
      op7()
    elif op == 8:
      op8()
    elif op == 9:
      op9()
    elif op == 10:
      op10()
    elif op == 11:
      op11()
    elif op == 12:
      op12()
    elif op == 13:
      break
  except Exception as e:
    print ('\n\033[91m' + str(e) + '\033[0m')
    time.sleep(1)