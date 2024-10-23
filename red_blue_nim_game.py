import sys

def calculate_score(red, blue, version):
    if version == 'standard':
        return 2 * red + 3 * blue
    elif version == 'misere':
        return 2 * blue + 3 * red
    else:
        return 2 * red + 3 * blue
    
def terminal_state(red, blue):
    return red == 0 or blue == 0

def player_move(red, blue):
    pile = input("Select the pile (red/blue): ").lower()
    while pile not in ['red', 'blue']:
        print("Please select from given options.")
        pile = input("Select the pile (red/blue): ").lower()
    num = int(input("Choose number of marbles to remove (1/2): "))
    while num not in [1, 2]:
        print("Please select from given options.")
        num = int(input("Choose number of marbles to remove (1/2): "))
    if pile == 'red':
        red -= num
        if red < 0:
            red = 0
    elif pile == 'blue':
        blue -= num
        if blue < 0:
            blue = 0
    return red, blue  # Return updated values

def computer_move(red, blue, version, depth):
    if version == 'standard':
        # Implement Minimax with Alpha-Beta Pruning for the standard version
        best_move = minmax(red, blue, version, depth, True, float("-inf"), float("inf"))[1]
    elif version == 'misere':
        # Implement Minimax with Alpha-Beta Pruning for the misère version
        best_move = minmax(red, blue, version, depth, True, float("-inf"), float("inf"))[1]
    else:
        best_move = minmax(red, blue, version, depth, True, float("-inf"), float("inf"))[1]

    # Perform the best move
    if best_move == '2_red':
        red -= 2
        print(f"Computer move: 2 from red")
    elif best_move == '2_blue':
        blue -= 2
        print(f"Computer move: 2 from blue")
    elif best_move == '1_red':
        red -= 1
        print(f"Computer move: 1 from red")
    elif best_move == '1_blue':
        blue -= 1
        print(f"Computer move: 1 from blue")
    return red, blue # Return updated values and turn counter

def minmax(red, blue, version, depth, max_player, alpha, beta):
    if version == 'misere':
        if depth == 0 or terminal_state(red, blue):
            return evaluate(red, blue,version,max_player), None
        if max_player:
            alpha = float("-inf")
            best_move = None
            for move in generate_moves_misere(red, blue, version):
                new_red, new_blue = make_move_misere(red, blue, move, version)
                eval = minmax(new_red, new_blue, version, depth - 1, False, alpha, beta)[0]
                if eval > alpha:
                    alpha = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return alpha, best_move
        else:
            beta = float("inf")
            best_move = None
            for move in generate_moves_misere(red, blue, version):
                new_red, new_blue = make_move_misere(red, blue, move, version)
                eval = minmax(new_red, new_blue, version, depth - 1, True, alpha, beta)[0]
                if eval < beta:
                    beta = eval
                    best_move = move
                beta = min(beta, eval)

                if beta <= alpha:
                    break
            return beta, best_move
    else:
        if depth == 0 or terminal_state(red, blue):
            return evaluate(red, blue,version,max_player), None
        if max_player:
            alpha = float("-inf")
            best_move = None
            for move in generate_moves_standard(red, blue, version):
                new_red, new_blue = make_move_standard(red, blue, move, version)
                eval = minmax(new_red, new_blue, version, depth - 1, False, alpha, beta)[0]
                if eval > alpha:
                    alpha = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return alpha, best_move
        else:
            beta = float("inf")
            best_move = None
            for move in generate_moves_standard(red, blue, version):
                new_red, new_blue = make_move_standard(red, blue, move, version)
                eval = minmax(new_red, new_blue, version, depth - 1, True, alpha, beta)[0]
                if eval < beta:
                    beta = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return beta, best_move

def generate_moves_misere(red, blue, version):
    moves = []
    if version == 'misere':
        if blue >= 1:
            moves.append('1_blue')
        if red >= 1:
            moves.append('1_red')
        if blue >= 2:
            moves.append('2_blue')
        if red >= 2:
            moves.append('2_red')
        
    return moves

def generate_moves_standard(red, blue, version):
    moves = []
    if version == 'standard':
        if red >= 2:
            moves.append('2_red')
        if blue >= 2:
            moves.append('2_blue')        
        if red >= 1:
            moves.append('1_red')       
        if blue >= 1:
            moves.append('1_blue')      
    return moves

def make_move_misere(red, blue, move, version):
    if version == 'misere':
        if move == '1_blue':
            return red, blue - 1
        elif move == '1_red':
            return red - 1, blue
        elif move == '2_blue':
            return red, blue - 2
        elif move == '2_red':
            return red - 2, blue

def make_move_standard(red, blue, move, version):
    if version == 'standard':
        if move == '2_red':
            return red - 2, blue
        elif move == '2_blue':
            return red, blue - 2
        elif move == '1_red':
            return red - 1, blue
        elif move == '1_blue':
            return red, blue - 1

def evaluate(red, blue, version,max_player):     
    if version == 'misere':
        if max_player:
            return (2*red + 3*blue)
        else:
            return -(2*red + 3*blue)
    else:
        if max_player:
            return -(2*red + 3*blue)
        else:
            return (2*red + 3*blue)


        
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: red_blue_nim.py <num-red> <num-blue> [<version>] [<first-player>] [<depth>]")
        sys.exit(1)

    red = int(sys.argv[1])
    blue = int(sys.argv[2])
    version = sys.argv[3] if len(sys.argv) > 3 else 'standard'
    first_player = sys.argv[4] if len(sys.argv) > 4 else 'computer'
    if len(sys.argv) > 5:
        depth = int(sys.argv[5])
    else:
        depth = max(red,blue)
    
    while not terminal_state(red, blue):
        print(f"\nRed marbles: {red}, Blue marbles: {blue}")
        if first_player == 'human': #or (first_player == 'computer' and turn % 2 == 1):
            red, blue = player_move(red, blue)
            if red == 0 or blue == 0:
                print("Computer Wins!" if version == 'misere' else "Computer loose!")
                print("Game Over!")
                print(f"Your Score: {calculate_score(red, blue, version)}" if version == 'standard' else f"Computer Score: {calculate_score(red, blue, version)}")
                break
            red, blue = computer_move(red, blue, version, depth)
            if red == 0 or blue == 0:
                print("You Win!" if version == 'misere' else "You loose!")
                print("Game Over!")
                print(f"Computer Score: {calculate_score(red, blue, version)}" if version == 'standard' else f"Your Score: {calculate_score(red, blue, version)}")
                break
        else:
            red, blue = computer_move(red, blue, version, depth)
            if red == 0 or blue == 0:
                print("You win!" if version == 'misere' else "You loose!")
                print("Game Over!")
                print(f"Computer Score: {calculate_score(red, blue, version)}" if version == 'standard' else f"Your Score: {calculate_score(red, blue, version)}")
                break
            red, blue = player_move(red, blue)
            if red == 0 or blue == 0:
                print("Computer Win!" if version == 'misere' else "Computer loose!")
                print("Game Over!")
                print(f"Your Score: {calculate_score(red, blue, version)}" if version == 'standard' else f"Computer Score: {calculate_score(red, blue, version)}")
                break
            