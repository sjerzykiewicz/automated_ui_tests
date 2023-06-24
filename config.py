import yaml

global config

with open("./config.yml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
