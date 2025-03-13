import random
import copy

# Oyun tahtası boyutu
BOARD_SIZE = 8

# Oyuncu taşları
WHITE = 'W'  # Beyaz taş
BLACK = 'B'  # Siyah taş
EMPTY = '.'  # Boş kare


# Tahtanın başlangıç durumu
def initialize_board():
    board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    # Beyaz taşların başlangıç konumu (sol üst 3x3)
    for i in range(3):
        for j in range(3):
            board[i][j] = WHITE

    # Siyah taşların başlangıç konumu (sağ alt 3x3)
    for i in range(3):
        for j in range(3):
            board[BOARD_SIZE - 1 - i][BOARD_SIZE - 1 - j] = BLACK

    return board


# Tahtayı yazdırma fonksiyonu
def print_board(board):
    for row in board:
        print(' '.join(row))
    print()


# Belirli bir taş için geçerli hamleleri döndür
def get_valid_moves(board, player):
    moves = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # İleri ve yan hareketler

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == player:
                for dx, dy in directions:
                    x, y = i + dx, j + dy
                    # Normal bir kare ileri
                    if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and board[x][y] == EMPTY:
                        moves.append(((i, j), (x, y)))
                    # Atlama hareketi
                    x2, y2 = i + 2 * dx, j + 2 * dy
                    mid_x, mid_y = i + dx, j + dy
                    if (
                            0 <= x2 < BOARD_SIZE and 0 <= y2 < BOARD_SIZE and
                            board[mid_x][mid_y] != EMPTY and board[x2][y2] == EMPTY
                    ):
                        moves.append(((i, j), (x2, y2)))
    return moves


# Tahtanın değerlendirme fonksiyonu
def evaluate_board(board, player):
    target_region = get_target_region(player)
    score = 0
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == player:
                # Hedef bölgesine yakınlık skorunu artır
                target_x, target_y = get_closest_target(i, j, target_region)
                score -= abs(target_x - i) + abs(target_y - j)  # Hedefe uzaklık
    return score


# Hedef bölgesini döndür
def get_target_region(player):
    if player == WHITE:
        return [(BOARD_SIZE - 1 - i, BOARD_SIZE - 1 - j) for i in range(3) for j in range(3)]
    elif player == BLACK:
        return [(i, j) for i in range(3) for j in range(3)]


# Hedef bölgeye en yakın konumu döndür
def get_closest_target(x, y, target_region):
    return min(target_region, key=lambda pos: abs(pos[0] - x) + abs(pos[1] - y))


# Mini-max algoritması
def minimax(board, depth, maximizing_player, player, alpha=float('-inf'), beta=float('inf')):
    opponent = WHITE if player == BLACK else BLACK

    if depth == 0 or is_game_over(board, player):
        return evaluate_board(board, player), None

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        moves = get_valid_moves(board, player)
        for move in moves:
            new_board = make_move(copy.deepcopy(board), move)
            eval_score, _ = minimax(new_board, depth - 1, False, player, alpha, beta)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        moves = get_valid_moves(board, opponent)
        for move in moves:
            new_board = make_move(copy.deepcopy(board), move)
            eval_score, _ = minimax(new_board, depth - 1, True, player, alpha, beta)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move


# Oyunun bitiş durumunu kontrol et
def is_game_over(board, player):
    # Rakip bölgedeki hedef alan
    target_region = get_target_region(player)
    # Hedef bölgede tüm taşların doğru konumlandığını kontrol et
    return all(board[x][y] == player for x, y in target_region)



# Bir hamleyi uygula
def make_move(board, move):
    (from_x, from_y), (to_x, to_y) = move
    board[to_x][to_y] = board[from_x][from_y]
    board[from_x][from_y] = EMPTY
    return board


# Oyun döngüsü tekrar düzenleniyor
def play_game():
    board = initialize_board()
    print("Başlangıç tahtası:")
    print_board(board)

    current_player = WHITE  # Beyaz taşlar başlar
    while True:
        print(f"Sıra: {current_player}")

        # Mevcut oyuncunun hamlelerini hesapla
        valid_moves = get_valid_moves(board, current_player)
        if not valid_moves:
            print(f"{current_player} için geçerli hamle yok! Oyun bitti.")
            winner = BLACK if current_player == WHITE else WHITE
            print(f"{winner} kazandı!")
            break

        # Mini-max ile en iyi hamleyi seç
        _, best_move = minimax(board, depth=3, maximizing_player=True, player=current_player)
        if best_move:
            board = make_move(board, best_move)
            print(f"{current_player} hamle yaptı: {best_move}")
            print_board(board)

            # Eğer oyun bitiş durumu oluştuysa
            if is_game_over(board, current_player):
                print(f"{current_player} kazandı!")
                break

            # Sırayı değiştir
            current_player = WHITE if current_player == BLACK else BLACK
        else:
            print(f"{current_player} için geçerli hamle yok! Oyun bitti.")
            break


# Oyunu tekrar çalıştır
play_game()