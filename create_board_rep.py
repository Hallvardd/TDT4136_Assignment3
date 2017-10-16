import os



class Node():

    def __init__(self, coordinates, heuristic, distance_from_start, parent):
        self.coordinates = coordinates
        self.distance_from_start = distance_from_start
        self.heuristic = heuristic
        self.f_value = heuristic + distance_from_start
        self.parent = parent
        self.children = []

    def set_distance_from_start(self, distance_from_start):
        self.distance_from_start = distance_from_start
        self.set_f_value(self.heuristic, self.distance_from_start)

    def get_distance_from_start(self):
        return self.distance_from_start

    def set_heuristic(self,heuristic):
        self.heuristic = heuristic

    def get_heuristic(self):
        return self.heuristic

    def set_f_value(self, heuristic, distance_from_start):
        self.f_value = heuristic + distance_from_start

    def get_f_value(self):
        return self.f_value

    def get_coordinates(self):
        return self.coordinates

    def set_parent(self, parent):
        self.parent = parent

    def get_parent(self):
        return self.parent

    def add_child(self, child):
        self.children.append(child)

    def get_children(self):
        return self.children


board_names = os.listdir("boards")
board_names.sort()
weights = {'w':100, 'm':50, 'f':10, 'g':5, 'r':1, 'B':0, 'A':0}

BASE_DIR = "boards/"
def create_board(file_name):
    # opens the file containing the board, and creates
    # a two dimensional list of line[chars[]]
    txt_board = open(BASE_DIR + file_name)
    board = []
    for l in txt_board:
        board.append(list(l.strip()))
    txt_board.close()
    return board




def find_in_board(board, key):
    line_nr = 0
    for ln in board:
        col_nr = 0
        for i in ln:
            if i == key:
                return [line_nr, col_nr]
            else:
                col_nr += 1
        line_nr += 1
    raise ValueError("The board contains no " + key)


def find_manhattan_dist(A,B):
    return (abs(B[0] - A[0]) + abs(B[1] - A[1]))

def a_star_simple(board, A, B):
    # CLOSED ← ∅; OPEN ← ∅
    _open = []
    _closed = []

    # Generate the initial node, n0, for the start state.
    # Coordinates is set by init of Node-object,
    # f(s) is calculated by h(A) + g(A)
    # parent is set to None signifying start node
    start = Node(A, find_manhattan_dist(A,B),0, None)
    end = B

    #Push n0 onto OPEN
    _open.append(start)

    # Agenda loop
    while True:
        if _open == []:
            return False
        # pops the last element of the list
        x = _open.pop()
        _closed.append(x)
        if x.get_coordinates() == end:
            return _closed, _open

        # generate successors
        coordinates = x.get_coordinates()
        successor_coordinates = []
        for s in[1,-1]:
            # controls for nodes at the edge of the board and for inaccessible nodes
            if 0 <= (coordinates[0] + s) < len(board):
                if board[coordinates[0] + s][coordinates[1]] != '#':
                    successor_coordinates.append([(coordinates[0] + s),coordinates[1]])
            if 0 <= (coordinates[1] + s) < len(board[0]):
                if board[coordinates[0]][coordinates[1] + s] != '#':
                    successor_coordinates.append([coordinates[0], (coordinates[1] + s)])

        for coord in successor_coordinates:
            found = False
            for node in _open:
                if node.get_coordinates() == coord:
                    found = True
                    if node.get_distance_from_start() > x.get_distance_from_start() + 1 :
                        node.set_distance_from_start(x.get_distance_from_start())
                        node.set_parent(x)
                        x.add_child(node)
                        propagate_path_improvements(node)
                        _open.sort(key=lambda x: x.get_f_value(), reverse=True)

            if not found:
                for node in _closed:
                    if node.get_coordinates() == coord:
                        found = True
                        if node.get_distance_from_start() > x.get_distance_from_start() + 1:
                            node.set_distance_from_start(x.get_distance_from_start())
                            node.set_parent(x)
                            x.add_child(node)
                            propagate_path_improvements(node)
                            _open.sort(key=lambda x: x.get_f_value(), reverse=True)

            if not found:
                new_node = Node(coord, find_manhattan_dist(coord,end), x.get_distance_from_start() + 1, x)
                x.add_child(new_node)
                _open.append(new_node)
                _open.sort(key=lambda x: x.get_f_value(), reverse=True)

