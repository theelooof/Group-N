import math

# Node class for each playable field 
class Node:
    def __init__(self, id):
        self.id = id
        self.occupied = False
        self.player = None
        self.left = None
        self.right = None
        self.up = None
        self.down = None
        self.turn=0
        self.pieces=None

    def __repr__(self):
        return f'Node(id={self.id}, occupied={self.occupied}, player={self.player}'

class MillBoard:
    global ID_MAPPING 
    

    def __init__(self):
        self.node = [Node(i) for i in range(24)]
        for i in range(24):
            self.node[i].id=i
        self.set_neighbors()
     
    def set_neighbors(self):
        neighbors = {
            0: {"right": 1, "down": 9},
            1: {"left": 0, "right": 2, "down": 4},
            2: {"left": 1, "down": 14},
            3: {"right": 4, "down": 10},
            4: {"left": 3, "right": 5, "up": 1, "down": 7},
            5: {"left": 4, "down": 13},
            6: {"right": 7, "down": 11},
            7: {"left": 6, "right": 8, "up": 4},
            8: {"left": 7, "up": 11},
            9: {"right": 10, "up": 0, "down": 21},
            10: {"left": 9, "right": 11, "up": 3, "down": 18},
            11: {"left": 10, "up": 6, "down": 15},
            12: {"right": 13, "up": 8, "down": 17},
            13: {"left": 12, "right": 14, "up": 5, "down": 20},
            14: {"left": 13, "up": 2, "down": 23},
            15: {"right": 16, "up": 11},
            16: {"left": 15, "right": 17, "down": 19},
            17: {"left": 16, "up": 12},
            18: {"right": 19, "up": 10},
            19: {"left": 18, "right": 20, "up": 16, "down":22},
            20: {"left": 19, "up": 13},
            21: {"right": 22, "up": 9},
            22: {"left": 21, "right": 23, "up": 19},
            23: {"left": 22, "up": 14}
        }
        for node_id, neighbors_ids in neighbors.items():
            node = self.node[node_id]
            for direction, neighbour_id in neighbors_ids.items():
                setattr(node, direction, self.node[neighbour_id])
    
    ID_MAPPING = {
        "A1": 0, "A4": 1, "A7": 2,
        "B2": 3, "B4": 4, "B6": 5,
        "C3": 6, "C4": 7, "C5": 8,
        "D1": 9, "D2": 10, "D3": 11,
        "D5": 12, "D6": 13, "D7": 14,
        "E3": 15, "E4": 16, "E5": 17,
        "F2": 18, "F4": 19, "F6": 20,
        "G1": 21, "G4": 22, "G7": 23
        }
    def occupy_node(self, id_map: str, player: str):
        
        # Check, if id lies in the valid area 
        id = map_node_to_text(str)
        if id ==None:
            raise ValueError(f"{id_map} is no valid Value")
        
        node = self.node[id]
      
        # Check, if Node is already occupied 
        if node.occupied:
            raise ValueError(f"Node with ID {id_map} is already occupied.")
        
        # Occupy the Node and set the PlayerValue
        node.occupied = True
        node.player = player

    def move_player_phase_three(self, start_id: str, target_id: str, player: str):
        start_id = map_node_to_text(start_id)
        target_id = map_node_to_text(target_id)

        if self.node[target_id].occupied:
            return False
        
        # Player moves StartNode to the TargetNode
        self.node[target_id].player = player
        self.node[target_id].occupied = True
        # marks StartNode as unoccupied 
        self.node[start_id].player = None
        self.node[start_id].occupied = False

    def move_player_phase_two(self, start_id: str, target_id: str,player: str):
        start_id = map_node_to_text(start_id)
        target_id = map_node_to_text(target_id)     
   
        # Player moves StartNode to the TargetNode
        self.node[target_id].player = player
        self.node[target_id].occupied = True
        # marks StartNode as unoccupied 
        self.node[start_id].player = None
        self.node[start_id].occupied = False
    
    def move_player_phase_one(self, move: str, player: str):
        move = map_node_to_text(move) 
        self.node[move].player = player
        self.node[move].occupied = True
    # helper function to look in all directions
    def check_muehle_in_direction(self, node, primary_dir, secondary_dir):
        primary_node = getattr(node, primary_dir)
        
        if(primary_node==None):
           return None
        if(primary_dir== secondary_dir):
            secondary_node = getattr(primary_node, secondary_dir) 
        else:
            secondary_node = getattr(node, secondary_dir) 
        if(secondary_node ==None):
           return None
        
        
        nodes = [n for n in [node, primary_node, secondary_node] if n]
        if len(nodes) != 3:
            return None
        if all(n.occupied for n in nodes) and len(set(n.player for n in nodes)) == 1:
            return nodes
        return None
    # checks mill
    def check_for_mill(self, position):
        node_id=map_node_to_text(position)
        if(node_id==None):
            return None
        node = self.node[node_id]
        
        vertical_muehle = (self.check_muehle_in_direction(node, "up", "up") or 
                           self.check_muehle_in_direction(node, "up", "down") or 
                           self.check_muehle_in_direction(node, "down", "down"))
        
        horizontal_muehle = (self.check_muehle_in_direction(node, "left", "left") or 
                             self.check_muehle_in_direction(node, "left", "right") or 
                             self.check_muehle_in_direction(node, "right", "right"))
        if(vertical_muehle!=None):
            return vertical_muehle
        if(horizontal_muehle!=None):
            return horizontal_muehle
        return None
    
    def is_valid_move_phase_three(self,positions,player):
        if positions[0] in ID_MAPPING:
            node_id = map_node_to_text(positions[0])
            node = self.node[node_id]

            if  node.occupied:
                if(player==node.player):
                    return True
                else:
                    print("The starting piece doesn't belong to the current player")
                    return False
            else:
                print(f"The starting position {positions[0]} is not occupied.")
            return False
        
        if positions[1] in ID_MAPPING:
            node_id = map_node_to_text(positions)
            node = self.node[node_id]
            if not node.occupied:
                return True
            else:
                print(f"The target position {positions[1]} is already occupied.")
            return False

    def is_valid_move_phase_two(self,input_position,player):
        if input_position in ID_MAPPING:
            node_id = map_node_to_text(input_position)
            node = self.node[node_id]
            
            # Überprüfe, ob der Knoten bereits belegt ist
            if  node.occupied:
                if(self.turn>17):  
                    if(player==node.player):
                        return True
                    else:
                        print("The select piece doesn't belong to the current player")
                        return False
            else:
                print(f"The position {input_position} is not occupied.")
            return False
    def is_valid_move_phase_two_second(self,start_id, target_id):
        # Überprüfe, ob die Eingabe im ID_MAPPING ist
        
        if  target_id in ID_MAPPING:
            node_id = map_node_to_text(target_id)
            node = self.node[node_id]
            possible_moves=self.get_next_possible_moves(start_id)
            # Überprüfe, ob der Knoten bereits belegt ist
            if not node.occupied:
                if(not target_id in possible_moves):
                   print(f"You can only move between adjacent nodes.") 
                   return False
                return True
            else:
                print(f"The position {target_id} is already occupied.")
        else:
            print(f"Invalid input: {target_id} is not a valid position.")  
        return False       
    def is_valid_move(self,input_position):
        # Überprüfe, ob die Eingabe im ID_MAPPING ist
        if input_position in ID_MAPPING:
            node_id = map_node_to_text(input_position)
            node = self.node[node_id]
            
            # Überprüfe, ob der Knoten bereits belegt ist
            if not node.occupied:
                return True
            else:
                print(f"The position {input_position} is already occupied.")
        else:
            print(f"Invalid input: {input_position} is not a valid position.")  
        return False    
    
    def get_next_possible_moves(self,input_move):
        # Check if the input move is in ID_MAPPING
        if input_move in ID_MAPPING:
            node_id = map_node_to_text(input_move)
            current_node = self.node[node_id]

            # Create a list to store the next possible moves
            next_possible_moves = []

            # Check neighboring nodes for possible moves
            neighbors = [current_node.left, current_node.right, current_node.up, current_node.down]
            for neighbor_node in neighbors:
                if neighbor_node is not None and not neighbor_node.occupied:
                            next_possible_moves.append(map_text_to_node(neighbor_node.id))

            # Convert the list of possible moves to a comma-separated string
            next_moves_text = ", ".join(next_possible_moves)

            return next_moves_text
        else:
            print(f"Invalid input: {input_move} is not a valid position.")
            return ""
    #TODO: Check if Mill is formed and remove a stone of the opponent

    def remove_player(self, position: str, player: str):
        node_id = ID_MAPPING.get(position.upper(), None)
        if(node_id==None):
            print(f"Invalid input: {position} is not a valid position.")
            return False
        already_existing_mill=[]
        is_in_mill = self.check_for_mill(position)
        if(is_in_mill!=None):
            for node in self.node:
                if(node.player!=player and (node.player=="O" or node.player=="X")): 
                    pos = map_text_to_node(node.id)
                    is_in_mill = self.check_for_mill(pos)
                    if(is_in_mill==None):
                        already_existing_mill.append(False)
                    else:
                        already_existing_mill.append(True)
        
        if(not(all(already_existing_mill))):
            print(f"You can't remove mill pieces as long as there are other free pieces left")
            return False
        
        if node_id is None:
            print(f"Invalid position: {position} is not a valid position.")
            return False

        if not self.node[node_id].occupied:
            print(f"No player at position {position} to remove.")
            return False

        if self.node[node_id].player == player:
            print(f"Player {player} cannot remove a piece at position {position}.")
            return False

        self.node[node_id].player = None
        self.node[node_id].occupied = False 
        return True  
    # TODO: Check if Player has only 3 stones left and can move to any free space     

