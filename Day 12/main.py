

class Character:
    def __init__(self, idd, x, y, edges):
        self.id = idd
        self.x = x
        self.y = y
        self.edges = edges
        self.region = None
        self.neighbors = {}
        self.NE = None
        self.N = None
        self.NW = None
        self.W = None
        self.SW = None
        self.S = None
        self.SE = None
        self.E = None
        self.cardinal_neighbors = []
        self.neighbors = []
        self.same_neighbors = []
        self.is_connected = False
        self.is_visited = False


    def update_neighbors(self):
        self.cardinal_neighbors = [self.N, self.E, self.S, self.W]
        self.neighbors = [self.N, self.NE, self.E, self.SE, self.S, self.SW, self.W, self.NW]
        for neighbor in self.neighbors:
            if neighbor is not None and neighbor.id == self.id: self.same_neighbors.append(neighbor)

    def update_edges(self):
        edges = 0
        for neighbor in self.cardinal_neighbors:
            if neighbor is not None and neighbor.id != self.id:
                edges += 1
            elif neighbor is None:
                edges += 1
        self.edges = edges

    def __str__(self):
        return f'{self.id} {self.x} {self.y}'



class Region:
    def __init__(self, idd, area, perimeter):
        self.id = idd
        self.area = area
        self.perimeter = perimeter
        self.cost = None #area * perimeter
        self.characters = []

    def calculate_cost(self):
        # self.characters.sort(key=lambda c: c.x)
        # self.characters.sort(key=lambda c: c.y)
        # cost = 0

        # for character in self.characters:

        self.cost = self.area * self.perimeter


def connect_same(character):
    same_characters = [character]
    character.is_visited = True

    for neighbor in character.same_neighbors:
        if neighbor.is_visited == False:
            same_characters += connect_same(neighbor)
    return same_characters



with open('demo.txt', 'r') as file:
    lines = file.readlines()


for line in range(len(lines)):
    lines[line] = '#' + lines[line].strip() + '#'
lines.insert(0, '#' * len(lines[0]))
lines.append('#' * len(lines[0]))


characters = []
regions = []

for line in range(1, len(lines)-1):
    for char in range(1, len(lines[line])-1):
        character = Character(lines[line][char], char, line, 0)
        characters.append(character)

for character in characters:

    north = next((c for c in characters if c.x == character.x and c.y == character.y - 1), None)
    east = next((c for c in characters if c.x == character.x + 1 and c.y == character.y), None)
    south = next((c for c in characters if c.x == character.x and c.y == character.y + 1), None)
    west = next((c for c in characters if c.x == character.x - 1 and c.y == character.y), None)

    north_west = next((c for c in characters if c.x == character.x - 1 and c.y == character.y - 1), None)
    north_east = next((c for c in characters if c.x == character.x + 1 and c.y == character.y - 1), None)
    south_west = next((c for c in characters if c.x == character.x - 1 and c.y == character.y + 1), None)
    south_east = next((c for c in characters if c.x == character.x + 1 and c.y == character.y + 1), None)

    character.N = north
    character.E = east
    character.S = south
    character.W = west

    character.NW = north_west
    character.NE = north_east
    character.SW = south_west
    character.SE = south_east

    character.update_neighbors()
    character.update_edges()


for character in characters:
    region_chars = []
    if not character.is_visited:
        region_chars = connect_same(character)
        sum_edges = sum([c.edges for c in region_chars])
        region = Region(character.id, len(region_chars), sum_edges)
        region.characters = region_chars
        region.calculate_cost()
        regions.append(region)


total_cost = 0
for region in regions:
    total_cost += region.cost
    print(f'{region.id} {region.area} {region.perimeter} {region.cost}')

print(total_cost)



