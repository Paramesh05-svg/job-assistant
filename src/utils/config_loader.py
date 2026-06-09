import yaml

def load_keywords(path="config/keywords.yaml"):
    with open(path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)
