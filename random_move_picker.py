import copy 
from math import sqrt
import random

#Reading contents from the file. Returns a list of all the lines as strings
def readFile(fileName) -> list:
    file = open(fileName,"r")
    lines = file.readlines()
    lines = [i.strip('\n') for i in lines]
    file.close()
    return lines

#Understanding file contents

#Input: array of file elements
# Function takes all the file elements listed as strings, 
#     processes and stores the required information into a dictionary as directed in the problem statement
#Output: Dictionary containing all the reuired information

def getInfo(lines) -> dict:
    details = {}
    details["type"] = lines[0]
    details["turn"] = lines[1]
    details["time"] = lines[2]
    details["board_state"] = []
    for i in range(3,len(lines)):
        details["board_state"].append(lines[i])
    details["board_state"] = [list(word) for word in details["board_state"]]
    return details


lines = readFile("input.txt")
details = getInfo(lines)



class Board:   
    black_positions = [(0,0),(1,0),(2,0),(3,0),(4,0), (0,1),(1,1),(2,1),(3,1),(4,1), (0,2),(1,2),(2,2),(3,2), (0,3),(1,3),(2,3), (0,4),(1,4)]
    white_positions = [(15,15),(14,15),(13,15),(12,15),(11,15), (15,14),(14,14),(13,14),(12,14),(11,14), (15,13),(14,13),(13,13),(12,13), (15,12),(14,12),(13,12), (15,11),(14,11)]
    turn = details["turn"]
    
    #Initializes a board of given size
    def __init__(self, size):
        positions = {}
        positions["BLACK"] = [(0,0),(1,0),(2,0),(3,0),(4,0), (0,1),(1,1),(2,1),(3,1),(4,1), (0,2),(1,2),(2,2),(3,2), (0,3),(1,3),(2,3), (0,4),(1,4)]
        
        positions["WHITE"] = [(15,15),(14,15),(13,15),(12,15),(11,15), (15,14),(14,14),(13,14),(12,14),(11,14), (15,13),(14,13),(13,13),(12,13), (15,12),(14,12),(13,12), (15,11),(14,11)]
        
        positions["B"] = [(0,0),(1,0),(2,0),(3,0),(4,0), (0,1),(1,1),(2,1),(3,1),(4,1), (0,2),(1,2),(2,2),(3,2), (0,3),(1,3),(2,3), (0,4),(1,4)]
        
        positions["W"] = [(15,15),(14,15),(13,15),(12,15),(11,15), (15,14),(14,14),(13,14),(12,14),(11,14), (15,13),(14,13),(13,13),(12,13), (15,12),(14,12),(13,12), (15,11),(14,11)]
        
    
        self.size = size
        self.initialize_board()
    
    #takes the input, creates a dictionary to represesnt the board, with the key as index and value as value in that cell. 
    #This takes care of the indexing issues - uses image-style indexing of a matrix
    def initialize_board(self):
        self.board = {}
        board_list = details["board_state"]
        for x in range(self.size):
            for y in range(self.size):
                self.board[(y,x)] = board_list[x][y]

    #Returns a list of all the possible adjacent moves that a pawn can make.
    def adjacent_moves(self, i, j):
        moves = []
        if self.board[(i,j)] == '.':
            return moves        
        
        neighbors = [(i-1,j),(i,j-1),(i-1,j-1),(i+1,j),(i,j+1),(i+1,j+1),(i+1,j-1),(i-1,j+1)]
        neighbors = [nbr for nbr in neighbors if nbr[0]>=0 and nbr[0]<self.size and nbr[1]>=0 and nbr[1]<self.size]
        
        #Constraint: if a white pawn is in the black camp
        if self.board[(i,j)] == 'W' and (i,j) in self.black_positions:
            #it cannot move out of the black camp 
            #keep moves that are in the black camp
            neighbors = list(set(neighbors).intersection(self.black_positions))
        
        #Constraint: if a black pawn is in the white camp
        if self.board[(i,j)] == 'B' and (i,j) in self.white_positions:
            #it cannot move out of the white camp
            #keep moves that are in the white camp.
            neighbors = list(set(neighbors).intersection(self.white_positions))
        
        for n in neighbors: 
            if self.board[n] == '.':
                moves.append(n)
            else:
                #print("Cant move to",n)   
                pass
            
        #Move of white that starts outside the white cmap and ends up inside the white camp must be removed.
        if (i,j) not in self.white_positions and self.board[(i,j)] == 'W':
            for m in moves:
                if m in self.white_positions:
                    moves.remove(m)                       
        #Move of black that starts outside the black camp and ends up inside the black camp must be removed.
        if (i,j) not in self.black_positions and self.board[(i,j)] == 'B':
            for m in moves:
                if m in self.black_positions:
                    moves.remove(m) 


        moves = [['E', (i,j), m] for m in moves]

        return moves
    

    
    #Get a list of all the possible moves for a position
     #Get a list of all the possible moves for a position
    def get_next_moves_list(self, pos, j_flag):
        #Get all the adjacent and jump moves
        if j_flag == 0:
            adj_moves = self.adjacent_moves(pos[0],pos[1])
        else:
            adj_moves = []
        j_moves = self.jump_moves(pos[0],pos[1])
        
        #For each jump move, first place a pawn in that index, and get all the next moves from that index.
        # Add it to the list. 
        # Concatenate the jump lists
        next_j_moves = []
        temp_changes = []
        for m in j_moves:
            #print(m)
            self.board[m[2]] = self.turn[0]
            temp_changes.append(m[2])
            next_j_moves = self.get_next_moves_list(m[2], 1)
            #next_j_moves = self.jump_moves(m[2][0], m[2][1])
            #print("next moves list of ", m[2])
            #print(next_j_moves)
            if len(next_j_moves) > 0:
                next_j_moves = [[m, next_move] for next_move in next_j_moves]
                
        j_moves = j_moves + next_j_moves
                    
        moves = adj_moves + j_moves
        
        #print("TEMP CHANGES ", temp_changes)
        #Undo all the temp changes and get the b oard state back to the original state.
        for i in temp_changes:         
            self.board[i] = '.'
        
        return moves
    
    
    
    #Check if the board is in the initial state
    def is_first_state(self):
        first_state = False
        for i in self.black_positions: 
            if self.board[i] == 'B' :
                first_state = True
            else:
                first_state = False
                break
        for i in self.white_positions: 
            if self.board[i] == 'W' :
                first_state = True
            else:
                first_state = False
                break
        return first_state
    
    # Returns true if the board is in a winning state
    def is_win(self):
        win = False
        for i in self.black_positions: 
            if self.board[i] != '.' :
                win = True
            else:
                win = False
                break
        for i in self.white_positions: 
            if self.board[i] != '.' :
                win = True
            else:
                win = False
                break        
        is_win = win and (not self.is_first_state())
        return is_win 
    
    
    def make_move(self, old_pos, new_pos):
        temp = self.board[old_pos]
        if temp == '.':
            return False
        self.board[old_pos] = self.board[new_pos]
        self.board[new_pos] = temp
        return True
    
    
    
        #Returns a list of all the jumps that a pawn can make
    def jump_moves(self, i, j):
        #print("INSIDE JUMP")
        moves = []
        if self.board[(i,j)] == '.':
            return moves
        neighbors = [(i-1,j),(i,j-1),(i-1,j-1),(i+1,j),(i,j+1),(i+1,j+1),(i+1,j-1),(i-1,j+1)]
        neighbors = [nbr for nbr in neighbors if nbr[0]>=0 and nbr[0]<self.size and nbr[1]>=0 and nbr[1]<self.size]

        for nbr in neighbors:
            if self.board[nbr] != '.':
                if nbr[0] == i:
                    if nbr[1] == j+1 and j+1 < self.size:
                        if j+2 < self.size and self.board[(i,j+2)] == '.':
                            if (i, j+2) not in moves:
                                moves.append((i, j+2))
                    elif nbr[1] == j-1 and j-1 >= 0:
                        if j-2 >= 0 and self.board[(i,j-2)] == '.':
                            if (i, j-2) not in moves:
                                moves.append((i, j-2))
                elif nbr[1] == j:
                    if nbr[0] == i+1 and i+1 < self.size:
                        if i+2 < self.size and self.board[(i+2, j)] == '.':
                            if (i+2, j) not in moves:
                                moves.append((i+2, j))
                    elif nbr[0] == i-1 and i-1 >= 0:
                        if i-2 >= 0 and self.board[(i-2,j)] == '.':
                            if (i-2, j) not in moves:
                                moves.append((i-2,j))
                elif nbr == (i-1, j-1):
                    if i-2 >=0 and j-2 >=0 and self.board[(i-2,j-2)] == '.':
                        if (i-2,j-2) not in moves:
                            moves.append((i-2,j-2))
                elif nbr == (i+1, j+1):
                    if i+2 < self.size and j+2 < self.size and self.board[(i+2,j+2)] == '.':
                        if (i+2, j+2) not in moves:
                            moves.append((i+2,j+2))
                elif nbr == (i-1, j+1):
                    if i-2 >=0 and j+2 < self.size and self.board[(i-2,j+2)] == '.':
                        if (i-2, j+2) not in moves:
                            moves.append((i-2,j+2)) 
                elif nbr == (i+1, j-1):
                    if i+2 < self.size and j-2 >= 0 and self.board[(i+2,j-2)] == '.':
                        if (i+2, j-2) not in moves:
                            moves.append((i+2,j-2))                   
        else:
            #print("Cant jump over empty cell")            
            pass
        
        
        #Move of white that starts outside the white cmap and ends up inside the white camp must be removed.
        if (i,j) not in self.white_positions and self.board[(i,j)] == 'W':
            for m in moves:
                if m in self.white_positions:
                    moves.remove(m)                       
        #Move of black that starts outside the black camp and ends up inside the black camp must be removed.
        if (i,j) not in self.black_positions and self.board[(i,j)] == 'B':
            for m in moves:
                if m in self.black_positions:
                    moves.remove(m) 
                    
        #Constraint: if a white pawn is in the black camp
        if self.board[(i,j)] == 'W' and (i,j) in self.black_positions:
            #it cannot move out of the black camp.
            #remove the moves that are out of the black camp i.e. keep moves that are in the black camp only
            moves = list(set(moves).intersection(self.black_positions))
        #Constraint: if a black pawn is in the white camp
        if self.board[(i,j)] == 'B' and (i,j) in self.white_positions:
            #it cannot move out of the white camp.
            #remove moves that are out of the white camp 
            moves = list(set(moves).intersection(self.white_positions))        
        moves = [['J',(i,j), m] for m in moves]
        
        return moves
    

            
    def print_all_moves(self,list_of_moves):
        print("ALL MOVES")
        if not list_of_moves:
            print("No moves possible")
            return
        
        for m in list_of_moves:
            print(m)
            
            
    def get_all_moves(self,player):
        color = player[0]
        black_corner = (0,0)
        white_corner = (15,15)
        pos_of_pieces_in_own_camp = []
        all_moves = []
        if player == "WHITE":
            
            piece_in_own_camp = False
            for pos in self.white_positions:
                if self.board[pos] == 'W':
                    piece_in_own_camp = True
                    pos_of_pieces_in_own_camp.append(pos)
                    
        elif player == 'BLACK':
            piece_in_own_camp = False
            for pos in self.black_positions:
                if self.board[pos] == 'B':
                    piece_in_own_camp = True
                    pos_of_pieces_in_own_camp.append(pos)
        
        #If there are pieces in own camp, moves of only those pieces
        if pos_of_pieces_in_own_camp:
            input()
            #print("Pieces in own camp: ", pos_of_pieces_in_own_camp)
            for pos in pos_of_pieces_in_own_camp:
                moves_list = self.get_next_moves_list(pos, 0)
                if not moves_list:
                    pass
                else:
                    all_moves = all_moves+moves_list
            #print("All moves: ", all_moves)
            if all_moves:
                for move in all_moves:
                    move_copy = copy.deepcopy(move)
                    positions = get_first_and_final_pos(move_copy)
                    if player == "WHITE":
                        dist_from_corner_before_move = sqrt( (positions[0][0] - white_corner[0])** 2 + (positions[0][1] - white_corner[1])** 2)
                        dist_from_corner_after_move = sqrt( (positions[1][0] - white_corner[0])** 2 + (positions[1][1] - white_corner[1])** 2)
                        distance_diff = dist_from_corner_after_move - dist_from_corner_before_move
                        if distance_diff <= 0:
                            all_moves.remove(move)
                    elif player == "BLACK":
                        dist_from_corner_before_move = sqrt( (positions[0][0] - black_corner[0])** 2 + (positions[0][1] - black_corner[1])** 2)
                        dist_from_corner_after_move = sqrt( (positions[1][0] - black_corner[0])** 2 + (positions[1][1] - black_corner[1])** 2)
                        distance_diff = dist_from_corner_after_move - dist_from_corner_before_move
                        if distance_diff <= 0:
                            #print("Removing backward move: ", move)
                            all_moves.remove(move)

        #print("All moves after removing backward moves: ", all_moves)
        #if neither of the two alternatives are possible, all_moves will be empty. Move a piece outside the camp.                    
        if len(all_moves) == 0:
            for k in self.board.keys():
                if k not in pos_of_pieces_in_own_camp:
                    if self.board[k] == color:            
                        moves_list = self.get_next_moves_list(k, 0)
                        if not moves_list:
                            pass
                        else:
                            all_moves = all_moves+moves_list
        #return all_moves
        
        
        #if there are no pieces in own camp
        elif not pos_of_pieces_in_own_camp: 
            for k in self.board.keys():
                if self.board[k] == color:            
                    moves_list = self.get_next_moves_list(k, 0)
                    if not moves_list:
                        pass
                    else:
                        all_moves = all_moves+moves_list
        return all_moves
                #print(all_moves)
        
        
    def print_board(self):
        for row in range(16):
            for col in range(16):
                print(self.board[(col,row)],' ',end="")
            print()
    

        


#prints each move according to the required output format
def print_move(move):
    print(move[0], end = " ")
    print(move[1][0], end = "")
    print(",", end = "")
    print(move[1][1], end = " ")
    print(move[2][0], end = "")
    print(",", end = "")
    print(move[2][1])
    
    
def print_move_list(move_list):  
    if not move_list:
        return
    if len(move_list) == 3 and (move_list[0] == 'J' or move_list[0] == 'E'):
        print_move(move_list)
    else:
        move =  move_list.pop(0)
        print_move_list(move)
        if len(move_list) == 1:
            move_list = move_list.pop(0)
            print_move_list(move_list)



def pick_random_move(move_list):
    move = random.choice(move_list)
    return move


def main():
    game = Board(16)
    all_moves = []
    color = details["turn"]
    all_moves = game.get_all_moves(color)
    
    if len(all_moves) == 0:
        print("No moves possible")
    else:
        r_move = pick_random_move(all_moves)
        print_move_list(r_move)



if __name__ == "__main__":
	main()
