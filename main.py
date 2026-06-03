

import os

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def imprimir_tabuleiro(board, placar):
    print(f"\n  ✕ {placar['X']}  |  Empate {placar['D']}  |  ○ {placar['O']}\n")
    simbolos = {None: ' ', 'X': '✕', 'O': '○'}
    linhas = [
        f"  {simbolos[board[0]]} │ {simbolos[board[1]]} │ {simbolos[board[2]]}   (1│2│3)",
        f"  ──┼───┼──",
        f"  {simbolos[board[3]]} │ {simbolos[board[4]]} │ {simbolos[board[5]]}   (4│5│6)",
        f"  ──┼───┼──",
        f"  {simbolos[board[6]]} │ {simbolos[board[7]]} │ {simbolos[board[8]]}   (7│8│9)",
    ]
    print('\n'.join(linhas))
    print()

LINHAS_VENCEDORAS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6],
]

def verificar_vencedor(board):
    for linha in LINHAS_VENCEDORAS:
        a, b, c = linha
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    return None

def tabuleiro_cheio(board):
    return all(c is not None for c in board)

def minimax(board, eh_maximizando):
    vencedor = verificar_vencedor(board)
    if vencedor == 'O':
        return 10
    if vencedor == 'X':
        return -10
    if tabuleiro_cheio(board):
        return 0

    if eh_maximizando:
        melhor = -1000
        for i in range(9):
            if board[i] is None:
                board[i] = 'O'
                melhor = max(melhor, minimax(board, False))
                board[i] = None
        return melhor
    else:
        melhor = 1000
        for i in range(9):
            if board[i] is None:
                board[i] = 'X'
                melhor = min(melhor, minimax(board, True))
                board[i] = None
        return melhor

def jogada_ia(board):
    melhor_score = -1000
    melhor_jogada = None
    for i in range(9):
        if board[i] is None:
            board[i] = 'O'
            score = minimax(board, False)
            board[i] = None
            if score > melhor_score:
                melhor_score = score
                melhor_jogada = i
    return melhor_jogada

def pedir_jogada(board, jogador):
    simbolo = '✕' if jogador == 'X' else '○'
    while True:
        try:
            entrada = input(f"  Jogador {simbolo}, escolha uma posição (1-9): ").strip()
            pos = int(entrada) - 1
            if pos < 0 or pos > 8:
                print("  ⚠ Digite um número entre 1 e 9.")
            elif board[pos] is not None:
                print("  ⚠ Posição já ocupada, tente outra.")
            else:
                return pos
        except ValueError:
            print("  ⚠ Entrada inválida. Digite um número.")

def escolher_modo():
    print("\n┌─────────────────────────────┐")
    print("  │      JOGO DA VELHA XO       │")
    print("  └─────────────────────────────┘\n")
    print("  Modos de jogo:")
    print("  [1] Dois jogadores")
    print("  [2] Jogar contra a IA\n")
    while True:
        op = input("  Escolha o modo (1 ou 2): ").strip()
        if op in ('1', '2'):
            return op
        print("Digite 1 ou 2.")

def jogar_partida(modo, placar):
    board = [None] * 9
    jogador_atual = 'X'

    while True:
        limpar_tela()
        imprimir_tabuleiro(board, placar)

        vencedor = verificar_vencedor(board)
        if vencedor:
            simbolo = '✕' if vencedor == 'X' else '○'
            print(f"  Jogador {simbolo} venceu!\n")
            placar[vencedor] += 1
            return

        if tabuleiro_cheio(board):
            print(" Empate!\n")
            placar['D'] += 1
            return

        if modo == '2' and jogador_atual == 'O':
            print(" A sua amiga IA está pensando...")
            pos = jogada_ia(board)
            board[pos] = 'O'
        else:
            pos = pedir_jogada(board, jogador_atual)
            board[pos] = jogador_atual

        jogador_atual = 'O' if jogador_atual == 'X' else 'X'

def main():
    limpar_tela()
    modo = escolher_modo()
    placar = {'X': 0, 'O': 0, 'D': 0}

    while True:
        jogar_partida(modo, placar)
        imprimir_tabuleiro([None]*9, placar)
        resposta = input("  Jogar novamente? (s/n): ").strip().lower()
        if resposta != 's':
            print("\n  Até a próxima cota! \n")
            break

if __name__ == '__main__':
    main()
