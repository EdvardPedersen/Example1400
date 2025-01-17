import curses
import time

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbours = 0
        self.native_neighbours = 0

    def update_neighbours(self, full_map):
        self.neighbours = 0
        self.native_neighbours = 0
        for x in range(self.x - 1, self.x + 2):
            for y in range(self.y - 1 , self.y + 2):
                if (x, y) in full_map and (x, y) != (self.x, self.y):
                    self.neighbours += 1
                    if isinstance(full_map[(x,y)], type(self)):
                        self.native_neighbours += 1

    def survive(self):
        if self.neighbours > 1 and self.neighbours < 4:
            return True
        return False

    def born(self):
        return False

    def draw(self, window, window_upperleft, window_lowerright):
        if self.x <= window_upperleft[0] or self.x >= window_lowerright[0]:
            return
        if self.y <= window_upperleft[1] or self.y >= window_lowerright[1]:
            return
        window.addch(self.y, self.x, self.character)


class ConwayNode(Node):
    def __init__(self, x, y):
        self.character = "X"
        super().__init__(x, y)

    def born(self):
        if self.neighbours == 3:
            return True
        return False

class HighlifeNode(Node):
    def __init__(self, x, y):
        self.character = "O"
        super().__init__(x, y)

    def born(self):
        if self.neighbours == 3 or self.neighbours == 6:
            return True
        return False

class Simulation:
    def __init__(self):
        self.win = curses.initscr()
        self.window_offset = [0,0]
        self.board = {}
        self.active_classes = []

    def run(self):
        while True:
            self.draw()
            self.update_board()
            
    def draw(self):
        size = self.win.getmaxyx()
        upperleft = self.window_offset
        lowerright = [self.window_offset[1] + size[1], self.window_offset[0] + size[0]]
        self.win.erase()
        for square in self.board.values():
            square.draw(self.win, upperleft, lowerright)
        self.win.refresh()
        time.sleep(0.1)

    def update_board(self):
        newboard = self.board.copy()
        self.remove_dead_nodes(newboard)
        self.birth_new_nodes(newboard)
        self.board = newboard
        
    def remove_dead_nodes(self, target_board):
        for coord, node in self.board.items():
            node.update_neighbours(self.board)
            if not node.survive():
                target_board.pop(coord)

    def birth_new_nodes(self, target_board):
        x_values = [coord[0] for coord in self.board.keys()]
        min_x = min(x_values)
        max_x = max(x_values)
        y_values = [coord[1] for coord in self.board.keys()]
        min_y = min(y_values)
        max_y = max(y_values)

        for x in range(min_x-1, max_x + 2):
            for y in range(min_y-1, max_y + 2):
                for cls in self.active_classes:
                    node = cls(x, y)
                    node.update_neighbours(self.board)
                    if node.born() and (x,y) not in self.board and node.native_neighbours > node.neighbours / 2:
                        target_board[(x,y)] = node


    # Legg til nytt brett
    # Tar inn filnavn og klasse på nodene
    # Returnerer ingenting
    def add_board(self, filename, cls):
        if cls not in self.active_classes:
            self.active_classes.append(cls)
        with open(filename) as f:
            for y, line in enumerate(f):
                for x, character in enumerate(line):
                    if character == "x":
                        self.board[(x, y)] = cls(x, y)

if __name__ == "__main__": 
    s = Simulation()
    s.add_board("conway_start", ConwayNode)
    s.add_board("highlife_start", HighlifeNode)
    s.run()

