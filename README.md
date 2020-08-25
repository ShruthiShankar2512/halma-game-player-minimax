## Halma Game Player - CSCI561
The rules of the Halma Game, as explained in the pdf (`hw2.pdf` as well as `hw-addendum.pdf`) are encoded and implemented from scratch.  
There are two versions, one is a random move picker and an optimal move picker, where the optimal move picker uses the minimax algorithm to look ahead and then pick an optimal move.   
The program `game_player_optimal.py` reads the input file, uses the algorithm to figure out the next move, and returns the next move in the output file.
The input and output file formats are as described.

### Implementation details:
There are multiple classes, the main class being the Board class, which represents the states of the board. The board is implemented using a dictionary, where the key is the position and the value is the type of pawn in that position. This method was chosen so that the indexing issues are taken care of, and access would be fast and efficient.  

All the changes are made to this Board object, via functions defined in this class.  

The minimax algorithm is implemented with Alpha Beta pruning, where the depth of the tree is taken as a parameter. The depth of the minimax tree decides how many moves to look ahead, before making a decision and picking an optimal move.    
For this game to be fit in the minimax function, the move is first done, minimax along with alphabeta pruning is done to look ahead, and then the move is undone again inside this minimax function before returning.    

**The utility/evaluation function:**
The evaluation function evaluates the state of the board at any point of time.  

It sums the Euclidean distance of each pawn from its opponent's camp. It also takes into account and weights very highly, the pawns that are already in the other camp. In order to see which is a better state, it takes the difference of the number of pawns that are in the opponent's camps, and adds it to the sum of squared distances.
This ensures that a player who has managed to move more number of players to the opponent's camp is closer to winning.   

Finally, if the current state is a winning state, that is multiplied by a constant and this ensures that it has the highest possible weight, and this move will always be picked if it is an option.




### Issues:
1. Slow performance, due to the extremely large number of possible moves that has to be looked into, and the branching factor of the tree being extremely high.
2. The evaluation function can be rethought.
3. The evaluation function can be implemented in a more efficient manner. Since it traverses the entire board at every single node of the minimax tree, the algorithm slows down by a lot.
