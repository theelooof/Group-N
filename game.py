from Boardrepresentation.mill_board import MillBoard
from Boardrepresentation.mill_board import draw_millboard
from Boardrepresentation.mill_board import announce_winner

class Game:
    def __init__(self):
        self.board = MillBoard()
        self.gameOver = False
        self.turn = 0
        self.players = ["X", "O"]
        self.pieces=[3,3]
        self.last_move=None
    
    #Input moves for the game
    
    def input_move(self):
        while True:
            try:
                
                if self.turn>18:
                    move1 = input("Enter your first move (e.g., 'A1'): ").strip().upper()
                    if(move1=="undo"):
                        return
                    if(move1=="EXIT"):
                        self.gameOver=True
                        return
                    while(not(self.board.is_valid_move(move1))):
                        move1 = input("Choose the piece you want to move (e.g., 'A1'): ").strip().upper()
                        next_moves= self.board.get_next_possible_moves(move1)
                        print(f"Next possible moves from {move1}: {next_moves}")

                        if(move1=="undo"):
                            return
                        if(move1=="EXIT"):
                            self.gameOver=True
                            return

                    move2 = input("Choose the position you want to move the piece to (e.g., 'A4'): ").strip().upper()
                    if(move2=="EXIT"):
                        self.gameOver=True
                        return
                    while(not(self.board.is_valid_move(move2))):
                        move2 = input("Choose the position you want to move it to (e.g., 'A4'): ").strip().upper()
                        if(move2=="EXIT"):
                            self.gameOver=True
                            return
                    #TODO: Check if the move is valid and apply it to the board
                    
                    self.board.move_player_phase_two(move1, move2)
                    self.last_move=move2
                    return
                else:
                    move0 = input("Enter your move (e.g., 'A1, A4,...'): ").strip().upper()
                    if(move0=="EXIT"):
                        self.gameOver=True
                        return
                    while(not(self.board.is_valid_move(move0))):
                        move0 = input("Enter your move (e.g., 'A1, A4,...'): ").strip().upper()
                        if(move0=="EXIT"):
                            self.gameOver=True
                            return
                    self.board.move_player_phase_one(move0, self.players[self.turn % 2])
                    self.last_move=move0
                    return
                    
            except KeyboardInterrupt:
                EXIT()

    def mill(self):
        mill_nodes=self.board.check_for_mill(self.last_move)
        mill = False if mill_nodes is None else True 
        if(mill):
            draw_millboard(self,self.board)
        if(mill_nodes!=None):
            print(f"Mill is build by{mill_nodes[0].id,mill_nodes[1].id,mill_nodes[2].id} ")
        while(mill):
            remove_piece = input("Enter the position of the piece that you want to remove: ").strip().upper()
            mill=not(self.board.remove_player(remove_piece,self.players[self.turn % 2]))
            self.pieces[self.turn % 2]-=1
            if(remove_piece=="EXIT"):
                self.gameOver=True
                return
        if(self.pieces[self.turn % 2]<3):
               announce_winner(self)
               self.restart()
        return
    def restart(self):
        restar_text = input("\n Do you want to pkay again yes/no \n").strip().upper()
        if(restar_text=="YES"):
           self.board= MillBoard()
           self.gameOver = False
           self.turn = 0
           self.pieces=[3,3]
        if(restar_text=="NO"):
           self.gameOver=True


    #Game loop
    def game_loop(self):
        while not self.gameOver:
            self.board.players=self.players
            self.board.turn=self.turn
            self.board.pieces=self.pieces
            if(self.turn==0):
               draw_millboard(self,self.board)           
            else:
               self.input_move()
               if(self.turn>0):
                  self.mill()
               draw_millboard(self,self.board)
               
            self.turn += 1


   
