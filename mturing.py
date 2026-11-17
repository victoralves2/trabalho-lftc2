import os
import re

class MaquinaTuring():
    def __init__(self, 
                 estados: set[str], 
                 alfabeto: set[str], 
                 inicial: str, 
                 final: set[str], 
                 transicoes: dict[tuple[str, str], tuple[str, str, str]]):
        self.estados = estados
        self.alfabeto = alfabeto
        self.inicial = inicial
        self.final = final
        self.transicoes = transicoes

def criar_arquivos_pre_carregados():
    """Cria automaticamente todos os arquivos de configuração se não existirem."""
    arquivos = {
        "inversor.txt": """e{q0,q1}
a{0,1}
iq0
f{q1}
(q0,0){q0,1,R}
(q0,1){q0,0,R}
(q0,B){q1,B,R}
""",
        "par_de_as.txt": """e{q0,q1,q_aceita}
a{a,b}
iq0
f{q_aceita}
(q0,a){q1,a,R}
(q0,b){q0,b,R}
(q0,B){q_aceita,B,R}
(q1,a){q0,a,R}
(q1,b){q1,b,R}
""",
        "soma.txt": """e{q0,q1,q2,q_aceita}
a{1,+}
iq0
f{q_aceita}
(q0,1){q0,1,R}
(q0,+){q1,1,R}
(q1,1){q1,1,R}
(q1,B){q2,B,L}
(q2,1){q_aceita,B,R}
""",
        "an_bn.txt": """e{0,1,2,3,4}
a{a,b}
i0
f{4}
(0,a){1,X,R}
(1,a){1,a,R}
(1,Y){1,Y,R}
(1,b){2,Y,L}
(2,Y){2,Y,L}
(2,a){2,a,L}
(2,X){0,X,R}
(0,Y){3,Y,R}
(3,Y){3,Y,R}
(3,B){4,B,R}
""",
        "arquivo_mt.txt": """e{0,1}
a{0,1}
i0
f{1}
(0,0){0,1,R}
(0,1){0,0,R}
(0,B){1,B,R}
"""
    }

    for nome_arq, conteudo in arquivos.items():
        if not os.path.exists(nome_arq) or os.path.getsize(nome_arq) == 0:
            with open(nome_arq, "w", encoding="utf-8") as f:
                f.write(conteudo)
            print(f"[!] Arquivo padrão criado automaticamente: '{nome_arq}'")

def carregar_mt(nome_arquivo) -> MaquinaTuring:
    transicoes = {}
    estados = set()
    alfabeto = set()
    inicial = ''
    finais = set()
    
    try:
        # Usando 'latin-1' para ler arquivos do Windows sem erros de codificação
        with open(nome_arquivo, "r", encoding="latin-1") as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if not linha or linha.startswith("#"): 
                    continue
                
                # Remove espaços internos para facilitar a leitura dos padrões
                clean_linha = linha.replace(" ", "")
                
                # Leitura de estados: e{...}
                if clean_linha.startswith('e'):
                    match = re.search(r'e\{([^}]+)\}', clean_linha)
                    if match:
                        estados = set(match.group(1).split(","))
                
                # Leitura de alfabeto: a{...}
                elif clean_linha.startswith('a'):
                    match = re.search(r'a\{([^}]+)\}', clean_linha)
                    if match:
                        alfabeto = set(match.group(1).split(","))
                
                # Leitura de estado inicial: i0 ou i{0}
                elif clean_linha.startswith('i'):
                    match = re.search(r'i\{?([^}]+)\}?', clean_linha)
                    if match:
                        inicial = match.group(1)
                
                # Leitura de estados finais: f{...}
                elif clean_linha.startswith('f'):
                    match = re.search(r'f\{([^}]+)\}', clean_linha)
                    if match:
                        finais = set(match.group(1).split(","))
                
                # Leitura de transições: (estado, lido){destino, escrito, direcao}
                elif clean_linha.startswith('('):
                    match = re.match(r'\(([^,]+),([^)]+)\)\{([^}]+)\}', clean_linha)
                    if match:
                        estado_atual = match.group(1)
                        simbolo_lido = match.group(2)
                        acoes = match.group(3).split(',')
                        
                        estado_destino = acoes[0]
                        simbolo_escrito = acoes[1]
                        direcao = acoes[2].upper()
                        
                        transicoes[(estado_atual, simbolo_lido)] = (estado_destino, simbolo_escrito, direcao)
        
        print(f"\n[+] Máquina carregada de '{nome_arquivo}' com sucesso!")
        print(f"    - Estado Inicial: '{inicial}'")
        print(f"    - Estados Finais: {finais}")
        print(f"    - Transições carregadas: {len(transicoes)}")
        
        if not transicoes or not inicial:
            print("ALERTA: O arquivo está com formato inválido.")
            
        return MaquinaTuring(estados, alfabeto, inicial, finais, transicoes)
    
    except Exception as e:
        print(f"Erro ao ler o arquivo '{nome_arquivo}': {e}")
        return None

