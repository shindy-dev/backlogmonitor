import json


class Settings:
    def __setattr__(self, name, value):
        if name not in ("path", "data") and isinstance(self.data, dict):
            self.data[name] = value
        super().__setattr__(name, value)

    def __getattr__(self, name):
        if isinstance(self.data, dict) and name in self.data:
            return self.data[name]
        raise AttributeError(
            f"'{type(self).__name__}' object has no attribute '{name}'"
        )

    def __init__(self, path, data):
        self.path = path
        self.data = data

    @staticmethod
    def load(path):
        try:
            with open(path, "r") as f:
                return Settings(path, json.load(f))
        except FileNotFoundError:
            return None

    @staticmethod
    def save(path, data):
        with open(path, "w") as f:
            json.dump(data, f, indent=4)

    def reload(self):
        self = Settings.load(self.path)

    def resave(self):
        Settings.save(self.path, self.data)
