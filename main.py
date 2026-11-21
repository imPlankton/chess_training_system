import chess
import chess.pgn
import io

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
        print(outcome)
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
            
        # if board.is_game_over():
        #     if board.is_checkmate():
        #         print("Checkmate!")
        #         game.headers["Result"] = board.result()
        #         print(game)
        #         break
        #     if board.is_variant_draw():
        #         print("Draw!")
        #         game.headers["Result"] = board.result()
        #         print(game)
        #         break
        #     if board.is_stalemate():
        #         print("Stalemate!")
        #         game.headers["Result"] = board.result()
        #         print(game)
        #         break
        #     if board.is_insufficient_material():
        #         print("Draw!")
        #         game.headers["Result"] = board.result()
        #         print(game)
        #         break
        #     if board.is_fifty_moves():
        #         print("Draw!")
        #         game.headers["Result"] = board.result()
        #         print(game)
        #         break
        #     if board.is_repetition():
        #         print("Draw!")
        #         game.headers["Result"] = board.result()
        #         print(game)
        #         break
        #     if board.is_seventyfive_moves():
        #         print("Draw!")
        #         game.headers["Result"] = board.result()
        #         print(game)
        #         break
    except AssertionError:
        print("Invalid Move")
    except chess.InvalidMoveError:
        print("Please enter a valid move!")
    except ValueError:
        print("Please enter a valid move.")

with open("game.pgn", "w", encoding="utf-8") as file:
    exporter = chess.pgn.FileExporter(file)
    game.accept(exporter)

