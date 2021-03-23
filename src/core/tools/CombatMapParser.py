import numpy as np
import cv2
from collections import defaultdict

from core.tools.CellCoordinateManager import CellCoordinateManager
from core.Map import Map, VOID_CELL_ID, OBSTACLE_CELL_ID, WALKABLE_CELL_ID, TEAM_RED_CELL_ID, TEAM_BLUE_CELL_ID
from core import env, dofus

CELL_VOID_MAX_LUM = 80
CELL_VOID_MAX_DEVIATION = 20
CELL_COLOR_VOID = np.array([(0, 0, 0), (77, 87, 75), (73, 83, 72), (67, 75, 65), (100, 106, 98), (100, 104, 97),
                            (84, 101, 92), (83, 101, 92), (94, 99, 91), (19, 20, 18), (65, 73, 63), (93, 98, 91),
                            (40, 41, 42), (16, 24, 41), (67, 71, 65)],
                           dtype=np.uint8)
CELL_COLOR_OBSTACLE = np.array([(147, 150, 153), (142, 146, 148), (132, 140, 137)], dtype=np.uint8)
CELL_COLOR_WALKABLE = np.array([(143, 167, 173), (153, 177, 183),
                                (92, 147, 110), (86, 141, 104),  # green tile
                                ], dtype=np.uint8)
CELL_COLOR_BOONES = np.array([(93, 77, 77), (69, 59, 53), (67, 58, 51), (61, 54, 46)], dtype=np.uint8)
CELL_COLOR_TEAM_RED_START = np.array([(0, 34, 221)])
CELL_COLOR_TEAM_BLUE_START = np.array([(173, 135, 129), (166, 128, 122)])

COLOR_BOONES_RED_CIRCLE = [0, 0, 255]
COLOR_BOONES_BLUE_CIRCLE = [255, 0, 0]


def is_color_in_list(c, l):
    for cl in l:
        if np.linalg.norm(c - cl) < 25:
            return True
    return False


