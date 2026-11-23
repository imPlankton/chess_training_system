import chess
import chess.pgn
import chess.engine

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


def get_game_positions(game):
    board = game.board()
    positions = [board.copy()]

    for move in game.mainline_moves():
        board.push(move)
        positions.append(board.copy())

    return positions


def analyze_position(position, engine):

    info = engine.analyse(
    position,
    chess.engine.Limit(depth=12),
    )

    white_score = info["score"].white()

    if white_score.is_mate():
        n = white_score.mate()

        if n>0:
            print(f"Mate in {n} for white.")

        elif n<0:
            print(f"Mate in {-n} for black.")

        else:
            print("There is already a mate.")

    else:
        score = white_score.score() / 100
        print(f"Position evaluation: {score:+.2f}")

    if not info.get("pv"):
        print("No best move available.")

    else:
        best_move = info["pv"][0]
        print(f"Best move: {best_move.uci()}")

    return info


def calculate_eval_loss(before_score, after_score, player_color):

    if player_color == chess.WHITE and before_score > after_score:
        eval_score = before_score - after_score
    elif player_color == chess.BLACK and after_score > before_score:
        eval_score = after_score - before_score
    else:
        eval_score = 0.0
    return eval_score


def classify_move(eval_loss):
    if eval_loss <= 0.20:
        return "Good"
    elif eval_loss <= 0.50:
        return "Inaccuracy"
    elif eval_loss <= 1.0:
        return "Mistake"
    else:
        return "Blunder"


def analyze_game(game):
    positions = get_game_positions(game)
    engine = chess.engine.SimpleEngine.popen_uci(
        "engines/stockfish/stockfish-windows-x86-64-universal.exe"
    )
    evaluations = []

    try:
        for position in positions:
            evaluation = analyze_position(position, engine)
            evaluations.append(
                evaluation["score"].white().score() / 100
            )

        statistics = {
            "White": {
                "Good": 0,
                "Inaccuracy": 0,
                "Mistake": 0,
                "Blunder": 0
            },
            "Black": {
                "Good": 0,
                "Inaccuracy": 0,
                "Mistake": 0,
                "Blunder": 0
            }
        }

        for i in range(len(positions) - 1):
            before_position = positions[i]

            before_score = evaluations[i]
            after_score = evaluations[i+1]

            player_color = before_position.turn
            if player_color == chess.WHITE:
                player = "White"
            else:
                player = "Black"

            eval_loss = calculate_eval_loss(before_score,
                                            after_score,
                                            player_color)

            category = classify_move(eval_loss)
            statistics[player][category] += 1

            print(f"Move {i+1} | "
                  f"Evaluation loss: {eval_loss:.2f} | "
                  f"Category: {category}")

        for player, player_stats in statistics.items():

            print(f"\n{player}: ")

            for key, value in player_stats.items():
                print(f" {key}: {value}")

    finally:
        engine.quit()


if __name__ == "__main__":
    loaded_game = load_game()
    analyze_game(loaded_game)