from Boardrepresentation.mill_board import MillBoard
from Boardrepresentation.mill_board import draw_millboard
from Boardrepresentation.mill_board import announce_winner
from Boardrepresentation.mill_board import map_text_to_node

class Game:
    def __init__(self):
        self.board = MillBoard()
        self.gameOver = False
        self.turn = 0
        self.players = ["O", "X"]
        self.pieces=[9,9]
        self.pieces_on_board=[9,9]
        self.last_move=None
    
    #Input moves for the game
    def input_move(self):
        while True:
            try:
                #TODO: Wrong condition
                phase_two=18
                
                if (self.pieces_on_board[0]==3 or self.pieces_on_board[1]==3) and self.turn>phase_two:
                    move1 = input("Choose the piece you want to move (e.g., 'A1'): ").strip().upper()
                    move2 = input("Choose the position you want to move the piece to (e.g., 'A4'): ").strip().upper()
                    if(move1=="EXIT" or move2=="EXIT"):
                        self.gameOver=True
                        return
                    while(not(self.board.is_valid_move_phase_three([move1, move2], self.players[self.turn % 2] ))):
                        move1 = input("Choose the piece you want to move (e.g., 'A1'): ").strip().upper()
                        move2 = input("Choose the position you want to move the piece to (e.g., 'A4'): ").strip().upper()
                        if(move1=="EXIT" or move2=="EXIT"):
                            self.gameOver=True
                            return
                    self.board.move_player_phase_three(move1, move2, self.players[self.turn % 2])
                    self.last_move=move2
                    return
                elif self.turn>phase_two:
                    move1 = input("Choose the piece you want to move (e.g., 'A1'): ").strip().upper()
                    next_moves= self.board.get_next_possible_moves(move1)
                    if(not next_moves):
                       print("all neighboring fields are occupied")
                    if(move1=="undo"):
                        return
                    if(move1=="EXIT"):
                        self.gameOver=True
                        return
                    while(not(self.board.is_valid_move_phase_two(move1,self.players[self.turn % 2])) or (not next_moves)):
                        move1 = input("Choose the piece you want to move (e.g., 'A1'): ").strip().upper()
                        next_moves= self.board.get_next_possible_moves(move1)
                        if(move1=="undo"):
                            return
                        if(move1=="EXIT"):
                            self.gameOver=True
                            return
                        elif(not next_moves):
                            print("all neighboring fields are occupied")
                        else:
                            print(f"Next possible moves from {move1}: {next_moves}")

                    move2 = input("Choose the position you want to move the piece to (e.g., 'A4'): ").strip().upper()
                    if(move2=="EXIT"):
                        self.gameOver=True
                        return
                    while(not(self.board.is_valid_move_phase_two_second(move1,move2))):
                        move2 = input("Choose the position you want to move it to (e.g., 'A4'): ").strip().upper()
                        if(move2=="EXIT"):
                            self.gameOver=True
                            return
                    #TODO: Check if the move is valid and apply it to the board
                    
                    self.board.move_player_phase_two(move1, move2,self.players[self.turn % 2])
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
                    self.pieces[(self.turn + 1) % 2]-=1
                    self.pieces_on_board[self.turn % 2]+=1
                    return
                    
            except KeyboardInterrupt:
                EXIT()

    def mill(self):
        if(self.turn>0):
            mill_nodes=self.board.check_for_mill(self.last_move)
            mill = False if mill_nodes is None else True 
            if(mill):
                draw_millboard(self,self.board)
            if(mill_nodes!=None):
                mill_1=map_text_to_node(mill_nodes[0].id)
                mill_2=map_text_to_node(mill_nodes[1].id)
                mill_3=map_text_to_node(mill_nodes[2].id)
                print(f"Mill is build by{mill_3,mill_2,mill_1} ")
            while(mill):
                remove_piece = input("Enter the position of the piece that you want to remove: ").strip().upper()
                mill=not(self.board.remove_player(remove_piece,self.players[(self.turn) % 2]))
                if(remove_piece=="EXIT"):
                    self.gameOver=True
                    return
                self.pieces_on_board[(self.turn) % 2]-=1
            return
    def restart(self):
        if(self.gameOver or self.turn>299 or (self.pieces_on_board[(self.turn-1) % 2]<3 and self.turn>18)):
            restar_text = input("\n Do you want to play again yes/no \n").strip().upper()
            while(restar_text!="YES"or restar_text!="NO"):
                restar_text = input("\n Do you want to play again yes/no \n").strip().upper()
            if(restar_text=="YES"):
                self.board= MillBoard()
                self.gameOver = False
                self.turn = 1
                self.pieces=[9,9]
            if(restar_text=="NO"):
                self.gameOver=True

    def input_game_info(self):
        self.board.player=self.players
        self.board.turn=self.turn
        self.board.pieces=self.pieces
    #Game loop
    def game_loop(self):

        #TODO: Print rules

        while not self.gameOver:
            self.restart()  
            self.input_game_info()
            if(self.turn==0):
               draw_millboard(self,self.board)           
            else:
               self.input_move()
               self.mill()
               draw_millboard(self,self.board)
            announce_winner(self) 
            self.turn += 1


   