class CombatMapParser:
    def __init__(self, crop_map_width=None, crop_map_height=None, cell_h_count=14.5, cell_v_count=20):
        if crop_map_height is None or crop_map_width is None:
            crop_map_height = dofus.COMBAT_R.height()
            crop_map_width = dofus.COMBAT_R.width()
        self.cell_coordinate_manager = CellCoordinateManager(crop_map_width, crop_map_height,
                                                             cell_h_count, cell_v_count)
        self.top_corner_dx = 0
        self.top_corner_dy = int(self.cell_coordinate_manager.cell_h * -0.32)

    def parse_map(self, img=None, is_placement_stage=False):
        if img is None:
            img = env.capture(dofus.COMBAT_R)
        cv2.imwrite("/tmp/dot_noPr.png", img)
        map_dict = {}
        team_red = []
        team_blue = []
        team_blue_start_pos = []
        team_red_start_pos = []
        colors = defaultdict(int)
        for pix_x, pix_y, x, y in self.cell_coordinate_manager.iterate_pixel_coord():
            # cv2.circle(img, (pix_x, pix_y), 3, (255, 0, 0), 3)
            c = img[pix_y + self.top_corner_dy, pix_x + self.top_corner_dx, :]
            c = tuple([int(i) for i in c])
            cv2.circle(img, (pix_x + self.top_corner_dx, pix_y + self.top_corner_dy), 3, c, 6)
            ca = np.array(c, dtype=np.uint8)
            if self.is_void_tile(ca, pix_x, pix_y, img):
                cv2.circle(img, (pix_x, pix_y), 20, (50, 50, 50), 3)
                map_dict[(x, y)] = VOID_CELL_ID
            elif is_color_in_list(ca, CELL_COLOR_OBSTACLE):
                cv2.circle(img, (pix_x, pix_y), 20, (0, 255, 0), 3)
                map_dict[(x, y)] = OBSTACLE_CELL_ID
            elif is_color_in_list(ca, CELL_COLOR_WALKABLE):
                cv2.circle(img, (pix_x, pix_y), 20, (0, 255, 255), 3)
                map_dict[(x, y)] = WALKABLE_CELL_ID
            else:
                if is_placement_stage:
                    if is_color_in_list(ca, CELL_COLOR_TEAM_RED_START):
                        team_red_start_pos.append((x, y))
                        cv2.circle(img, (pix_x, pix_y), 15, (0, 0, 200), 3)
                    elif is_color_in_list(ca, CELL_COLOR_TEAM_BLUE_START):
                        team_blue_start_pos.append((x, y))
                        cv2.circle(img, (pix_x, pix_y), 15, (200, 0, 0), 3)
                is_boones, boone_team = self.is_boones(img, pix_x, pix_y)
                if is_boones and boone_team == "red":
                    cv2.circle(img, (pix_x, pix_y), 20, (0, 0, 255), 3)
                    map_dict[(x, y)] = TEAM_RED_CELL_ID
                    team_red.append((x, y))
                    if is_placement_stage:
                        team_red_start_pos.append((x, y))
                elif is_boones and boone_team == "blue":
                    cv2.circle(img, (pix_x, pix_y), 20, (255, 0, 0), 3)
                    map_dict[(x, y)] = TEAM_BLUE_CELL_ID
                    team_blue.append((x, y))
                    if is_placement_stage:
                        team_blue_start_pos.append((x, y))
                else:
                    cv2.circle(img, (pix_x, pix_y), 20, (0, 255, 255), 1)
                    colors[c] += 1
                    map_dict[(x, y)] = WALKABLE_CELL_ID
        # print(len(colors), sum(colors.values()))
        # print(sorted(colors.items(), key=lambda x: -x[1]))
        # cv2.imshow("dot", img)
        cv2.imwrite("/tmp/dot.png", img)
        # cv2.waitKey(1)
        player_info = {"red": team_red,
                       "blue": team_blue}
        if is_placement_stage:
            player_info["red_start_pos"] = team_red_start_pos
            player_info["blue_start_pos"] = team_red_start_pos

        return Map(map_dict), player_info

    def is_void_tile(self, tile_color, pix_x, pix_y, img):
        if (tile_color.max() - tile_color.min() < CELL_VOID_MAX_DEVIATION and tile_color.max() < CELL_VOID_MAX_LUM) \
                or is_color_in_list(tile_color, CELL_COLOR_VOID):
            if not is_color_in_list(tile_color, CELL_COLOR_BOONES):
                # First do a basic, quick check
                return True
            elif self.is_boones(img, pix_x, pix_y)[0]:
                # If it might be a boones, do the expensive check, and do it again later when we actually check for it
                return False
            else:
                return True
        return False

    @staticmethod
    def count_pixel_of_color(img, color):
        return np.count_nonzero(np.sum(color == img, axis=2) == 3)

    def is_boones(self, img, pix_x, pix_y):
        crop = self.cell_coordinate_manager.crop_img_at_coord(img, pix_x, pix_y, mask_color=(0, 0, 0))
        if crop.shape[0] == 0 or crop.shape[1] == 0:
            return False, ""
        if np.sum(crop[:, :, 2] == 255) > 60:
                # self.count_pixel_of_color(crop, COLOR_BOONES_RED_CIRCLE) > 60:
            # cv2.imshow("red {} {}".format(pix_x, pix_y), crop)
            return True, "red"
        elif np.sum(crop[:, :, 0] == 255) > 60:
            # self.count_pixel_of_color(crop, COLOR_BOONES_BLUE_CIRCLE) > 60:
            # cv2.imshow("blue {} {}".format(pix_x, pix_y), crop)
            return True, "blue"
        else:
            # cv2.imshow("empty {} {}".format(pix_x, pix_y), crop)
            return False, ""

    def click_on_tile(self, pos):
        pix_x = self.cell_coordinate_manager.to_pix_x(*pos) + dofus.COMBAT_R.x()
        pix_y = self.cell_coordinate_manager.to_pix_y(*pos) + dofus.COMBAT_R.y()
        env.click(pix_x, pix_y)


def main():
    import cv2
    import numpy as np
    from core import dofus
    from core.ScaleManager import ScaleManager

    # full_image = cv2.imread("/home/nicolas/Pictures/Screenshot_20210317_190049-1_window_crop_noheader.png")
    # full_image = cv2.imread("/home/nicolas/Pictures/Screenshot_20210318_174552_window_crop_noheader.png")
    # full_image = cv2.imread("/home/nicolas/Pictures/Screenshot_20210318_204752_window_crop_noheader.png")
    # Placement stage
    full_image = cv2.imread("/home/nicolas/Pictures/Screenshot_20210321_092431.png")
    h, w, c = full_image.shape
    print(full_image.shape)
    ScaleManager().set_win_size(w, h)
    x, y, w, h = dofus.COMBAT_R.getRect()
    # img = np.zeros(shape=(h + 100, w + 100, 3), dtype=np.uint8)
    # img[:h, :w, :] = full_image[y:y + h, x:x + w, :]
    img = full_image[y:y + h, x:x + w, :]

    map_parser = CombatMapParser()

    map_parser.parse_map(img, is_placement_stage=True)

    cv2.imshow("dot", img)
    cv2.waitKey()


if __name__ == '__main__':
    main()



