from random import randint

class Board:
  def __init__(self, size=10, num_mines=10):
    self.size = size
    self.num_mines = num_mines
    self.board = self.make_new_board()
    self.dug_sq = set() #Set of dug squares
    print(self)
  
  def make_new_board(self):
    #Initializes a size x size board with num_mines mines randomly placed

    #Create mineless board
    self.board = [[None for _ in range(self.size)] for _ in range(self.size)]
    #Assign mines randomly
    placed_mines = 0 
    while placed_mines < self.num_mines:
      square = randint(0, self.size ** 2 -1)
      r = square// self.size
      c = square % self.size
      if self.board[r][c] == '*': continue
      self.board[r][c] = '*'
      placed_mines += 1
      
    #check each square for the number of near mines
    for r in range(self.size):
      for c in range(self.size):
        if self.board[r][c]=='*':
          continue
        self.board[r][c] = self.mine_number(r,c)
    return self.board
    
  def mine_number(self, row, col):
    #Takes a mined board and counts  the number of mines close to square (row,col)
    near_mines = 0
    for r in range(max(row-1,0),min(row+1,self.size-1)+1):
      for c in range(max(col-1,0),min(self.size-1,col+1) +1):
        if (r,c) == (row, col): continue
        if self.board[r][c] == '*':
          near_mines += 1
    return near_mines
  
  def dig(self, row, col):

    self.dug_sq.add(row*self.size+col)
    #End digging on bomb
    if self.board[row][col] == '*':   return False
    #End digging on square neighboring mine
    if self.board[row][col] > 0: return True
    for r in range(max(row-1,0),min(row+1,self.size-1)+1):
      for c in range(max(col-1,0),min(self.size-1,col+1) +1):
        #avoid infinite digging loop
        if r*self.size+c in self.dug_sq: continue
        self.dig(r,c)
    return True

  def __str__(self):
    show_board = [[' ' for _ in range(self.size)] for _ in range(self.size)]
    for sq in self.dug_sq:
      r = sq // self.size
      c = sq % self.size
      show_board[r][c] = str(self.board[r][c])
    board_str = ''
    for i,row in enumerate(show_board):
      board_str = board_str+f'{i}| '+' | '.join(row)+' |\n'
    board_str = board_str+ '   '+'   '.join([str(k) for k in range(self.size)])+'   '
    
    return board_str
    

def play(size = 10, mines=10):
  # Create mined board
  game = Board(size, mines)
  
  while len(game.dug_sq)< game.size**2-game.num_mines:  
    #ask for input
    
    move = input("Where do you want to dig? row, column:").split(',')
    [row, col] = [int(move[0]),int(move[1])]  
    #if mine end game lose
    if game.board[row][col]=='*':
      print('You lose.')
      return
    #dig
    game.dig(row,col)
    print(game)
    print(game.dug_sq)
  print('You win.')


if __name__=='__main__':
  play(10,10)
  