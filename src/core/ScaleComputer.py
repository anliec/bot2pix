

class ScaleComputer:
    def __init__(self, win_width, win_height, top_bar_decoration_offset=31):
        self.win_width = win_width
        self.win_height = win_height
        self.top_bar_decoration_offset = top_bar_decoration_offset
        usable_win_height = int(win_height - top_bar_decoration_offset)
        if win_width / 1350 > usable_win_height / 1080:
            self.center_height = usable_win_height
            self.center_width = int(self.center_height * 1350 / 1080)
            self.center_x = int((win_width - self.center_width) / 2)
            self.center_y = int(self.top_bar_decoration_offset)
        else:
            self.center_width = int(win_width)
            self.center_height = int(self.center_width * 1080 / 1350)
            self.center_x = 0
            self.center_y = int(((usable_win_height - self.center_height) / 2) + self.top_bar_decoration_offset)

    def rescale(self, x: int, y: int, original_scale, just_scale: bool = False):
        scale_factor = self.center_width / original_scale.center_width
        if just_scale:
            # useful for the map coordinate on screen
            new_x = int(x * scale_factor)
            new_y = int((y - original_scale.top_bar_decoration_offset) * scale_factor) + self.top_bar_decoration_offset
            # print(scale_factor, x, y, new_x, new_y)
        else:
            # this point is in the center, fix the offset and scale
            new_x = int(self.center_x + scale_factor * (x - original_scale.center_x))
            new_y = int(self.center_y + scale_factor * (y - original_scale.center_y))

        # clip the value to current screen size
        new_x = max(0, min(new_x, self.win_width))
        new_y = max(0, min(new_y, self.win_height))
        return new_x, new_y

    def rescale_rect(self, x, y, w, h, original_scale, just_scale: bool = False):
        new_x, new_y = self.rescale(x, y, original_scale, just_scale)
        x2, y2 = x + w, y + h
        new_x2, new_y2 = self.rescale(x2, y2, original_scale, just_scale)
        return new_x, new_y, (new_x2 - new_x), (new_y2 - new_y)

    def is_in_center(self, x, y):
        return self.center_x <= x <= (self.center_width + self.center_x) \
               and self.center_y <= y <= (self.center_height + self.center_y)



