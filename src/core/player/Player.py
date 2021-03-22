from core.player.Attack import Attack

import json


class Player:
    # Singleton class
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print('Creating the object')
            cls._instance = super(Player, cls).__new__(cls)
            cls._instance.attacks = []
            cls._instance.name = None
        return cls._instance

    def write_to_json(self, path):
        with open(path, 'w') as f:
            json.dump({"attacks": [a.to_dict() for a in self.attacks],
                       "name": self.name}, f)

    def read_from_json(self, path):
        with open(path, 'r') as f:
            player_dict = json.load(f)
        self.name = player_dict["name"]
        self.attacks = [Attack().from_dict(a) for a in player_dict["attacks"]]
