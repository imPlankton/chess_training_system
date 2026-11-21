import chess
import chess.pgn


def play_game():
    board = chess.Board()
    game = chess.pgn.Game()
    node = game
    game.headers["Event"] = "Casual game"
    while True:
        try:
            print(board)
            print([move.uci() for move in board.legal_moves])
            user_move = input("UCI Move(from which cell to which cell like e2e4): ")
            if user_move=='q':
                print("Your game remains unfinished.")
                break
            move = chess.Move.from_uci(user_move)
            if board.is_legal(move):
                board.push(move)
            else:
                print("Invalid Move")
                continue

            node = node.add_variation(move)

            outcome = board.outcome(claim_draw=True)
            if outcome:
                game.headers["Result"] = outcome.result()
                print("Game over!")
                if outcome.winner is True:
                    winner = "White"
                elif outcome.winner is False:
                    winner = "Black"
                else:
                    winner = "Draw"
                if winner == "Draw":
                    print("Draw!")
                else:
                    print("Winner:", winner)
                print("Reason:", outcome.termination)
                print(game)
                break

        except AssertionError:
            print("Invalid Move")
        except chess.InvalidMoveError:
            print("Please enter a valid move!")
        except ValueError:
            print("Please enter a valid move.")
    return game


def save_game(game):
    with open("game.pgn", "w", encoding="utf-8") as file:
        exporter = chess.pgn.FileExporter(file)
        game.accept(exporter)


def load_game():
    with open("game.pgn", "r", encoding="utf-8") as file:
        first_game = chess.pgn.read_game(file)
    return first_game


def show_game_moves(game):
    for i, move in enumerate(game.mainline_moves(), start=1):
        print(f"{i}. {move.uci()}")


def replay_game(game):
    replay_board = game.board()
    for move in game.mainline_moves():
        replay_board.push(move)
        print(replay_board,'\n')

if __name__ == "__main__":
    # game = play_game()
    # save_game(game)
    loaded_game = load_game()
    show_game_moves(loaded_game)
    replay_game(loaded_game)