# **Sistema Manipulador de Linguagens Formais**

Sistema manipulador de linguagens regulares e livres de contexto, desenvolvido em Python.

## **Execução**
Para executar o programa:
```
pip install requirements.txt
python3 src/main.py
```

Será exibido, então, no prompt de comandos, um menu de seleção, onde o usuário poderá navegar utilizando as setas "para cima" e "para baixo" do teclado.

### **Carregar autômato**
Ao selecionar a opção de carregar um autômato, o usuário será capaz de fazer o upload, para o programa, de um arquivo contendo um autômato finito;
Quando o caminho do arquivo for indicado, o autômato carregado ficará armazenado na memória, permitindo sua manipulação;
Os arquivos lidos pelo software seguem o seguinte padrão:
```
-- Comentário ou descrição da linguagem

*vertices N
-- Onde "N" é o número de estados
-- Os estados serão, então, numerados de 1 a "N"
*initial N0
-- Onde "N0" é o índice do estado inicial
*final F1 F2 ... Fn
-- Onde "F1 F2 ... Fn" é o conjunto de índices de estados finais, do autômato
*transitions
X > Y | a1 a2 ... an
-- Onde "X" e "Y" são índices de estados pertencentes ao autômato e "a1 a2 ... an" é uma lista de terminais
-- "X > Y | a1 a2 ... an" significa que "X" transiciona para "Y" via "a1 a2 ... an"
```

Uma série de arquivos de teste/exemplo pode ser encontrada sob o diretório "tests", na raiz do projeto.

### **Ler entrada**
Caso o usuário deseje verificar se determinada entrada de dados é aceita por um autômato finito, se deve selecionar esta opção;

O algoritmo solicitará que seja escolhido um autômato, da base de dados do programa e, em seguida, fará a solicitação de uma string de entrada;

Será impresso na tela, por fim, se a entrada fornecida é ou não aceita pela AF escolhida.

### **Converter AFND > AFD**
Esta opção utiliza o algoritmo de conversão de autômatos finitos não-determinísticos para autômatos finitos determinísticos;

O usuário será instruído a escolher um AFND, da base de dados do programa;

O software apresentará a tabela de transições do AFND convertido.

### **Minimizar AF**
Quando selecionada, esta função requisita a escolha de um autômato, da base de dados, e realiza a minimização do mesmo;

O algoritmo funciona através da eliminação de estados inalcançáveis, mortos e de mesma classe de equivalência;

Ao término da execução, é impresso, na tela, a tabela de transições do AF minimizado.

### **União de AFs**
Realiza a união de dois autômatos finitos, gerando um autômato finito não-determinístico;

Será solicitado ao usuário que sejam selecionados dois AFs previamente carregados e será feita a união dos dois;

O autômato resultante será impresso em tela.

### **Interseção de AFs**
Esta ferramenta permite a interseção, através do produto cartesiano, de dois autômatos finitos;

O software pedirá que sejam escolhidos dois AFs e realizará a interseção dos dois;

O resultado será impresso em tela, como uma tabela de transições.

### **Converter ER > AFD**
Ao selecionar esta opção, o programa requisitará a entrada de uma expressão regular;

Expressões regulares reconhecem caracteres, caracteres reservados ("+", ".", "*", "(", ")") e épsilon (representado pelo caractere "&"), mas elimina espaços em branco;

Quando inserida uma ER válida, o software utilizará a árvore de derivação para converter a expressão em um AF;

O novo AF criado será apresentado, no terminal, na forma de tabela de transições.

### **Carregar gramática**
Ao selecionar a opção de carregar uma gramática, o usuário será capaz de fazer o upload, para o programa, de um arquivo contendo uma gramática;

Quando o caminho do arquivo for indicado, a gramática carregada ficará armazenada na memória, permitindo sua manipulação;

Os arquivos lidos pelo software seguem o seguinte padrão:

```
-- Comentário ou descrição da gramática

X -> produção1 | produção2 | ... | produçãoN
-- Onde "X" é a cabeça da produção
-- Onde "produção1 ... N" é o conjunto de produções com cabeça "X"
-- Os símbolos terminais são aqueles iniciados com letra minúscula
-- Os símbolos não-terminais são aqueles iniciados com letra maiúscula
-- Os símbolos de cada produção devem ser separados por espaços em branco
-- Diversas produções, com a mesma cabeça, podem ser representadas na mesma linha, utilizando o caractere "|"
```

Uma série de arquivos de teste/exemplo pode ser encontrada sob o diretório "tests", na raiz do projeto.

### **Eliminar recursão à esquerda**
Quando selecionada, esta função requisita a escolha de uma gramática, da base de dados, e realiza a eliminação de recursão à esquerda do mesmo;

O algoritmo funciona em gramáticas sem ciclos e sem épsilon-produções;

Ao término da execução, é impressa, na tela, a nova gramática gerada.

### **Fatorar gramática**
Esta opção elimina a ambiguidade entre produções que iniciem com a mesma forma sentencial;

O usuário será instruído a escolher uma gramática, da base de dados do programa;

O software apresentará a nova gramática fatorada.

### **Ler entrada [preditivo LL(1)]**
É possível verificar se determinada entrada de dados é aceita por uma gramática, através desta opção;

O algoritmo solicitará que seja escolhida uma gramática, da base de dados do programa e, em seguida, fará a solicitação de uma string de entrada;

Será construída uma tabela de análise preditivo LL(1), assim como os componentes necessários para modelagem da tabela;

O programa fará o reconhecimento da entrada, através de um analisador sintático preditivo;

Por fim, será impresso em tela se a entrada fornecida é ou não aceita pela gramática escolhida.

### **Ler entrada [SLR(1)]**
É possível verificar se determinada entrada de dados é aceita por uma gramática, através desta opção;

O algoritmo solicitará que seja escolhida uma gramática, da base de dados do programa e, em seguida, fará a solicitação de uma string de entrada;

Será construída uma tabela de análise SLR, assim como os componentes necessários para modelagem da tabela;

O programa fará o reconhecimento da entrada, através de um analisador sintático SLR(1);

Por fim, será impresso em tela se a entrada fornecida é ou não aceita pela gramática escolhida.

### **Menu de manipulação de arquivo**

  #### Salvar como arquivo
  Quando um novo autômato é criado, o usuário pode optar por salvar o AF resultante, para utilização futura, no programa;
  
  Ao selecionar "Salvar como arquivo", o software requisita que seja informado um nome para o novo arquivo;
  
  O AF é salvo, então, no formato lido pelo programa (apresentado previamente).

  #### Salvar como tabela de transições
  O usuário pode optar, também, por salvar o AF no formato de tabela de transições, facilitando a sua leitura;
  
  Para isso, será solicitado o nome do arquivo a ser criado e o autômato será salvo;
  
  Um AF salvo como tabela de transições NÃO PODE ser carregado no programa, para uso futuro, por não se adequar ao formato lido.

  #### Carregar
  Ao selecionar esta opção, o AF gerado será carregado na base de dados do software;
  
  Um nome para o autômato será requisitado;
  
  O AF carregado no programa NÃO SERÁ SALVO no disco, sendo assim, após a execução, o autômato será perdido.