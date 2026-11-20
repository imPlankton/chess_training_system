import chess
import chess.pgn
import io

board = chess.Board()
game_not_over = True
game = chess.pgn.Game()
node = game
while True:
    try:
        print(board)
        print([move.uci() for move in board.legal_moves])
        user_move = input("UCI Move(from which cell to which cell like e2e4): ")
        if user_move=='q':
            break
        move = chess.Move.from_uci(user_move)
        if board.is_legal(move):
            board.push(move)
        else:
            print("Invalid Move")
            continue

        game.headers["Event"] = "Casual game"
        node = game.add_variation(chess.Move.from_uci(user_move))

        node = node.add_variation(chess.Move.from_uci(user_move))

        if board.is_game_over():
            if board.is_checkmate():
                print("Checkmate!")
                game.headers["Result"] = board.result()
                print(game)
                break
            if board.is_variant_draw():
                print("Draw!")
                game.headers["Result"] = board.result()
                print(game)
                break
            if board.is_stalemate():
                print("Stalemate!")
                game.headers["Result"] = board.result()
                print(game)
                break
    except AssertionError:
        print("Invalid Move")
    except chess.InvalidMoveError:
        print("Please enter a valid move!")
    except ValueError:
        print("Please enter a valid move.")

with open("game.pgn", "w", encoding="utf-8") as file:
    exporter = chess.pgn.FileExporter(file)
    game.accept(exporter)