def ler_cadeia() -> str: 
    return input("\nDigite a cadeia (ou pressione Enter para fita vazia): ")

def verificar_cadeia_mt(mt: MaquinaTuring, cadeia: str) -> bool:
    fita = list(cadeia) if cadeia else ['B']
    cabecote = 0
    estado = mt.inicial
    passo = 0

    print(f"\n--- Iniciando Simulação ---")
    print(f"Cadeia de entrada: '{cadeia}'\n")
    
    while True:
        if cabecote < 0:
            fita.insert(0, 'B')
            cabecote = 0
        elif cabecote >= len(fita):
            fita.append('B')

        simbolo_atual = fita[cabecote]
        
        print(f"[Passo {passo}]")
        fita_visual = "".join(fita)
        print(f"  Fita:   {fita_visual}")
        print(f"          " + " " * cabecote + "^")
        print(f"  Estado: {estado} | Lendo: '{simbolo_atual}'")

        if estado in mt.final:
            print(f"\n>>> STATUS: Cadeia ACEITA no passo {passo} (Alcançou o estado final '{estado}') <<<\n")
            print(f"Fita Final Resultante: {''.join(fita).strip('B')}")
            return True

        acao = mt.transicoes.get((estado, simbolo_atual))

        if acao is None:
            print(f"\n>>> STATUS: Cadeia REJEITADA (Nenhuma transição para o estado '{estado}' lendo '{simbolo_atual}') <<<\n")
            return False

        estado_destino, simbolo_escrito, direcao = acao
        print(f"  Ação:   Escreve '{simbolo_escrito}' -> Vai para '{estado_destino}' -> Move '{direcao}'\n")

        fita[cabecote] = simbolo_escrito
        estado = estado_destino
        
        if direcao == 'R':
            cabecote += 1
        elif direcao == 'L':
            cabecote -= 1
            
        passo += 1

def executar_maquina(nome_arquivo):
    mt = carregar_mt(nome_arquivo)
    if mt is None or not mt.transicoes: 
        return

    while True:
        cadeia = ler_cadeia()
        verificar_cadeia_mt(mt, cadeia)
        
        if input("\nDeseja testar outra cadeia nesta máquina? (s/n): ").strip().lower() != 's':
            break

def main():
    # Garante que todos os arquivos padrão sejam gerados caso não existam
    criar_arquivos_pre_carregados()

    while True:
        print("\n========================================")
        print("     SIMULADOR DE MÁQUINA DE TURING     ")
        print("========================================")
        print(" 1 - Escolher Máquinas Pré-carregadas")
        print(" 2 - Carregar 'arquivo_mt.txt' personalizado")
        print(" 3 - Sair")
        print("----------------------------------------")
        
        escolha = input("Escolha uma opção: ").strip()
        
        if escolha == '1':
            while True:
                print("\n----------------------------------------")
                print("       MÁQUINAS PRÉ-CARREGADAS          ")
                print("----------------------------------------")
                print(" 1 - Inversor de Bits (inversor.txt)")
                print(" 2 - Verificador Par de 'a's (par_de_as.txt)")
                print(" 3 - Soma Unária (soma.txt)")
                print(" 4 - Linguagem AnBn (an_bn.txt)")
                print(" 5 - Voltar ao menu principal")
                print("----------------------------------------")
                
                sub_escolha = input("Escolha a máquina: ").strip()
                
                if sub_escolha == '1':
                    executar_maquina("inversor.txt")
                elif sub_escolha == '2':
                    executar_maquina("par_de_as.txt")
                elif sub_escolha == '3':
                    executar_maquina("soma.txt")
                elif sub_escolha == '4':
                    executar_maquina("an_bn.txt")
                elif sub_escolha == '5':
                    break
                else:
                    print("Opção inválida! Tente novamente.")
                    
        elif escolha == '2':
            executar_maquina("arquivo_mt.txt")
            
        elif escolha == '3':
            print("\nFIM do programa. Até logo!")
            break
        else:
            print("Opção inválida! Por favor, digite 1, 2 ou 3.")

if __name__ == "__main__":
    main()