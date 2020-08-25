import copy 
from math import sqrt
import sys

sys.stdout = open("output.txt", "w")


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
        
        if all(self.board[i] != '.' for i in self.black_positions):
            win = True
        elif all(self.board[i] != '.' for i in self.white_positions):
            win = True     
        is_win = win and (not self.is_first_state())
        return is_win 
    
    
    def make_move(self, old_pos, new_pos):
        temp = self.board[old_pos]
        if temp == '.':
            return False
        self.board[old_pos] = self.board[new_pos]
        self.board[new_pos] = temp
        
        #print("Inside make move")
        #self.print_board()
        
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
        #print("ALL MOVES")
        if not list_of_moves:
            #print("No moves possible")
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
            #input()
            #print("Pieces in own camp: ", pos_of_pieces_in_own_camp)
            for pos in pos_of_pieces_in_own_camp:
                moves_list = self.get_next_moves_list(pos, 0)
                if not moves_list:
                    pass
                else:
                    all_moves = all_moves+moves_list
            #print("All moves: ", all_moves)
            #print("len", len(all_moves))
            if all_moves:
                remove_moves = []
                for move in all_moves:
                    #print(move)
                    move_copy = copy.deepcopy(move)
                    positions = get_first_and_final_pos(move_copy)
                    if player == "BLACK":
                        #print("Black player")
                        coord_diff = (positions[1][0] - positions[0][0], positions[1][1] - positions[0][1])
                        #print("Coord diff: ", coord_diff)
                        if (coord_diff[0] >= 1 and coord_diff[1] >=0) or (coord_diff[0] >= 1 and coord_diff[1] >=1) or (coord_diff[0] >= 0 and coord_diff[1] >=1):
                            pass
                        else:
                            remove_moves.append(move)
                            #print(remove_moves)
                            
                               
                    
                    elif player == "WHITE":
                        #print("WHITE")
                        #print(move)
                        coord_diff = (positions[0][0] - positions[1][0], positions[0][1] - positions[1][1])
                        #print("Coord diff: ", coord_diff)
                        if (coord_diff[0] >= 1 and coord_diff[1] >=0) or (coord_diff[0] >= 1 and coord_diff[1] >=1) or (coord_diff[0] >= 0 and coord_diff[1] >=1):
                            pass
                        else:
                            remove_moves.append(move)
                            #print(remove_moves)
                            
                all_moves = [item for item in all_moves if item not in remove_moves]

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
        for row in range(self.size):
            for col in range(self.size):
                print("",self.board[(col,row)],end=" ")
                
            print("\n")
    

        




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






#This function takes a move list, and returns the first and final position of the pawn.
def get_first_and_final_pos(move):
    
    #print(move)
    if len(move) == 3 and (move[0] == 'J' or move[0] == 'E'):
        return [move[1], move[2]]
    if len(move)>0:
        m = move.pop(0)
        first = m[1]
    while len(move) > 0:
        if len(move) == 1:
            move = move.pop()
            #print(move)
        if len(move) == 3 and (move[0] == 'J' or move[0] == 'E'):
            last = move[2]
            #print(last)
            return [first, last]
        else:
            move.pop(0)




def eval_function(game):
    #print("INSIDE EVAL FUNCTION")
    val_B = 0
    val_W = 0
    sld = 0
    
    is_win = game.is_win()
    #print("Winning state: ", is_win)
    
    count_W = 0
    count_B = 0
    for cell in game.board:
        if game.board[cell] == "W":
            if cell in game.black_positions:
                count_W += 1
            sld = sqrt( (cell[0] - 0)**2 + (cell[1] - 0)**2 )
            val_W -= sld
        if game.board[cell] == "B":
            if cell in game.white_positions:
                count_B += 1
            sld = sqrt( (cell[0] - 15)**2 + (cell[1] - 15)**2 )
            val_B += sld
    val = val_W + val_B + count_W*500 - count_B*500
    
    
    if is_win:
        val = val*5
    return val


