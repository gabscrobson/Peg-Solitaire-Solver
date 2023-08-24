import sys

class Node():
    def __init__(self, state, parent, action, pegs):
        self.state = state
        self.parent = parent
        self.action = action
        self.pegs = pegs

class Frontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0
    
    # TODO: try some heuristic (maybe distance from center)
    # using a stack for DFS
    def remove(self):
        if self.empty():
            raise Exception("Empty frontier")
        else:
            node = self.frontier.pop()
            return node

class Game():

    def __init__(self, filename):

        # Read file
        with open(filename) as f:
            contents = f.read()

        # Validate
        if contents.count("o") < 1:
            raise Exception("Game must have at least one peg")
        if contents.count("x") < 1:
            raise Exception("Game must have at least one empty space")

        pegs = contents.count("o")

        # Determine height and width of game
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Store initial state
        state = []
        for line in contents:
            state.append(list(line))

        # Create initial state
        self.initial = Node(state=state, parent=None, action=None, pegs=pegs)

    def neighbors(self, node):
        """ Returns all valid neighbors of a state. """
        result = []
        state = node.state
        directions = [[-2, 0], [2, 0], [0, -2], [0, 2]]

        for i in range(self.height):
            for j in range(self.width):
                if state[i][j] == "o":
                    for direction in directions:
                        if (i + direction[0] >= 0 and i + direction[0] < self.height) and (j + direction[1] >= 0 and j + direction[1] < self.width) and state[i + direction[0]][j + direction[1]] == "x" and state[i + direction[0] // 2][j + direction[1] // 2] == "o":
                            new_state = [row[:] for row in state]
                            new_state[i][j] = "x"
                            new_state[i + direction[0] // 2][j + direction[1] // 2] = "x"
                            new_state[i + direction[0]][j + direction[1]] = "o"
                            result.append(Node(state=new_state, parent=node, action=(i, j, direction), pegs=node.pegs - 1))
                            
        return result

    def solve(self):
        """ Finds a solution to the game, if one exists. """

        # Keep track of states expored
        self.explored = set()
        self.num_explored = 0

        # Initialize frontier to just the starting position
        frontier = Frontier()
        frontier.add(self.initial)

        # Keep looping until solution found
        while True:

            # If nothing left in frontier, then no solution
            if frontier.empty():
                print("No solution")
                return False
            
            # Choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1

            # If node is the goal, then we have a solution
            if node.pegs == 1:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                print("Solution found!")
                return True
            
            # Mark node as explored
            self.explored.add(tuple(map(tuple, node.state)))

            # Add neighbors to frontier
            for neighbor in self.neighbors(node):
                if not frontier.contains_state(neighbor.state) and tuple(map(tuple, neighbor.state)) not in self.explored:
                    frontier.add(neighbor)

    def print_solution(self):
        """ Prints the solution. """
        actions, cells = self.solution
        print(f"Solution requires {len(actions)} steps")
        for i in range(len(actions)):
            print(f"Step {i + 1}:")
            for line in cells[i]:
                print("".join(line))
            print(f"A peg at {actions[i][0] + 1}, {actions[i][1] + 1} jumps over a peg at {actions[i][0] + actions[i][2][0] // 2 + 1}, {actions[i][1] + actions[i][2][1] // 2 + 1} to {actions[i][0] + actions[i][2][0] + 1}, {actions[i][1] + actions[i][2][1] + 1}")
            print(" ")

    def output_solution_images(self):
        from PIL import Image, ImageDraw
        """ Outputs an image of each step of the solution. """
        actions, cells = self.solution
        cell_size = 60  # Adjust cell size for a gap between cells
        cell_padding = 5  # Add some padding to the cells
        wall_color = "#888888"
        path_color = "#ff7777"
        peg_color = "#4513b0"
        empty_color = "#444444"
        
        for i in range(len(actions)):
            img = Image.new("RGB", (self.width * cell_size, self.height * cell_size), wall_color)
            draw = ImageDraw.Draw(img)
            for x in range(self.width):
                for y in range(self.height):
                    
                    # Draw cell background
                    draw.ellipse((x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size), fill=wall_color)
                    
                    # Draw different elements based on cell content
                    if (actions[i][0], actions[i][1]) == (y, x):
                        color = path_color
                    elif (actions[i][0] + actions[i][2][0] // 2, actions[i][1] + actions[i][2][1] // 2) == (y, x):
                        color = path_color
                    elif cells[i][y][x] == "o":
                        color = peg_color
                    elif cells[i][y][x] == "x":
                        color = empty_color
                    else:
                        color = wall_color
                    
                    draw.ellipse((x * cell_size + cell_padding, y * cell_size + cell_padding,
                                (x + 1) * cell_size - cell_padding, (y + 1) * cell_size - cell_padding), fill=color)
            
            img.save(f"./solution/step-{i}.png")



g = Game(sys.argv[1])
if g.solve():
    g.print_solution()
    g.output_solution_images()