board = MillBoard()

def draw_millboard(self,board:MillBoard):
    global A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X
    letter = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X"]
    for i, letter in enumerate(letter):
     globals()[letter] = board.node[i].player or '+'

        
    # Parts of the Board
    number_line =       f'   1──2──3─4─5──6──7'             + f'    |-----------------------------------------------------------------------------'
    upper_first_line =  f'A  {A}───────{B}───────{C}'       + f'    | The objective of the board game is to perform mills, which is done by'
    inner_lines_11 =    f'   │       │       │'             + f'    | aligning 3 of your pieces in a vertical or horizontal line. When a mill'
    upper_second_line = f'B  │  {D}────{E}────{F}  │'       + f'    | is formed, the player is allowed to remove one of the other players pieces  '
    inner_lines_21 =    f'   │  │    │    │  │'             + f'    | that is not placed in a mill. An opponent’s piece that is part of a mill'
    inner_third_line =  f'C  │  │  {G}─{H}─{I}  │  │'       + f'    | can only be removed if there is no other piece available on the board. '
    inner_lines_31 =    f'   │  │  │   │  │  │'             + f'    | '
    middle_line =       f'D  {J}──{K}──{L}   {M}──{N}──{O}' + f'    | Phase 1: The players take turns to fill the vacant intersections with their '
    inner_lines_32 =    f'   │  │  │   │  │  │'             + f'    |          respective nine pieces. X begins.'
    lower_third_line =  f'E  │  │  {P}─{Q}─{R}  │  │'       + f'    | Phase 2: The players take turns to move their pieces to adjacent vacant  '
    inner_lines_22 =    f'   │  │    │    │  │'             + f'    |          intersections trying to form mills and removing the opponent’s pieces.'
    lower_second_line = f'F  │  {S}────{T}────{U}  │'       + f'    | Phase 3: Phase 3 begins when one of the players has 3 pieces left. '
    inner_lines_12 =    f'   │       │       │'             + f'    |          Here the player is allowed to move their pieces to any vacant '
    lower_first_line =  f'G  {V}───────{W}───────{X }'      + f'    |          intersection.'
    end_line =          f'                    '             + f'    |-------------------------------------------------------------------------------'
    round_line=          f'Player:{self.players[(self.turn+1) % 2]} Pieces:{self.pieces[self.turn % 2]} Round:{self.turn}'
    exit_line=f'Enter "exit" to exit the game'
    # Assembly of the Boards
    board = [
        number_line,
        upper_first_line,
        inner_lines_11,
        upper_second_line,
        inner_lines_21,
        inner_third_line,
        inner_lines_31,
        middle_line,
        inner_lines_32,
        lower_third_line,
        inner_lines_22,
        lower_second_line,
        inner_lines_12,
        lower_first_line,
        end_line,
        round_line,
        exit_line
    ]
    
    print('\n'.join(board))
    
