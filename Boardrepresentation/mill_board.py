
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

    def __repr__(self):
        return f'Node(id={self.id}, occupied={self.occupied}, player={self.player})'

class MillBoard:
    global ID_MAPPING 

    def __init__(self):
        self.node = [Node(i) for i in range(24)]
        self.set_neighbors()

    def set_neighbors(self):
        neighbors = {
            0: {"right": 1, "down": 9},
            1: {"left": 0, "right": 2, "down": 4},
            2: {"left": 1, "down": 14},
            3: {"right": 4, "down": 10},
            4: {"left": 3, "right": 5, "up": 1, "down": 7},
            5: {"left": 4, "down": 13},
            6: {"right": 7, "down": 15},
            7: {"left": 6, "right": 8, "up": 4},
            8: {"left": 7, "up": 5},
            9: {"right": 10, "up": 0, "down": 21},
            10: {"left": 9, "right": 11, "up": 3, "down": 18},
            11: {"left": 10, "up": 2, "down": 23},
            12: {"right": 13, "up": 8, "down": 20},
            13: {"left": 12, "right": 14, "up": 5, "down": 17},
            14: {"left": 13, "up": 2, "down": 22},
            15: {"right": 16, "up": 6},
            16: {"left": 15, "right": 17, "up": 7, "down": 19},
            17: {"left": 16, "up": 13},
            18: {"right": 19, "up": 10},
            19: {"left": 18, "right": 20, "up": 16},
            20: {"left": 19, "up": 12},
            21: {"right": 22, "up": 9},
            22: {"left": 21, "right": 23, "up": 14},
            23: {"left": 22, "up": 11}
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
        id = ID_MAPPING.get(id_map.upper(), None)
        if id ==None:
            raise ValueError(f"{id_map} is no valid Value")
        
        node = self.node[id]
      
        # Check, if Node is already occupied 
        if node.occupied:
            raise ValueError(f"Node with ID {id_map} is already occupied.")
        
        # Occupy the Node and set the PlayerValue
        node.occupied = True
        node.player = player


    def move_player(self, start_id: str, target_id: str):
        start_id = ID_MAPPING.get(start_id.upper(), None)
        target_id = ID_MAPPING.get(target_id.upper(), None)
        # Check, if IDs are in the accepted area
        if start_id ==None:
            raise ValueError("Must be a valid id")
        if target_id ==None:
            raise ValueError("Must be a valid id")
        
        start_node = self.node[start_id] 
        target_node = self.node[target_id]
        
        # Check, if of StartNode is occupied and of TargetNode is not occupied
        if not start_node.occupied:
            raise ValueError(f"StartNode with ID {start_id} is not occupied.")
        if target_node.occupied:
            raise ValueError(f"TargetNode with ID {target_id} is already occupied.")
        
        # Player moves StartNode to the TargetNode
        target_node.player = start_node.player
        target_node.occupied = True
        
        # marks StartNode as unoccupied 
        start_node.player = None
        start_node.occupied = False      

board = MillBoard()

def draw_millboard(board:MillBoard ):
    global A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X
    letter = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X"]
    for i, letter in enumerate(letter):
     globals()[letter] = board.node[i].player or '+'

        
    # Parts of the Board
    number_line =        f'   1──2──3─4─5──6──7'   
    upper_first_line =  f'A  {A}───────{B}───────{C}'
    inner_lines_1 =     f'   │       │       │'
    upper_second_line = f'B  │  {D}────{E}────{F}  │'
    inner_lines_2 =     f'   │  │    │    │  │'
    inner_third_line =  f'C  │  │  {G}─{H}─{I}  │  │'
    inner_lines_3 =     f'   │  │  │   │  │  │'
    middle_line =       f'D  {J}──{K}──{L}   {M}──{N}──{O}'
    lower_third_line =  f'E  │  │  {P}─{Q}─{R}  │  │'
    lower_second_line = f'F  │  {S}────{T}────{U}  │'
    lower_first_line =  f'G  {V}───────{W}───────{X }'
    

    # Assembly of the Boards
    board = [
        number_line,
        upper_first_line,
        inner_lines_1,
        upper_second_line,
        inner_lines_2,
        inner_third_line,
        inner_lines_3,
        middle_line,
        inner_lines_3,
        lower_third_line,
        inner_lines_2,
        lower_second_line,
        inner_lines_1,
        lower_first_line
    ]
    
    print('\n'.join(board))


board.occupy_node("A1","X")
board.move_player("A1","A4")
board.occupy_node("A7","O")
board.move_player("A7","D5")
draw_millboard(board)
board.occupy_node("D1","X")
board.occupy_node("E5","O")
draw_millboard(board)

