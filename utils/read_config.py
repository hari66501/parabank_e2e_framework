import yaml

class ReadConfig:
    def __init__(self, path="config/config.yaml"):
        with open(path) as file:
            self.config = yaml.safe_load(file)

    def get_config(self):
        return self.config