def announce_winner(self):
    if(self.turn>299):
      print('\n'.join(draw_text)) 
    if(self.pieces_on_board[(self.turn ) % 2]<3):
      text=[player_1_winner_text,player_2_winner_text]
      winner_text=text[(self.turn+1)  % 2]
      print('\n'.join(winner_text))
      
def map_text_to_node(id): 
    for key, value in ID_MAPPING.items():
        if value == id:
            return key    


def map_node_to_text(str):
    return ID_MAPPING.get(str.upper(), None)
player1_1=     f'  _____  _                         __  __          ___              '         
player1_2=     f' |  __ \| |                       /_ | \ \        / (_)             '
player1_3=     f' | |__) | | __ _ _   _  ___ _ __   | |  \ \  /\  / / _ _ __  ___    ' 
player1_4=     f' |  ___/| |/ _` | | | |/ _ \ |__|  | |   \ \/  \/ / | | |_ \/ __|   '
player1_5=     f' | |    | | (_| | |_| |  __/ |     | |    \  /\  /  | | | | \__ \   '
player1_6=     f' |_|    |_|\__,_|\__, |\___|_|     |_|     \/  \/   |_|_| |_|___/   '
player1_7=     f'                  __/ |                                             '
player1_8=     f'                 |___/                                              '

