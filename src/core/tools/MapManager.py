from math import ceil, floor
import numpy as np
import unittest
import copy

from core.Map import Map


def is_tile_visible(map_object: Map, a, b):
    a = np.array(a, dtype=np.int32)
    b = np.array(b, dtype=np.int32)
    move = b - a
    i = np.sign(move)
    target = b
    start = a.astype(np.float64) + 0.5
    current_bound = a + np.fmax(i, [0, 0])
    current_pos = a.copy()
    # ignore divide by zero here
    old_setting = np.seterr(divide='ignore')
    while True:
        # print("bound", current_bound)
        # print("pos", current_pos)
        current_move = current_bound - start
        p = current_move / move
        # print("move", current_move, "p", p)
        if p[0] == p[1]:
            current_bound += i
            current_pos += i
        elif not np.isinf(p[0]) and (np.isinf(p[1]) or p[0] < p[1]):
            current_bound[0] += i[0]
            current_pos[0] += i[0]
        else:
            current_bound[1] += i[1]
            current_pos[1] += i[1]

        if (current_pos == target).all():
            # We have reach the target without seeing any obstacle
            # reset np settings
            np.seterr(**old_setting)
            return True
        elif map_object.is_tile_blocking_view(tuple(current_pos)):
            # We are not at the target yet but are on an obstacle
            # print()
            # print("{} is blocking the view ({})".format(current_pos,
            #                                             map_object.get_tile(tuple(current_pos))))
            # print(current_bound, a, b, i, p)
            # reset np settings
            np.seterr(**old_setting)
            return False


def find_shortest_path(map_object: Map, start_pos: np.ndarray, dest_pos: np.ndarray):
    moves = np.array([[0, 1], [1, 0], [-1, 0], [0, -1]])

    def bound(p: np.ndarray):
        return np.linalg.norm(p - dest_pos, ord=1)

    grey = {}
    black = set()

    # initialise grey:
    for move in moves:
        p = start_pos + move
        grey[tuple(p)] = (bound(p), [])

    while len(grey) > 0:
        pos, dists = min(grey.items(), key=lambda x: x[1][0])
        del grey[pos]
        black.add(pos)
        path = dists[1]
        path += [pos]
        if (pos == dest_pos).all():
            return path
        if map_object.is_tile_walkable(pos):
            for move in moves:
                p = pos + move
                p_tuple = tuple(p)
                if p_tuple not in black and p_tuple not in grey:
                    grey[p_tuple] = (bound(p) + len(path), copy.copy(path))
    return []


