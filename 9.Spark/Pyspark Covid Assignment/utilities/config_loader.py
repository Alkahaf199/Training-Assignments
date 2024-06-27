import yaml

def get_config(config_file='/Users/cellarzero/Sigmoid_Training/9.Spark/Pyspark Covid Assignment/config.yml'):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config