player_1_winner_text=[
    player1_1,
    player1_2,
    player1_3,
    player1_4,
    player1_5,
    player1_6,
    player1_7,
    player1_8
]

player2_1= f'  _____  _                         ___   __          ___               '
player2_2= f' |  __ \| |                       |__ \  \ \        / (_)              '
player2_3= f' | |__) | | __ _ _   _  ___ _ __     ) |  \ \  /\  / / _ _ __  ___     '
player2_4= f' |  ___/| |/ _` | | | |/ _ \ |__|   / /    \ \/  \/ / | | |_ \/ __|    '
player2_5= f' | |    | | (_| | |_| |  __/ |     / /_     \  /\  /  | | | | \__ \    '
player2_6= f' |_|    |_|\__,_|\__, |\___|_|    |____|     \/  \/   |_|_| |_|___/    '
player2_7= f'                 __/ |                                                 '
player2_8= f'                |___/                                                  '

player_2_winner_text=[
    player2_1,
    player2_2,
    player2_3,
    player2_4,
    player2_5,
    player2_6,
    player2_7,
    player2_8
]

draw1=f'  _____                         '
draw2=f' |  __ \                        '
draw3=f' | |  | |_ __ __ ___      __    '
draw4=f' | |  | | |__/ _` \ \ /\ / /    '
draw5=f' | |__| | | | (_| |\ V  V /     '
draw6=f' |_____/|_|  \__,_| \_/\_/      '

draw_text=[
    draw1,
    draw2,
    draw3,
    draw4,
    draw5,
    draw6
]