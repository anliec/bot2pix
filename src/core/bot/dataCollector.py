from core.bot.walker import Walker
from core import env, dofus, Zone

import cv2
import numpy as np
import time
import pytesseract
import os
import random

import itertools


class DataCollector(Walker):
    def __init__(self, workdir, zone, name="Dofus"):
        super(DataCollector, self).__init__(workdir, name=name)
        self.cell_with_interactive_item = set()
        self.cell_w, self.cell_h = 0.0, 0.0
        self.area_bound = zone

    def run(self):
        while not self.killsig.is_set():
            self.update()

    def update(self):
        self.updatePos()
        self.find_resource_area()
        self.random_map_change()

    def random_map_change(self):
        direction = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        random.shuffle(direction)
        min_x, min_y = self.area_bound[0]
        max_x, max_y = self.area_bound[1]
        for d in direction:
            if min_x <= self.currPos[0] + d[0] <= max_x and min_y <= self.currPos[1] + d[1] <= max_y:
                if self.changeMap(d, max_tries=1):
                    return
        print("map change failed, cur pos is: {}".format(self.currPos))

    def find_resource_area(self):
        self.find_interactive_object_tile()

        to_collect = {}
        for mx, my in self.cell_with_interactive_item:
            tile_x = int(round((((mx + my) / 2) + 0.5) * self.cell_w))
            tile_y = int(round((((mx - my) / 2) + 0.5) * self.cell_h))
            screen_x = tile_x + dofus.COMBAT_R.x()
            screen_y = tile_y + dofus.COMBAT_R.y()
            info_im_before_mouse = env.capture(dofus.COMBAT_R)
            env.move(screen_x, screen_y)
            time.sleep(0.5)
            info_im_color = env.capture(dofus.COMBAT_R)
            env.move(dofus.COMBAT_R.right(), dofus.COMBAT_R.bottom())  # reset mouse pos for future image capture
            info_im = cv2.cvtColor(info_im_color, cv2.COLOR_BGR2GRAY)
            _, info_detect = cv2.threshold(info_im, thresh=30, maxval=255, type=cv2.THRESH_BINARY_INV)
            contours, _ = cv2.findContours(info_detect, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            # print(contours)
            # print(len(contours))
            # print(contours[0].shape)
            # print(contours[0])
            selected = []
            for c in contours:
                rect = cv2.boundingRect(c)
                area = cv2.contourArea(c)
                # print(area, rect)
                if area > 2500 and rect[2] * rect[3] * 0.7 < area:
                    selected.append(rect)
            # print(selected)
            if len(selected) > 0:
                x, y, w, h = selected[0]
                # add some margin
                m = 5
                x, y, w, h = x+m, y+m, w-2*m, h-2*m
                crop = info_im_color[y:y+h, x:x+w, :]
                text = self.read_resources_text(crop)
                pic = self.get_tile_image(tile_x, tile_y, info_im_before_mouse)
                pixel_ref = self.get_resource_pixel_ref(info_im_before_mouse, info_im_color, tile_x, tile_y)
                is_resource_available_now = "Epuis" not in text
                self.sav_resource_image(pic, text, mx, my, is_resource_available_now, pixel_ref)
                if is_resource_available_now and "Niveau" not in text and pixel_ref is not None:
                    if pixel_ref in to_collect:
                        print("resource already seen in {}".format(to_collect[pixel_ref]))
                    to_collect[pixel_ref] = (screen_x, screen_y)
            else:
                pic = self.get_tile_image(tile_x, tile_y, info_im_before_mouse)
                self.sav_resource_image(pic, "FP", mx, my, False, None)
            # info_im = cv2.drawContours(info_im, contours[0], -1, (0, 0, 255), 2)
            # cv2.imshow("cap", info_im)
            # cv2.imshow("detect", info_detect)
            # cv2.waitKey()
            # break

        print("trying to collect {} resources".format(len(to_collect)))
        # if len(self.cell_with_interactive_item):
        #     draw = info_im_before_mouse
        #     # Debug draw detected tile and or tile position
        #     print(to_collect)
        #     for x, y in to_collect.values():
        #         x -= dofus.COMBAT_R.x()
        #         y -= dofus.COMBAT_R.y()
        #         cv2.circle(draw, (x, y), int(self.cell_h * 0.5), (255, 0, 0), thickness=3)
        #     cv2.imshow("result", draw)
        #     cv2.waitKey()
        # env.press('shift')
        # time.sleep(0.1)
        # for s_x, s_y in to_collect.values():
        #     env.press('shift')
        #     time.sleep(0.2)
        #     env.click(s_x, s_y)
        #     time.sleep(0.1)
        #     env.release('shift')
        #     time.sleep(0.3)
        # env.release('shift')

        time.sleep(3 * len(to_collect))

    def find_interactive_object_tile(self):
        first_im = env.capture(dofus.COMBAT_R)
        env.press("Y")
        time.sleep(1)
        second_im = env.capture(dofus.COMBAT_R)
        env.release("Y")

        small_im_size = 200, 140  # first_im.shape[1], first_im.shape[0]  #
        first_im_small = cv2.cvtColor(first_im, cv2.COLOR_BGR2GRAY)
        second_im_small = cv2.cvtColor(second_im, cv2.COLOR_BGR2GRAY)
        first_im_small = cv2.resize(first_im_small, dsize=small_im_size, interpolation=cv2.INTER_CUBIC)
        second_im_small = cv2.resize(second_im_small, dsize=small_im_size, interpolation=cv2.INTER_CUBIC)

        diff = cv2.absdiff(first_im_small, second_im_small)
        mask = cv2.threshold(diff, thresh=1, maxval=255, type=cv2.THRESH_BINARY)[1]
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        mask = cv2.erode(mask, kernel)

        # cv2.imshow("first_im", first_im)
        # cv2.imshow("second_im", second_im)
        # cv2.imshow("diff", diff)
        # cv2.imshow("mask", mask)
        # cv2.waitKey()

        self.cell_with_interactive_item = set()
        cell_w, cell_h = small_im_size[0] / 14.50, small_im_size[1] / 20.50
        # print("shape: diff={} im={} small={}".format(diff.shape, first_im.shape, first_im_small.shape))
        # draw = np.array(diff, dtype=np.uint8)
        for y, x in zip(*np.where(mask > 0)):
            x = x / cell_w - 0.5
            y = y / cell_h - 0.5
            mx = int(round(x + y))
            my = int(round(x - y))
            # dx = int(round((((mx + my) / 2) + 0.5) * cell_w))
            # dy = int(round((((mx - my) / 2) + 0.5) * cell_h))
            # cv2.circle(draw, (dx, dy), int(cell_h * 0.5), (255, 0, 0), thickness=3)
            self.cell_with_interactive_item.add((mx, my))
        # cv2.imshow("result diff", draw)
        # cv2.waitKey()
        self.cell_w, self.cell_h = first_im.shape[1] / 14.50, first_im.shape[0] / 20.50

        # Debug draw detected tile and or tile position
        # draw = first_im
        # for mx, my in cell_with_interactive_item:
        #     x = int(round((((mx + my) / 2) + 0.5) * cell_w))
        #     y = int(round((((mx - my) / 2) + 0.5) * cell_h))
        #     # print(mx, my, x, y)
        #     cv2.circle(draw, (x, y), int(cell_h * 0.5), (255, 0, 0), thickness=3)
        # cv2.imshow("result", draw)
        # my = 0
        # for mx, c in zip(range(20), itertools.cycle([(0, 0, 255), (255, 0, 0), (0, 255, 0), (255, 255, 255)])):
        #     x = int(round((((mx + my) / 2) + 0.5) * cell_w))
        #     y = int(round((((mx - my) / 2) + 0.5) * cell_h))
        #     cv2.circle(draw, (x, y), int(5), c, thickness=3)
        # cv2.imshow("line", draw)
        # cv2.waitKey()

    def get_tile_image(self, screen_x, screen_y, base_im):
        x, y = screen_x - self.cell_w, screen_y - self.cell_h
        w, h = self.cell_w * 2, self.cell_h * 2
        x1, y1, x2, y2 = [max(int(i), 0) for i in [x, y, x+w, y+h]]
        return base_im[y1:y2, x1:x2, :]

    def read_resources_text(self, crop_image):
        h, w, c = crop_image.shape
        crop_red = cv2.threshold(crop_image[:, :, 2], thresh=100, maxval=255, type=cv2.THRESH_BINARY_INV)[1]
        # crop_blue = cv2.threshold(crop, thresh=100, maxval=255, type=cv2.THRESH_BINARY_INV)[1]
        # crop_green = cv2.threshold(crop[:,:,1], thresh=100, maxval=255, type=cv2.THRESH_BINARY_INV)[1]
        # crop = ((crop_red + crop_blue + crop_green) > 0).astype(np.uint8) * 255
        crop = crop_red
        crop = cv2.resize(crop, (w * 10, h * 10))
        crop = cv2.blur(crop, (7, 7))
        text = pytesseract.image_to_string(crop, config='--psm 6', lang='fra')
        print(text)
        # crop = cv2.resize(crop, (int(w / 1), int(h / 1)))
        # cv2.imshow("crop", crop)
        # cv2.waitKey()
        return text

    def get_resource_pixel_ref(self, screen_im_no_hover, screen_im_hover, hover_x, hover_y):
        w, h, c = screen_im_hover.shape
        screen_im_hover = cv2.cvtColor(screen_im_hover, cv2.COLOR_BGR2GRAY)
        screen_im_no_hover = cv2.cvtColor(screen_im_no_hover, cv2.COLOR_BGR2GRAY)
        screen_im_hover_small = cv2.resize(screen_im_hover, (0, 0), fx=0.1, fy=0.1)
        screen_im_no_hover_small = cv2.resize(screen_im_no_hover, (0, 0), fx=0.1, fy=0.1)

        mask = ((screen_im_hover_small > screen_im_no_hover_small) * 255).astype(np.uint8)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
        mask = cv2.dilate(mask, kernel)
        contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        # cv2.imshow("mask", mask)
        # cv2.waitKey()

        print(len(contours))

        for i, c in enumerate(contours):
            d = cv2.pointPolygonTest(c, (int(hover_x/10), int(hover_y/10)), measureDist=False)
            if d >= 0:
                # draw = np.array(screen_im_no_hover_small, dtype=np.uint8)
                # cv2.drawContours(draw, contours, i, (0, 0, 255), 3)
                # cv2.imshow("detect", draw)
                # print(c)
                # cv2.waitKey()
                break
        else:
            return None

        key_x, key_y = max(c, key=lambda coord: coord[0][1] + coord[0][0] / 32)[0]
        key_y *= 10
        key_x *= 10
        # draw = screen_im_hover
        # cv2.circle(draw, (key_x, key_y), int(5), 255, thickness=3)
        # cv2.circle(draw, (hover_x, hover_y), int(5), 0, thickness=3)
        # cv2.imshow("size detection", draw)
        # cv2.imshow("mask", mask)
        # cv2.waitKey()
        # translate to absolute coord, round for more robustness
        return key_x, key_y

        # x1 = max(int(hover_x - 2 * self.cell_w), 0)
        # x2 = min(int(hover_x + 2 * self.cell_w), screen_im_hover.shape[1])
        # y1 = max(int(hover_y - 5 * self.cell_h), 0)
        # y2 = min(int(hover_y + 5 * self.cell_h), screen_im_hover.shape[0])
        # no_hover = screen_im_no_hover[y1:y2, x1:x2, :]
        # hover = screen_im_hover[y1:y2, x1:x2, :]
        # no_hover = cv2.cvtColor(no_hover, cv2.COLOR_BGR2GRAY)
        # hover = cv2.cvtColor(hover, cv2.COLOR_BGR2GRAY)
        # # get the "key" as the pixel with lowest on the screen
        # key_y, key_x = max(zip(*np.where(hover > no_hover)), key=lambda coord: coord[0] + coord[1]/32)
        # draw = hover
        # cv2.circle(draw, (key_x, key_y), int(5), (0, 0, 255), thickness=3)
        # cv2.imshow("size detection", draw)
        # cv2.imshow("mask", ((hover > no_hover) * 255).astype(np.uint8))
        # cv2.waitKey()
        # # translate to absolute coord, round for more robustness
        # key_y = int(round((key_y + y1) / 8))
        # key_x = int(round((key_x + x1) / 8))
        # return key_x, key_y

    def sav_resource_image(self, crop_resource_im, text, tile_x, tile_y, is_res_available_now, pixel_ref):
        if pixel_ref is None:
            pixel_ref = -1, -1
        name = text.split('\n')[0]
        if len(name) < 2:
            return
        if is_res_available_now:
            availability = "available"
        else:
            availability = "empty"
        dir_path = os.path.join("data", name, availability)
        os.makedirs(dir_path, exist_ok=True)
        file_name = "map_{}_{}_tile_{}_{}_pixref_{}_{}.png".format(self.currPos[0], self.currPos[1], tile_x, tile_y,
                                                                   pixel_ref[0], pixel_ref[1])
        print(os.path.join(dir_path, file_name))
        cv2.imwrite(os.path.join(dir_path, file_name), crop_resource_im)


if __name__ == '__main__':
    character_name = "Pif-Protect"

    # top_left = (-2, -28)
    # bot_right = (7, -20)
    top_left = (-3, -19)
    bot_right = (7, -15)

    bot = DataCollector(character_name, (top_left, bot_right))
    env.focusDofusWindow(character_name)

    # for _ in range(1):
    while True:
        bot.update()



