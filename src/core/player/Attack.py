

class Attack:
    def __init__(self):
        self.name = ""
        self.key_shortcut = []
        self.pa_cost = 0
        self.min_range = 0
        self.max_range = 0
        self.need_visibility = True

    def to_dict(self):
        return {"name": self.name,
                "key_shortcut": self.key_shortcut,
                "pa_cost": self.pa_cost,
                "min_range": self.min_range,
                "max_range": self.max_range,
                "need_visibility": self.need_visibility
                }

    def from_dict(self, attack_dict):
        self.name = attack_dict["name"]
        self.key_shortcut = attack_dict["key_shortcut"]
        self.pa_cost = attack_dict["pa_cost"]
        self.min_range = attack_dict["min_range"]
        self.max_range = attack_dict["max_range"]
        self.need_visibility = attack_dict["need_visibility"]










