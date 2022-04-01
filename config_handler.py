import json


class Config:
    def __init__(self):
        self.config = json.load(open("config.json"))

    def update(self, key, value):
        self.config[key] = value
        json.dump(self.config, open("config.json", "w"))

    def get(self, key):
        return self.config[key]

class TodoHandler:
    def __init__(self):
        self.config = json.load(open("todo.json"))

    def update(self, key, value):
        self.config[key] = value
        json.dump(self.config, open("todo.json", "w"))

    def get(self, key):
        if key in self.config.keys():
            return self.config[key]
        return False

    def purge(self):
        for key in self.config.keys():
            self.config.update(key, [])