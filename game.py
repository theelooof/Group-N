from Boardrepresentation.mill_board import MillBoard
from Boardrepresentation.mill_board import draw_millboard

class Game:
    def __init__(self):
        self.board = MillBoard()
        self.gameOver = False
        self.turn = 0
        self.players = ["X", "O"]
    
    #Input moves for the game
    
    def input_move(self):
        while True:
            try:
                move = input("Enter your move (e.g., 'A1 B2'): ").strip().upper()
                if len(move) == 5 and move[2] == ' ':
                    start_position = move[:2]
                    end_position = move[3:]
                    #TODO: Check if the move is valid and apply it to the board
                    if True:
                        self.board.move_player_phase_two(start_position, end_position)
                        return
                    else:
                        print("Invalid move. Try again.")
                elif len(move) == 2:
                    self.board.move_player_phase_one(move, self.players[self.turn % 2])
                    return
                else:
                    print("Invalid input format. Use 'A1 B2' format.")
            except KeyboardInterrupt:
                exit()


    #Game loop
    def game_loop(self):
        while not self.gameOver:
            draw_millboard(self.board)
            self.input_move()
            self.turn += 1


