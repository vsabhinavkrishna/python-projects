# Tic-Tac-Toe Game


def display_board(board):
    """Display the board with cell numbers for empty positions."""
    print()
    for row in range(3):
        cells = []
        for col in range(3):
            value = board[row * 3 + col]
            cells.append(value if value != " " else str(row * 3 + col + 1))
        print(" " + " | ".join(cells))
        if row < 2:
            print("---+---+---")
    print()


def get_move(board, player, symbol):
    """Ask the current player for a valid, empty cell."""
    while True:
        choice = input(f"Player {player} ({symbol}), choose a cell (1-9): ").strip()

        if choice == "":
            print("Input cannot be empty. Please try again.")
            continue

        try:
            position = int(choice)
        except ValueError:
            print("Please enter a number from 1 to 9.")
            continue

        if position < 1 or position > 9:
            print("That number is out of range. Choose 1 to 9.")
            continue

        if board[position - 1] != " ":
            print("That cell is already occupied. Choose another one.")
            continue

        return position - 1


def has_won(board, symbol):
    """Return True if the symbol has three in a row, column, or diagonal."""
    winning_lines = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6)              # Diagonals
    ]

    for a, b, c in winning_lines:
        if board[a] == board[b] == board[c] == symbol:
            return True
    return False


def play_game():
    """Run one complete game and return the winner's symbol, or None for a draw."""
    board = [" "] * 9
    current_player = 1
    symbols = {1: "X", 2: "O"}

    print("\nWelcome to Tic-Tac-Toe!")
    print("Choose a cell by entering its number.")
    display_board(board)

    while True:
        symbol = symbols[current_player]
        position = get_move(board, current_player, symbol)
        board[position] = symbol
        display_board(board)

        if has_won(board, symbol):
            print(f"Congratulations! Player {current_player} ({symbol}) wins!")
            return symbol

        if " " not in board:
            print("It's a draw! Well played by both players.")
            return None

        # Switch to the other player.
        current_player = 2 if current_player == 1 else 1


def main():
    """Allow players to play multiple rounds and keep score."""
    scores = {"X": 0, "O": 0, "Draws": 0}

    while True:
        winner = play_game()

        if winner is None:
            scores["Draws"] += 1
        else:
            scores[winner] += 1

        print("\nScoreboard")
        print(f"Player 1 (X): {scores['X']}")
        print(f"Player 2 (O): {scores['O']}")
        print(f"Draws: {scores['Draws']}")

        while True:
            again = input("\nWould you like to play again? (y/n): ").strip().lower()
            if again in ("y", "yes"):
                break
            if again in ("n", "no"):
                print("Thanks for playing Tic-Tac-Toe. Goodbye!")
                return
            print("Please enter y/yes or n/no.")


if __name__ == "__main__":
    main()
