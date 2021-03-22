import cv2
import numpy as np


class CellCoordinateManager:
    def __init__(self, crop_map_width, crop_map_height, cell_h_count=14.5, cell_v_count=20):
        self.crop_map_width = crop_map_width
        self.crop_map_height = crop_map_height
        self.cell_h_count = cell_h_count
        self.cell_v_count = cell_v_count
        self.cell_w = crop_map_width / cell_h_count
        self.cell_h = crop_map_height / cell_v_count
        self.max_w = int(cell_h_count * 2) - 1
        self.max_h = int(cell_v_count * 2) - 1
        print(self.max_h, self.max_w)

    def iterate_map_cord(self):
        x = 0
        y = 0
        while True:
            yield x, y
            y += 1
            if x - y < 0 or x + y >= self.max_w:
                # if go over the top line or too far on the right
                x += 1
                y = -x
                if x - y >= self.max_h:
                    # if we are going to low
                    y = x - self.max_h
                    if x + y >= self.max_w:
                        # if by doing that we are too right again, then we are done
                        break

    def iterate_pixel_coord(self):
        for x, y in self.iterate_map_cord():
            pix_x = self.to_pix_x(x, y)
            pix_y = self.to_pix_y(x, y)
            yield pix_x, pix_y, x, y

    def to_pix_x(self, x, y):
        return int(((x + y) / 2.0 + 0.5) * self.cell_w)

    def to_pix_y(self, x, y):
        return int(((x - y) / 2.0 + 0.5) * self.cell_w / 2.0)

    def crop_img_at_coord(self, img, pix_x, pix_y, mask_color=None):
        x1 = int(pix_x - self.cell_w / 2)
        x2 = int(pix_x + self.cell_w / 2)
        y1 = int(pix_y - self.cell_h / 2)
        y2 = int(pix_y + self.cell_h / 2)
        crop = img[y1:y2, x1:x2, :].copy()
        if mask_color is not None:
            for mx in [0, self.cell_w]:
                for my in [0, self.cell_h]:
                    triangle = np.array([(mx, my), (self.cell_w / 2, my), (mx, self.cell_h / 2)], dtype=np.int32)
                    cv2.fillConvexPoly(crop, triangle, mask_color)
        return crop


if __name__ == '__main__':
    import cv2
    import numpy as np
    from core import dofus
    from core.ScaleManager import ScaleManager

    full_image = cv2.imread("/home/nicolas/Pictures/Screenshot_20210317_190049-1_window_crop_noheader.png")
    h, w, c = full_image.shape
    print(full_image.shape)
    ScaleManager().set_win_size(w, h)
    x, y, w, h = dofus.COMBAT_R.getRect()
    img = np.zeros(shape=(h + 100, w + 100, 3), dtype=np.uint8)
    img[:h, :w, :] = full_image[y:y + h, x:x + w, :]

    coord_manager = CellCoordinateManager(w, h)

    for i, coord in enumerate(coord_manager.iterate_pixel_coord()):
        print(i, coord)
        cv2.circle(img, coord[:2], 3, (255, 0, 0), 3)

    cv2.imshow("dot", img)
    cv2.waitKey()