def minimax(game, move, depth, alpha, beta, max_player):
    
    #print("DEPTH", depth)

    if not move:
        return eval_function(game)
    #Make the move
    move_copy = copy.deepcopy(move)
    positions = get_first_and_final_pos(move_copy)
    #print("POS",positions)
    #print("MOVE and move_copy after getting first and final", move, move_copy)
    valid_move_bool = game.make_move(positions[0], positions[1])



    #depth = 0 
    
    if depth == 0 or game.is_win():
        #print("Depth 0 or win")
        eval_f = eval_function(game)
        #print("EVAL ", eval_f)
        
        #if max player has won 
        if game.turn == "WHITE" and game.is_win():
            eval_f = eval_f + depth
        elif (game.turn == "BLACK") and game.is_win():
            eval_f = eval_f - depth
        
        
        
        #Undo the move before returning
        valid_move_bool = game.make_move(positions[1], positions[0])

        
        return eval_f
    #if moves is empty i.e no more moves
    elif not move:
        #print("EMPTY MOVE\n\n\n")
        eval_f = eval_function(game)
        #print("EVAL ", eval_f)
        
        
        #Undo the move before returning
        valid_move_bool = game.make_move(positions[1], positions[0])

        
        
        return eval_f
    else:
        
        
        
        #Get the next moves from there
        next_moves = game.get_next_moves_list(positions[0], 0)
        
        #Remove the backward moves
        if move and next_moves:
            if(len(move) == 3 and (move[0] == 'J' or move[0] == 'E')):
                back_move = [move[0], move[2], move[1]]
                if back_move in next_moves:
                    #print("MOVE and NEXT MOVE ", move, next_moves)
                    next_moves.remove(back_move)
        
        
        if len(next_moves) > 0:
            if max_player:
                max_val = -99999
                #For each of the next_moves, call minimax
                for i in next_moves:
                    val = minimax(game, i, depth - 1, alpha, beta, False)
                    max_val = max(max_val, val)
                    #print("Updated max val ", max_val)
                    
                    alpha = max(alpha, val)
                    if beta <= alpha:
                        break
                    
                
                #Undo the move before returning
                valid_move_bool = game.make_move(positions[1], positions[0])
                    
                
                return max_val
            
            else:
                #print("inside mini player condition")
                min_val = 99999
                for i in next_moves:
                    val = minimax(game, i, depth - 1, alpha, beta, True)
                    min_val = min(min_val, val)
                    #print("Updated min val ", min_val)
                    

                    beta = min(beta, val)
                    if beta <= alpha:
                        break
                    
                #Undo the move before returning
                valid_move_bool = game.make_move(positions[1], positions[0])
                    
                    
                return min_val
        else:
            #print("Length of next_moves is 0: ", next_moves)

                    
            eval_f = eval_function(game)
            #print("EVAL ", eval_f)
            
            
            #Undo the move before returning
            valid_move_bool = game.make_move(positions[1], positions[0])
            return eval_f



def pick_optimal_move(game, list_of_moves):
    if not list_of_moves:
        return (-1,-1)
    
    count = 0
    depth = 4
    
    #max player is always white
    if game.turn == 'WHITE':
        max_player = True
        best_minimax_val = -99999
    else:
        max_player = False
        best_minimax_val = 99999
    #print("LIST OF MOVES: ", list_of_moves)
    #print("NO: ", len(list_of_moves))
    
    for m in list_of_moves:
        count += 1
        #print("\n\n\n Move number ", count)
        #print("Move ", m)
        #print("Calling minimax to get minimax val of that move")
        minimax_val = minimax(game, m, depth, -99999, 99999, max_player)
        #print("\nMinimax val of the move = ", m," ", minimax_val)
        if max_player:
            #print("WHITE")
            if minimax_val >= best_minimax_val:
                best_minimax_val = minimax_val
                op_move = m
                #print("Updated max value ", best_minimax_val)
                #print("Updated move", op_move)
        else:
            #print("Black")
            if minimax_val <= best_minimax_val:
                best_minimax_val = minimax_val
                op_move = m
                #print("Updated min value ", best_minimax_val)
                #print("Updated move", op_move)
                
    #print("MOVE AND VAL", op_move," ", best_minimax_val)
    
    return op_move



def main():
    game = Board(16)
    all_moves = []
    color = details["turn"]
    all_moves = game.get_all_moves(color)
    
    if len(all_moves) == 0:
        print("No moves possible")
    else:
        o_move = pick_optimal_move(game, all_moves)
        #print(o_move)
        print_move_list(o_move)





if __name__ == "__main__":
	main()





