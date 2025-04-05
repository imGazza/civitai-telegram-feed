import yaml

def load_config():
    with open('script_config.yaml', 'r') as file:
        return yaml.safe_load(file)

def get_config():
    config = load_config()
    return config