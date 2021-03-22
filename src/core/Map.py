
VOID_CELL_ID = 0
OBSTACLE_CELL_ID = 1
WALKABLE_CELL_ID = 2
TEAM_RED_CELL_ID = 3
TEAM_BLUE_CELL_ID = 4


class Map:
    def __init__(self, map_dict):
        self.map_dict = map_dict

    def map_from_array(self, array):
        self.map_dict = {}
        for y, row in enumerate(array):
            for x, v in enumerate(row):
                self.map_dict[(x, y)] = v

    def get_tile(self, pos):
        if pos in self.map_dict:
            return self.map_dict[pos]
        else:
            return VOID_CELL_ID

    def is_tile_blocking_view(self, pos):
        tile_type = self.get_tile(pos)
        return tile_type in [OBSTACLE_CELL_ID, TEAM_BLUE_CELL_ID, TEAM_RED_CELL_ID]

    def is_tile_walkable(self, pos):
        tile_type = self.get_tile(pos)
        return tile_type == WALKABLE_CELL_ID

    @staticmethod
    def dist(p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


