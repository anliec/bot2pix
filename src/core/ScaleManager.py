from core.ScaleComputer import ScaleComputer


class ScaleManager:
    # Singleton class
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print('Creating the object')
            cls._instance = super(ScaleManager, cls).__new__(cls)
            cls._instance.registered_objects = []
            cls._instance.current_win_width = None
            cls._instance.current_win_height = None
            cls._instance.current_scale = None
        return cls._instance

    def register(self, scaled_object):
        self.registered_objects.append(scaled_object)

    def set_win_size(self, w, h, top_bar_decoration_offset=0):
        if self.current_win_width != w and self.current_win_height != h:
            self.current_win_width = w
            self.current_win_height = h
            self.current_scale = ScaleComputer(w, h, top_bar_decoration_offset)
            for o in self.registered_objects:
                o.rescale(self.current_scale)

    def get_win_w(self):
        return self.current_win_width

    def get_win_h(self):
        return self.current_win_height