class TestMapManagerMethods(unittest.TestCase):

    def test_is_tile_visible_close(self):
        map_object = Map({})
        map_object.map_from_array([[2, 2, 2, 2, 2, 2, 4],
                                   [0, 0, 0, 2, 2, 2, 2],
                                   [2, 4, 2, 2, 2, 2, 2],
                                   [2, 1, 2, 3, 2, 1, 2],
                                   [2, 2, 1, 0, 1, 2, 4],
                                   [2, 2, 2, 0, 2, 2, 2],
                                   [2, 2, 2, 4, 2, 2, 2]
                                   ])

        # basic test first:
        # adjacent tiles:
        self.assertTrue(is_tile_visible(map_object=map_object,
                                        a=(3, 3),
                                        b=(3, 2)))
        self.assertTrue(is_tile_visible(map_object=map_object,
                                        a=(3, 3),
                                        b=(3, 4)))
        self.assertTrue(is_tile_visible(map_object=map_object,
                                        a=(3, 3),
                                        b=(2, 3)))
        self.assertTrue(is_tile_visible(map_object=map_object,
                                        a=(3, 3),
                                        b=(4, 3)))
        # Diagonal tiles
        self.assertTrue(is_tile_visible(map_object=map_object,
                                        a=(3, 3),
                                        b=(2, 2)))
        self.assertTrue(is_tile_visible(map_object=map_object,
                                        a=(3, 3),
                                        b=(2, 4)))

    def test_is_tile_visible_far(self):
        map_object = Map({})
        map_object.map_from_array([[2, 2, 2, 2, 2, 2, 4],
                                   [0, 0, 0, 2, 2, 2, 2],
                                   [2, 4, 2, 2, 2, 2, 2],
                                   [2, 1, 2, 3, 2, 1, 2],
                                   [2, 2, 1, 0, 1, 2, 4],
                                   [2, 2, 2, 0, 2, 2, 2],
                                   [2, 2, 2, 4, 2, 2, 2]
                                   ])

        # Further away but no obstacle
        self.assertTrue(is_tile_visible(map_object=map_object,
                                        a=(3, 3),
                                        b=(0, 0)))
        self.assertTrue(is_tile_visible(map_object=map_object,
                                        a=(3, 3),
                                        b=(1, 0)))
        self.assertTrue(is_tile_visible(map_object=map_object,
                                        a=(3, 3),
                                        b=(2, 0)))
        self.assertTrue(is_tile_visible(map_object=map_object,
                                        a=(3, 3),
                                        b=(3, 0)))
        self.assertTrue(is_tile_visible(map_object=map_object,
                                        a=(3, 3),
                                        b=(4, 0)))
        self.assertTrue(is_tile_visible(map_object=map_object,
                                        a=(3, 3),
                                        b=(5, 0)))
        self.assertTrue(is_tile_visible(map_object=map_object,
                                        a=(3, 3),
                                        b=(6, 0)))

    def test_is_tile_far_easy(self):
        map_object = Map({})
        map_object.map_from_array([[2, 2, 2, 2, 2, 2, 4],
                                   [0, 0, 0, 2, 2, 2, 2],
                                   [2, 4, 2, 2, 2, 2, 2],
                                   [2, 1, 2, 3, 2, 1, 2],
                                   [2, 2, 1, 0, 1, 2, 4],
                                   [2, 2, 2, 0, 2, 2, 2],
                                   [2, 2, 2, 4, 2, 2, 2]
                                   ])

        # Further away but no obstacle
        self.assertFalse(is_tile_visible(map_object=map_object,
                                         a=(3, 3),
                                         b=(0, 6)))
        self.assertFalse(is_tile_visible(map_object=map_object,
                                         a=(3, 3),
                                         b=(1, 6)))
        self.assertTrue(is_tile_visible(map_object=map_object,
                                        a=(3, 3),
                                        b=(2, 6)))
        self.assertTrue(is_tile_visible(map_object=map_object,
                                        a=(3, 3),
                                        b=(3, 6)))
        self.assertTrue(is_tile_visible(map_object=map_object,
                                        a=(3, 3),
                                        b=(4, 6)))
        self.assertFalse(is_tile_visible(map_object=map_object,
                                         a=(3, 3),
                                         b=(5, 6)))
        self.assertFalse(is_tile_visible(map_object=map_object,
                                         a=(3, 3),
                                         b=(6, 6)))

    def test_is_tile_far_tricky(self):
        map_object = Map({})
        map_object.map_from_array([[2, 2, 2, 2, 2, 2, 4],
                                   [0, 0, 0, 2, 2, 2, 2],
                                   [2, 4, 2, 2, 2, 2, 2],
                                   [2, 1, 2, 3, 2, 1, 2],
                                   [2, 2, 1, 0, 1, 2, 4],
                                   [2, 2, 2, 0, 2, 2, 2],
                                   [2, 2, 2, 4, 2, 2, 2]
                                   ])

        # Further away but no obstacle
        self.assertTrue(is_tile_visible(map_object=map_object,
                                        a=(3, 3),
                                        b=(0, 4)))
        self.assertFalse(is_tile_visible(map_object=map_object,
                                         a=(3, 3),
                                         b=(1, 4)))
        self.assertFalse(is_tile_visible(map_object=map_object,
                                         a=(3, 3),
                                         b=(0, 5)))
        self.assertFalse(is_tile_visible(map_object=map_object,
                                         a=(3, 3),
                                         b=(0, 3)))

        self.assertTrue(is_tile_visible(map_object=map_object,
                                        a=(3, 3),
                                        b=(6, 4)))
        self.assertFalse(is_tile_visible(map_object=map_object,
                                         a=(3, 3),
                                         b=(5, 4)))
        self.assertFalse(is_tile_visible(map_object=map_object,
                                         a=(3, 3),
                                         b=(6, 5)))
        self.assertFalse(is_tile_visible(map_object=map_object,
                                         a=(3, 3),
                                         b=(6, 3)))

    def test_find_shortest_path(self):
        map_object = Map({})
        map_object.map_from_array([[2, 2, 2, 2, 2, 2, 4],
                                   [0, 0, 0, 2, 2, 2, 2],
                                   [2, 2, 2, 2, 2, 2, 2],
                                   [2, 1, 2, 3, 2, 1, 2],
                                   [2, 2, 1, 0, 1, 2, 4],
                                   [2, 2, 2, 0, 2, 2, 2],
                                   [2, 2, 2, 4, 2, 2, 2]
                                   ])

        # Further away but no obstacle
        self.assertTrue(len(find_shortest_path(map_object=map_object,
                                               start_pos=np.array((3, 3)),
                                               dest_pos=np.array((3, 0)))
                            ) == 3)
        self.assertTrue(len(find_shortest_path(map_object=map_object,
                                               start_pos=np.array((3, 3)),
                                               dest_pos=np.array((0, 0)))
                            ) == 6)
        self.assertTrue(len(find_shortest_path(map_object=map_object,
                                               start_pos=np.array((3, 3)),
                                               dest_pos=np.array((2, 5)))
                            ) == 9)
        self.assertTrue(len(find_shortest_path(map_object=map_object,
                                               start_pos=np.array((3, 3)),
                                               dest_pos=np.array((5, 4)))
                            ) == 0)


def main():
    # map_object = Map()
    # map_object.map_from_array([[2, 2, 2, 2, 2, 2, 4],
    #                            [0, 0, 0, 2, 2, 2, 2],
    #                            [2, 4, 2, 2, 2, 2, 2],
    #                            [2, 1, 2, 3, 2, 1, 2],
    #                            [2, 2, 1, 0, 1, 2, 4],
    #                            [2, 2, 2, 0, 2, 2, 2],
    #                            [2, 2, 2, 4, 2, 2, 2]
    #                            ])
    #
    # # Further away but no obstacle
    # print(is_tile_visible(map_object=map_object,
    #                       a=(3, 3),
    #                       b=(0, 6)))
    unittest.main()


if __name__ == '__main__':
    main()