def a_star_weighted(board, A, B):
    # CLOSED ← ∅; OPEN ← ∅
    _open = []
    _closed = []

    # Generate the initial node, n0, for the start state.
    # Coordinates is set by init of Node-object,
    # f(s) is calculated by h(A) + g(A)
    # parent is set to None signifying start node
    start = Node(A, find_manhattan_dist(A,B),0, None)
    end = B

    #Push n0 onto OPEN
    _open.append(start)

    # Agenda loop
    while True:
        if _open == []:
            return False
        # pops the last element of the list
        x = _open.pop()
        _closed.append(x)
        if x.get_coordinates() == end:
            return _closed, _open

        # generate successors
        coordinates = x.get_coordinates()
        successor_coordinates = []
        for s in[1,-1]:
            # controls for nodes at the edge of the board and for inaccessible nodes
            if 0 <= (coordinates[0] + s) < len(board):
                successor_coordinates.append([(coordinates[0] + s),coordinates[1]])
            if 0 <= (coordinates[1] + s) < len(board[0]):
                successor_coordinates.append([coordinates[0], (coordinates[1] + s)])

        for coord in successor_coordinates:
            found = False
            for node in _open:
                if node.get_coordinates() == coord:
                    found = True
                    if node.get_distance_from_start() > x.get_distance_from_start() + \
                            weights.get(board[node.get_coordinates()[0]][node.get_coordinates()[1]]):
                        node.set_distance_from_start(x.get_distance_from_start())
                        node.set_parent(x)
                        x.add_child(node)
                        propagate_path_improvements_weighted(node)
                        _open.sort(key=lambda x: x.get_f_value(), reverse=True)

            if not found:
                for node in _closed:
                    if node.get_coordinates() == coord:
                        found = True

                        if node.get_distance_from_start() > x.get_distance_from_start() + \
                                weights.get(board[node.get_coordinates()[0]][node.get_coordinates()[1]]):
                            node.set_distance_from_start(x.get_distance_from_start())
                            node.set_parent(x)
                            x.add_child(node)
                            propagate_path_improvements_weighted(node)
                            _open.sort(key=lambda x: x.get_f_value(), reverse=True)

            if not found:
                new_node = Node(coord, find_manhattan_dist(coord,end), x.get_distance_from_start() + weights.get(board[coord[0]][coord[1]]), x)
                x.add_child(new_node)
                _open.append(new_node)
                _open.sort(key=lambda x: x.get_f_value(), reverse=True)


def propagate_path_improvements_weighted(P):
    print("yes")
    for child in P.get_children():
        if child.get_distance_from_start() > (P.get_distance_from_start() +
                                                  weights.get(board[child.get_coordinates()[0]][child.get_coordinates()[1]])):

            child.set_distance_from_start((P.get_distance_from_start() +
                                           weights.get(board[child.get_coordinates()[0]][child.get_coordinates()[1]])))
            propagate_path_improvements_weighted(child)

def propagate_path_improvements(P):
    print("yes")
    for child in P.get_children():
        if child.get_distance_from_start() > (P.get_distance_from_start() + 1):
            child.set_distance_from_start((P.get_distance_from_start() + 1))
            propagate_path_improvements(child)

board = create_board(board_names[-3])
a = find_in_board(board, 'A')
b = find_in_board(board, 'B')
closed_nds, open_nds = (a_star_weighted(board, a, b))
path = []

for n in closed_nds:
    coord = n.get_coordinates()
    board[coord[0]][coord[1]] = "+"
for n in open_nds:
    coord = n.get_coordinates()
    board[coord[0]][coord[1]] = "*"

current_node = closed_nds.pop()
while current_node.get_parent() != None:
    path.append(current_node.get_coordinates())
    current_node = current_node.get_parent()

for i in path:
    board[i[0]][i[1]] = "@"

for l in board:
    print(l)


