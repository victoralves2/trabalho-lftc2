O arquivo principal está no .py, os arquivos de texto não são necessários, caso eles não estejam na pasta o programa os cria automaticamente com os dados das máquinas de turing
O programa tem um menu interativo bem facil de usar, apenas cuidado na hora de escrever as cadeias para NÂO colocar nenhum espaço em branco 

para rodar o programa no terminal: python mturing.py

-INVERSOR DE BITS: 
apenas escrever uma cadeia de 0's e 1's e elá apresentará o inverso
Exemplo de entrada válida: 1101 ou 0011 ou 0101100

---------------------------------------------------------------
-VERIFICADOR DE QUANTIDADE PARES DE A'S: 
aceita cadeias que possuam apenas quantidades pares de A's
Alfabeto aceito: a e b
Exemplo de entrada válida: aab

--------------------------------------------------------------
-SOMA DE NUMEROS:
Exemplo de entrada válida: 111+11 
Os números devem ser escritos apenas por quantidades de 1's caso queira escrever 0 deixe em branco 
LEMBRE DE SEPARAR OS NUMEROS USANDO '+'

--------------------------------------------------------------
-LINGUAGEM a^n b^n:
Exemplo de entrada válida: aabb 
Exemplo de entrada válida: aabb (n=2) ou aaabbb (n=3).

--------------------------------------------------------------
-ARQUIVO PERSONALISADO:
caso queira testar uma maquina de turing própria:
Abra o arquivo arquivo_mt.txt no seu editor de texto, cole as regras de transição de um novo exercício passado pelo professor e escolha a Opção 2 no menu principal para testá-lo.

Exemplo Completo Comentado (inversor.txt)
Plaintext
e{0,1}          # 1. Estados da máquina (0 e 1)
a{0,1}          # 2. Alfabeto aceito na fita (0 e 1)
i0              # 3. Estado inicial é o 0
f{1}            # 4. Estado final é o 1
(0,0){0,1,R}    # 5. Transição 1: Se está no estado 0 e lê '0', escreve '1', continua no estado 0 e move a direita (R)
(0,1){0,0,R}    # 6. Transição 2: Se está no estado 0 e lê '1', escreve '0', continua no estado 0 e move a direita (R)
(0,B){1,B,R}    # 7. Transição 3: Se está no estado 0 e lê o fim da fita ('B'), mantém o 'B', vai para o estado final 1 e move a direita (R)



